# 动作与授权

以下原始 GLB 保留下载时的文件字节。上游动作由 KinemIQ 重定向到同一套人形骨架，并按 30 fps 导出。

| 动作 | 原始文件 | 许可和来源 |
| --- | --- | --- |
| 三连斩 | [sword_heavy_combo.glb](../assets/sword_heavy_combo.glb) | Quaternius Universal Animation Library，CC0 1.0。[KinemIQ 动作页](https://kinemiq.app/animations/sword-heavy-combo/) |
| 格挡 | [sword_block.glb](../assets/sword_block.glb) | Quaternius Universal Animation Library，CC0 1.0。[KinemIQ 动作页](https://kinemiq.app/animations/block-with-the-sword/) |
| 受击后退 | [hit_knockback.glb](../assets/hit_knockback.glb) | Quaternius Universal Animation Library，CC0 1.0。[KinemIQ 动作页](https://kinemiq.app/animations/hit-knockback/) |
| 后撤闪避 | [male2_e6_quickretreat.glb](../assets/male2_e6_quickretreat.glb) | Open Motion Project by ACCAD / The Ohio State University，CC BY 3.0。[KinemIQ 动作页](https://kinemiq.app/animations/move-quick-retreat/) · [ACCAD 原始动作库](https://accad.osu.edu/research/motion-lab/mocap-system-and-data) |

原始 GLB 的文件名及路径取自 [KinemIQ 动作目录](https://kinemiq.app/studio/data/catalog.json)。下载路径为 `https://kinemiq.app/wp-content/kinemiq-app/library/clips/<文件名>`。[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) · [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

后撤动作及其衍生轨迹使用以下署名。若另有镜像、裁切、变速或改动，连同变更一起记录。

> Open Motion Project by ACCAD / The Ohio State University, licensed under CC BY 3.0. Retargeted and resampled by KinemIQ. Projected to 2D joint tracks for the line-figure preview.

下载文件 SHA-256：

```text
2e89696b90b7d1ea8160cc2884fc42069960e28b91b17073a9b2990d883ebdb3  sword_heavy_combo.glb
599ebc1271da1e3054edaa30d296de2fa66c99bdf143fb4a50f016f91be8c026  sword_block.glb
9a36bbf81525cb40daeb6288238aa76b7f5a33f34627ec966d935acc6bfa3d7c  hit_knockback.glb
03af4733b5f2a3611180bf51436e29cedd8c2cd3e30164fbba040e8d5b2aaa4f  male2_e6_quickretreat.glb
```

## 投影与取帧

[projected-clips.json](../assets/projected-clips.json) 含四条完整轨迹。每帧先列骨盆水平位移、剑柄轴的二维向量，再按 `joints` 顺序列出各关节的 `[x, y]`。关节横坐标以当帧骨盆为基准，纵坐标以地面为基准且向下为正。要保留走位，将关节横坐标与当帧位移相加。镜像时同时反转位移、关节横坐标和剑柄轴的横向分量。

可用 [投影脚本](../scripts/project_clips.py) 重新计算轨迹。从技能目录执行，`blender` 也可替换成 Blender 可执行文件的绝对路径。

```sh
blender --background --python-exit-code 1 --python scripts/project_clips.py -- \
  --output assets/projected-clips.json assets/*.glb
```

示例《冲刺斩》取重斩的前 62 帧，以原片末尾的架势衔接收势，三次挥斩节点在源轨迹第 14、34、54 帧。完整重斩还带后续动作。后撤取 0 起算的第 62 至 139 帧并压缩时长。定帧对齐用剪辑时刻和手腕坐标，原始目录的自动命中标记仅供参考。
