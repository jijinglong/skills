# PixelFX 工具和导出

## 从已有素材开始

在 PixelFX 源码根目录运行命令。CLI 使用 Node.js 18 或更新版本。只有 GIF 或 MP4 预览使用 FFmpeg。优先使用项目已有的源码版本。Beat 中可浏览 `assets/pixelfx/sheets/index.json`，原始工具在 `assets/pixelfx/pixelfx-source.zip`；解压产生的源码目录适合在临时目录或项目的工作目录使用。缺少本地副本时，从官方仓库取得，并记录所用提交。

```bash
node tools/list.mjs campfire
node tools/serve.mjs
```

第一条按名称、标签和描述找效果。第二条启动本地 Canvas 图库，默认打开 `http://localhost:8080/gallery/`。

## 改现有特效

例如把 `fire/campfire` 改成蓝色，保持原来的 3 秒循环与木柴颜色。下面命令输出 `records/fire/campfire/` 下的帧图、透明图集和 JSON。需要换种子或帧率时可增加 `--seed` 或 `--fps`。不同变体用 `--out` 指定不同的目录，最终稿保留实际运行参数。

```bash
node tools/render.mjs fire/campfire --bg none --sheet \
  --opts '{"palette":["#0d1730","#12396b","#1765a7","#38a9e6","#8eeaff","#e9fcff","#ffffff"]}'
node tools/check.mjs fire/campfire
```

`check.mjs` 检查源码默认配置，例如出界、循环接缝和随机种子。对自定义色板、种子或帧率，打开这次实际渲染的预览，按 JSON 的顺序和时长播放，或用相同参数加 `--gif` 或 `--mp4` 看运动。

## 写新效果或招式

- 新效果可用 `node tools/new.mjs arcane/moon-ring --loop` 起稿。该命令创建 `src/fx/arcane/moon-ring.js`。实现后用 `node tools/render.mjs arcane/moon-ring` 生成帧图。需要在 Gallery 中出现时检查 `src/fx/index.js` 的注册。
- 常规效果提供 `meta`。无状态效果用 `draw(p, t, o)`，需要积分或碰撞时用 `create(o)` 返回 `update(dt)` 与 `draw(p)`。后景用 `drawBack`。模拟由运行时以 120 Hz 或更细的步长推进，随机数用 `o.seed` 初始化。确认 `meta.size`、`origin`、`duration`、`fps` 和 `loop` 都符合交付。
- 角色演出参考 `src/fx/melee/sword-slash.js`。用 `act.poses` 写姿势，负时间表示特效开始前的预备，`act.hits` 控制命中停顿和反应。常规姿势以 12 fps 步进，粒子用独立时间步模拟。命中停顿由演出时间轴处理。贴身变色或描边要核查 `onBody` 和角色遮罩。多段招式参考 `src/fx/moves/dash-strike.js`，用 `chain` 组合已有特效并对齐同一命中节拍。

## 选导出工具

| 交付 | 命令 | 结果 |
| --- | --- | --- |
| 单个基础特效 | `node tools/render.mjs fire/campfire --sheet` | `records/fire/campfire/` 中的透明 PNG、Aseprite 风格帧数据和帧图预览。 |
| 全库基础特效 | `node tools/sheets.mjs` | `sheets/` 下分类图集与索引。 |
| 演出预览 | `node tools/act.mjs moves/dash-strike` | `records/act/moves-dash-strike.png`，按时间排列的姿势预览。加 `--mp4` 可查看运动。 |
| 带角色的透明图集 | `node tools/act.mjs moves/dash-strike --sheet` | `records/act/` 中的 `moves-dash-strike.sheet.png` 和对应 `.sheet.json`。省去受击目标时可加 `--no-target`。 |

**检查演出图集的图片引用。** 已验证的上游版本有一处命名差异。`act.mjs --sheet` 输出 `moves-dash-strike.sheet.png`，但 `meta.image` 是 `dash-strike.png`。交付时可把图与 JSON 一同整理成 `dash-strike.png`、`dash-strike.json`，也可保留输出名并修改 JSON 的 `meta.image`。确认把两份文件一起移动到另一目录后仍能解析。这个版本的 `act.mjs --sheet` 固定输出到 `records/act/`，生成后再整理到交付目录。

游戏内播放时采用 `meta.pixelfx.pivot` 和图集帧矩形，检查坐标约定、最近邻过滤和导入器实际回放。手动切片时按 JSON 的帧顺序播放，有效帧数以 JSON 为准。精确的恒定帧率时长用帧数除以 `meta.pixelfx.fps`，因为 JSON 的逐帧毫秒数经过取整。演出图集通过采样帧序列体现停顿，实时游戏的全局停顿仍由游戏状态处理。用户需要整段视频预览时，可单独导出 GIF 或 MP4。

## 来源

这套方法参考 Patch 的 PixelFX 与 Hugo Duprez 的代码绘制实践。上面的命令和演出命名差异以源码提交 `5294518ce7c72e48b6100a744596e0acf57f2826` 为准。使用其他版本时核对工具参数及输出。复制或改用现有效果时保留上游要求的版权和许可信息。 [PixelFX 源码](https://github.com/patch-gg/pixelfx/tree/5294518ce7c72e48b6100a744596e0acf57f2826) · [编写特效](https://github.com/patch-gg/pixelfx/blob/5294518ce7c72e48b6100a744596e0acf57f2826/docs/AUTHORING.md) · [Hugo 的制作方法](https://www.spritefusion.com/blog/how-to-make-good-pixel-art-effects-with-claude)
