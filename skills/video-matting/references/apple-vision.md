# 用 Apple Vision 取前景实例蒙版

适用于 macOS 14 或更新版本的本地处理。需要 Swift 工具链；拆帧与封装示例还需要 FFmpeg。脚本只处理已经摆正方向的 PNG 帧。每一帧调用 VNGenerateForegroundInstanceMaskRequest，取 VNInstanceMaskObservation 的 allInstances 并用 generateScaledMaskForImage(forInstances:from:) 获取原尺寸灰度蒙版。它会合并所有检测到的显著前景，空检测写黑色蒙版并在终端标记对应帧，便于排查漏检。[Apple 前景实例 API](https://developer.apple.com/documentation/vision/vngenerateforegroundinstancemaskrequest) · [Apple 原尺寸蒙版 API](https://developer.apple.com/documentation/vision/vninstancemaskobservation/generatescaledmaskforimage(forinstances:from:))

## 快速验证

以下命令从技能目录运行。例子使用横竖方向已能正常解码、方形像素、恒定 30 fps 的视频。输入和输出路径按项目替换。

~~~bash
scratch=$(mktemp -d)
mkdir "$scratch/frames"
swiftc -O scripts/foreground-masks.swift -o "$scratch/foreground-masks"
ffmpeg -i input.mp4 -map 0:v:0 -fps_mode passthrough -start_number 0 \
  "$scratch/frames/%06d.png"
"$scratch/foreground-masks" "$scratch/frames" "$scratch/alpha"
ffmpeg -i input.mp4 -framerate 30 -start_number 0 -i "$scratch/alpha/%06d.png" \
  -filter_complex '[0:v:0][1:v:0]alphamerge[out]' -map '[out]' -map '0:a:0?' \
  -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le -c:a copy transparent.mov
~~~

先对短片段查看原帧和蒙版，核对帧数、同名文件、实际帧率、画幅和主体。29.97 fps 的素材应使用准确分数，例如 30000/1001。可变帧率素材应保留源时间戳，或先生成固定帧率工作副本并用它同时做取帧与合成。若音频不能直接封装到 MOV，再选兼容编码。原尺寸 Alpha 要拿灰度蒙版，instanceMask 本身保存的是实例标签。

## 只留指定主体或修复漏检

- 多个实例都要保留且背景足够明确时，可直接使用脚本结果。只留某一个或几个实例时，按位置核对标签，给 generateScaledMaskForImage 传所需的 IndexSet。跨帧根据位置、姿态和外观复核，尤其是入画、出画、遮挡与切镜。连续追踪也可交给接受起始蒙版的模型。
- 某帧无人但原片应有人时，应补蒙版或重新初始化。若演员在开头横向入画，模型可能误认肢体。可在校正姿态后的工作画面生成蒙版并用同一空间变换映回原画，或选回正后外形清楚的帧重新初始化。
- 只用 Apple Vision 给 MatAnyone 2 制作起始蒙版时，确认保留人物的整个可见轮廓，包括帽檐或衣摆。给模型传与起始帧同尺寸的二值蒙版。最后合成仍使用逐帧估计的灰度 Alpha，保留柔和边缘。
