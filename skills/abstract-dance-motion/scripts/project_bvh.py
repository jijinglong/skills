#!/usr/bin/env python3
"""Project BVH joints to a canvas-oriented time series. Requires NumPy."""

import argparse
from dataclasses import dataclass
from io import StringIO
import json
import math
from pathlib import Path
import re

import numpy as np


@dataclass(frozen=True)
class Joint:
    name: str
    parent: int
    offset: tuple[float, float, float]
    channels: tuple[str, ...]


def read_bvh(path: Path) -> tuple[list[Joint], np.ndarray, float]:
    hierarchy, motion = re.split(r"(?m)^\s*MOTION\s*$", path.read_text(), maxsplit=1)
    tokens = iter(re.findall(r"[^\s{}]+|[{}]", hierarchy))
    joints: list[Joint] = []

    def require(expected: str) -> None:
        token = next(tokens)
        if token != expected:
            raise ValueError(f"Expected {expected!r} in the hierarchy, got {token!r}")

    def read_joint(name: str, parent: int) -> None:
        require("{")
        require("OFFSET")
        offset = (float(next(tokens)), float(next(tokens)), float(next(tokens)))
        token = next(tokens)
        channels: tuple[str, ...] = ()
        if token == "CHANNELS":
            channels = tuple(next(tokens) for _ in range(int(next(tokens))))
            token = next(tokens)
        index = len(joints)
        joints.append(Joint(name, parent, offset, channels))
        while token != "}":
            if token == "JOINT":
                read_joint(next(tokens), index)
            elif token == "End":
                require("Site")
                read_joint(f"{name}.end", index)
            else:
                raise ValueError(f"Unexpected hierarchy token {token!r}")
            token = next(tokens)

    require("HIERARCHY")
    require("ROOT")
    read_joint(next(tokens), -1)
    lines = motion.strip().splitlines()
    if len(lines) < 3 or not lines[0].startswith("Frames:") or not lines[1].startswith("Frame Time:"):
        raise ValueError("Expected frame count, frame time, and motion channels")
    count = int(lines[0].split(":", 1)[1])
    step = float(lines[1].split(":", 1)[1])
    values = np.loadtxt(StringIO("\n".join(lines[2:])), ndmin=2)
    channels = sum(len(joint.channels) for joint in joints)
    if count < 1 or not math.isfinite(step) or step <= 0 or values.shape != (count, channels):
        raise ValueError("Frame time or channel matrix does not match the BVH header")
    if not np.isfinite(values).all():
        raise ValueError("Motion channels contain non-finite values")
    return joints, values, step


def world_joints(joints: list[Joint], values: np.ndarray) -> np.ndarray:
    length = len(values)
    xyz = np.zeros((length, len(joints), 3))
    rotations = np.zeros((length, len(joints), 3, 3))
    channel_index = 0
    identity = np.broadcast_to(np.eye(3), (length, 3, 3))

    for index, joint in enumerate(joints):
        offset = np.broadcast_to(joint.offset, (length, 3)).copy()
        rotation = identity
        for channel in joint.channels:
            if not re.fullmatch(r"[XYZ](?:position|rotation)", channel):
                raise ValueError(f"Unsupported BVH channel {channel!r}")
            axis = "XYZ".index(channel[0])
            data = values[:, channel_index]
            channel_index += 1
            if channel.endswith("position"):
                offset[:, axis] += data
                continue
            local = identity.copy()
            a, b = (axis + 1) % 3, (axis + 2) % 3
            sine = np.sin(np.deg2rad(data))
            cosine = np.cos(np.deg2rad(data))
            local[:, a, a] = local[:, b, b] = cosine
            local[:, a, b] = -sine
            local[:, b, a] = sine
            rotation = rotation @ local

        if joint.parent < 0:
            xyz[:, index] = offset
            rotations[:, index] = rotation
        else:
            parent_rotation = rotations[:, joint.parent]
            xyz[:, index] = xyz[:, joint.parent] + (parent_rotation @ offset[:, :, None])[:, :, 0]
            rotations[:, index] = parent_rotation @ rotation
    return xyz


