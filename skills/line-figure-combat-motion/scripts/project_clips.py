"""Project KinemIQ's humanoid GLB clips to line-figure joint tracks in Blender."""
import argparse
import json
import math
import sys
from pathlib import Path

import bpy


SOURCE_FPS = 30
JOINTS = {
    "hip": "pelvis",
    "neck": "neck_01",
    "head": ("Head", "head_leaf", .48),
    "shoulderL": "upperarm_l",
    "elbowL": "lowerarm_l",
    "handL": ("hand_l", "middle_01_l", .56),
    "shoulderR": "upperarm_r",
    "elbowR": "lowerarm_r",
    "handR": ("hand_r", "middle_01_r", .56),
    "kneeL": "calf_l",
    "footL": "foot_l",
    "toeL": "ball_l",
    "kneeR": "calf_r",
    "footR": "foot_r",
    "toeR": "ball_r",
}


def read_clip(path, yaw, ground):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.fps = SOURCE_FPS
    bpy.ops.import_scene.gltf(filepath=str(path))
    armature, = (obj for obj in scene.objects if obj.type == "ARMATURE")
    action = armature.animation_data.action
    # Blender also creates an NLA copy during import. Sample the active action once.
    armature.animation_data.use_nla = False
    start, end = map(round, action.frame_range)

    def bone(name):
        return armature.matrix_world @ armature.pose.bones[name].head

    def horizontal(point):
        return -point.y * math.cos(yaw) + point.x * math.sin(yaw)

    scene.frame_set(start)
    # These exports bake travel in the pelvis and leave the root bone at zero.
    origin = horizontal(bone("pelvis"))
    frames = []
    for frame in range(start, end + 1):
        scene.frame_set(frame)
        root_x = horizontal(bone("pelvis"))
        points = []
        for joint in JOINTS.values():
            point = bone(joint) if isinstance(joint, str) else bone(joint[0]).lerp(bone(joint[1]), joint[2])
            points.extend((horizontal(point) - root_x, ground - point.z))
        # Approximate the hilt axis from the knuckles across the grip.
        blade = bone("thumb_01_r") - bone("pinky_01_r")
        frames.append([round(value, 4) for value in (root_x - origin, horizontal(blade), -blade.z, *points)])
    return frames


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--yaw", type=float, default=24, help="degrees from a pure side view")
    parser.add_argument("--ground", type=float, default=.02, help="floor height in Blender units")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("files", type=Path, nargs="+")
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    clips = {file.stem: read_clip(file.resolve(), math.radians(args.yaw), args.ground) for file in args.files}
    args.output.write_text(json.dumps({"fps": SOURCE_FPS, "joints": list(JOINTS), "clips": clips},
                                      separators=(",", ":")) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
