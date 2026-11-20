# 锁画面的 FFmpeg 封装与验证

先读取源成片的音视频、字幕和其他流。以下示例用于普通 MP4，视频从时间零点开始，只有一条需要替换的成片音轨，字幕已烧录。`mix-aligned.wav` 已按视频实际时长对齐、完成混音并核对响度。其他容器、非零起始时码、独立字幕或需保留的流按实际输入调整映射和封装格式。

```bash
ffprobe -v error -show_streams -show_format -of json edit-v01.mp4
ffmpeg -n -i edit-v01.mp4 -i mix-aligned.wav \
  -map 0:v:0 -map 1:a:0 -map_metadata 0 -map_chapters 0 \
  -c:v copy -c:a aac -b:a 256k -movflags +faststart edit-v02.mp4
ffprobe -v error -show_streams -show_format -of json edit-v02.mp4
```

视频直接复制。混音应在封装前对齐和裁齐，避免临时以较短的音轨截断最后一帧。AAC 可能有编码延迟和尾部填充，以播放器时间轴和实际声画为准。若需确认视频编码数据与时码，可对两版运行下列命令并比较。容器发生时间基调整时用 `pts_time`、`dts_time` 比较实际时刻；遇到流不匹配先检查映射。

```bash
ffprobe -v error -select_streams v:0 -show_packets -show_data_hash sha256 \
  -show_entries packet=pts_time,dts_time,duration_time,data_hash -of csv=p=0 edit-v02.mp4
```

核对输出的画幅、总帧数、画面起止、字幕和音轨。在第一处开口、快速音节、每个换句切点和尾音处逐一听看。另存本次采用的无损混音，便于下一版复用。
