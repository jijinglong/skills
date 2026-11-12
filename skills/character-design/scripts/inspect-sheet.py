#!/usr/bin/env python3
"""Read PNG facts without modifying pixels; no visual or identity verdict."""

import argparse
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path


def inspect_png(path: Path) -> dict:
    with path.open('rb') as stream:
        header = stream.read(33)
        if len(header) != 33 or header[:8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('仅支持PNG原始文件；该文件不是有效PNG头')
        if struct.unpack('>I', header[8:12])[0] != 13 or header[12:16] != b'IHDR':
            raise ValueError('PNG缺少标准IHDR')
        if zlib.crc32(header[12:29]) & 0xffffffff != struct.unpack('>I', header[29:33])[0]:
            raise ValueError('PNG头校验失败')
        width, height = struct.unpack('>II', header[16:24])
        if not width or not height:
            raise ValueError('PNG宽高无效')
        digest = hashlib.sha256()
        digest.update(header)
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return {
        'path': str(path.resolve()), 'format': 'PNG',
        'targetWidth': 2560, 'targetHeight': 1440,
        'actualWidth': width, 'actualHeight': height,
        'matchesTargetPixels': (width, height) == (2560, 1440),
        'exact16to9': width * 9 == height * 16,
        'relativeAspectError': abs(width * 9 / (height * 16) - 1),
        'sha256': digest.hexdigest(),
        'visualReview': '未核实；脚本不判断脸、服装、布局、分割线或完整图像解码',
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    args = parser.parse_args()
    try:
        report = inspect_png(args.image)
    except (OSError, ValueError, struct.error) as error:
        print(f'检查失败：{error}', file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