def project(joints: list[Joint], xyz: np.ndarray, args: argparse.Namespace) -> tuple[list[str], np.ndarray]:
    lookup = {joint.name: i for i, joint in enumerate(joints)}
    names = [joint.name for joint in joints if not joint.name.endswith(".end")]
    if args.joints:
        names = [name.strip() for name in args.joints.split(",")]
    for name in [args.root, *args.shoulders, *args.floor_joints, *names]:
        if name not in lookup:
            raise ValueError(f"Joint {name!r} was not found. Available joints: {', '.join(lookup)}")
    left, right = (xyz[:, lookup[name]] for name in args.shoulders)
    shoulder_axis = np.median((right - left)[:, [0, 2]], axis=0)
    span = np.linalg.norm(shoulder_axis)
    if span < 1e-6:
        raise ValueError("Shoulders have no horizontal separation. Choose a suitable motion span or different joints.")
    across = shoulder_axis / span
    forward = np.array([-across[1], across[0]])
    yaw = math.radians(args.yaw)
    screen_x = across * math.cos(yaw) + forward * math.sin(yaw)
    origin = np.median(xyz[:, lookup[args.root]][:, [0, 2]], axis=0)
    floor = min(np.quantile(xyz[:, lookup[name], 1], 0.05) for name in args.floor_joints)
    points = xyz[:, [lookup[name] for name in names], :]
    x = (points[:, :, [0, 2]] - origin) @ screen_x
    y = floor - points[:, :, 1]
    return names, np.stack((x, y), axis=-1) * args.scale


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="BVH file with Y up")
    parser.add_argument("output", type=Path, help="Time-series JSON destination")
    parser.add_argument("--start", type=int, default=0, help="First source frame, zero-based")
    parser.add_argument("--end", type=int, help="Last source frame, inclusive")
    parser.add_argument("--fps", type=float, default=60)
    parser.add_argument("--source-fps", type=float, help="Verified source cadence when the BVH header is incorrect")
    parser.add_argument("--yaw", type=float, default=0, help="Camera yaw in degrees from the shoulder line")
    parser.add_argument("--scale", type=float, default=1, help="Canvas units per BVH length unit")
    parser.add_argument("--root", default="Hips")
    parser.add_argument("--shoulders", nargs=2, default=("LeftArm", "RightArm"), metavar=("LEFT", "RIGHT"))
    parser.add_argument("--floor-joints", nargs=2, default=("LeftToeBase", "RightToeBase"), metavar=("LEFT", "RIGHT"))
    parser.add_argument("--joints", help="Comma-separated output joint names. Defaults to all named joints.")
    args = parser.parse_args()
    rates = [args.fps, args.scale]
    if args.source_fps is not None:
        rates.append(args.source_fps)
    if not math.isfinite(args.yaw) or any(not math.isfinite(v) or v <= 0 for v in rates):
        parser.error("FPS and scale must be positive and finite, and yaw must be finite")
    if args.input.resolve() == args.output.resolve():
        parser.error("Use a separate output file to preserve the original BVH")
    try:
        joints, values, step = read_bvh(args.input)
        header_fps = round(1 / step, 3)
        if args.source_fps is not None:
            step = 1 / args.source_fps
        end = len(values) - 1 if args.end is None else args.end
        if not 0 <= args.start <= end < len(values):
            raise ValueError(f"Expected a source range within frames 0–{len(values) - 1}")
        names, xy = project(joints, world_joints(joints, values[args.start:end + 1]), args)
        source_times = np.arange(len(xy)) * step
        sample_count = math.floor(source_times[-1] * args.fps + 1e-8) + 1
        times = np.arange(sample_count) / args.fps
        flat = xy.reshape(len(xy), -1)
        samples = np.column_stack([np.interp(times, source_times, flat[:, i]) for i in range(flat.shape[1])])
        data = {
            "source": args.input.name,
            "bvh_header_fps": header_fps,
            "source_fps": round(1 / step, 3),
            "source_start_frame": args.start,
            "fps": args.fps,
            "joint_names": names,
            "frames": np.round(samples, 2).tolist(),
        }
        args.output.write_text(json.dumps(data, separators=(",", ":")) + "\n")
    except (ValueError, OSError, StopIteration, IndexError) as error:
        parser.error(str(error) or "Unexpected end of BVH hierarchy")


if __name__ == "__main__":
    main()
