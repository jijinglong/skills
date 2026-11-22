---
name: video-matting
description: 为已有视频抠出人物或物体，移除或替换背景，导出透明前景、蒙版或合成预览。用户提到视频抠像、人物去背景、视频换背景、透明 MOV、Apple Vision 实例蒙版或 MatAnyone 2 时使用。
---

# 视频抠像与换背景

先确认要保留的主体和交付物。画面有几个人、是否保留手持物和衣摆、透明前景是否需要复用，都会影响蒙版。根据素材和已有上下文做可逆决定。用户只给视频且要抠像时，交付带 Alpha 的前景，并用中性纯色预览检查边缘。用户指定新背景时，用指定背景合成。

## 选方法

| 方法 | 适用情况 | 怎么用 |
| --- | --- | --- |
| Apple Vision 的 VNGenerateForegroundInstanceMaskRequest | Mac 本地处理；显著人物、物体或需要一起保留的多个前景实例 | 逐帧生成实例蒙版，选择所需实例并输出与输入画面等大的灰度蒙版。可直接合成，也可给 MatAnyone 2 提供起始蒙版。[本地工具和用法](references/apple-vision.md) |
| Apple Vision 的 VNGeneratePersonSegmentationRequest | 只抠人物，画面中的可见人物可以一起处理 | 生成语义人物蒙版。需要区分几个人或保留帽子、手持物等易掉的结构时，试前景实例蒙版，并检查输出是否保留所需区域。 |
| MatAnyone 2 | 指定人物，需要连续跟踪和细边缘 | 用一张正确的起始蒙版初始化。可从 Apple Vision 或交互分割获得，也可复用已复核的蒙版。模型的默认 CLI 输出前景预览和 Alpha 蒙版，合成时使用原视频颜色与 Alpha。[官方仓库](https://github.com/pq-yang/MatAnyone2) · [非商业使用许可](https://github.com/pq-yang/MatAnyone2/blob/main/LICENSE.txt) |
| 剪映 / CapCut | 快速换背景、在同一剪辑工程直接交付 | 尝试自动抠像后把新背景放在下层。均匀绿幕或蓝幕优先用色度抠图，检查衣服同色与溢色。[官方换背景说明](https://www.capcut.com/tools/video-background-changer) |
| After Effects Object Matte / Roto Brush | 多人交叉、严重遮挡，或需要手动补轮廓和精修边缘 | 选中目标，分段传播，修补漏选和粘连。复杂边缘用 Refine Edge，复核并冻结后导出。[Adobe 官方说明](https://helpx.adobe.com/after-effects/desktop/roto-brush-and-refine-matte/roto-brush/object-matte.html) |

优先复用可运行的本地工具。MatAnyone 2 已安装时核对可执行入口、设备和输出尺寸；Apple Silicon 可测试 PyTorch MPS。比较模型用原片最难的几秒，在计划使用的背景上看结果。已明确要处理整条视频时，试跑只用于选方案，随后继续处理全片。

## 沿时间轴处理

1. 用 FFprobe 或编辑器查看帧率、时间戳、旋转、画幅、音轨和时长。识别真正的切镜、急转、相互遮挡与淡出，按需要分段。统一解码方向，保证 RGB 与蒙版逐帧对齐。
2. 选主体完整可见的关键帧做蒙版。Apple Vision 可处理逐帧前景，也可只补几个关键帧。实例编号按帧解释，指定同一主体时按位置、外观和遮挡关系重新关联。
3. 两个人交叉或大幅转身后，检查先前没入画的脸、帽子、手和脚。跟踪遗漏时，在主体清楚的帧重新初始化，或沿用该段已验证的逐帧蒙版。过渡放在两个蒙版均正确的帧里，避免缺失轮廓逐渐淡入。轻微抖动可对齐相邻帧后再平滑；快速运动处直接平均可能拖影。
4. 检查原片淡出在新背景上应保留成怎样的效果。需要淡出至透明时，让 Alpha 随原有时序渐退，并检查最终帧。合成用原帧颜色和灰度 Alpha，检查半透明边缘是否混入旧背景。

## 导出与复核

- 透明母版导出 ProRes 4444 MOV 并启用 RGB + Alpha，或交付带 Alpha 的 PNG 序列。用 FFprobe 确认像素格式含 Alpha，再实际提取 Alpha 或叠到背景检查，避免只凭扩展名判断。MP4 常规预览用新背景合成后导出。
- 核对视频尺寸、方向、时长、帧数或时间戳，确认原音轨按需求保留且同步。若无须改声且封装兼容，直接复制音轨。重点看片头、变形最快处、两人交叉处和片尾。
- 遵守项目现有的素材和版本目录。记录实际使用的工具或模型、输入蒙版和重新初始化的帧或时码、选用的输出版本。发布前只把用户选定的素材移入交付目录。
