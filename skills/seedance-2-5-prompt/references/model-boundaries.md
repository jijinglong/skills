# Seedance 2.5 官方依据与执行边界

核对日期为2026-11-08。当前模型为 `doubao-seedance-2-5-260628`。新任务仅使用2.5，已有真实历史记录保持其原始型号和冻结输入。

- [官方教程](https://console.volcengine.com/ark/region:cn-beijing/docs/seedance-2-5)
- [官方提示词指南与sd25-pe](https://console.volcengine.com/ark/region:cn-beijing/docs/seedance-2-5-prompt-guide)
- [创建任务API](https://docs.volcengine.com/docs/ark/create-video-generation-task-api?lang=zh)
- [模型价格](https://docs.volcengine.com/docs/ark/model-pricing?lang=zh)

## 输入和任务路由

视频4–30秒，`duration=-1`由模型选择。参考图片最多30张；视频最多10段、合计不超过30秒；音频最多10段、单段2–30秒且合计不超过30秒。所有参考合计最多50份。2.5允许纯音频参考。推荐的主体数量、片长属于稳定性建议，不当作接口硬上限。

严格首帧、首尾帧和全模态参考是互斥路由。首帧用 `first_frame`，尾帧用 `last_frame`；严格关键帧不混入参考音视频。全模态用 `reference_image/reference_video/reference_audio`，正文按真实顺序逐份说明职责。需要音色又需要开场状态时走联合参考，不能承诺严格像素锁定。

参考生成使用 `omni_reference_task_type=reference`，允许自行选择画幅和时长。视频编辑使用 `edit`，明确唯一母版和修改范围，固定 `ratio=adaptive,duration=-1`。延长使用 `extend`，固定 `ratio=adaptive`，正文明确向前或向后、原片边界状态和接续动作，时长可选。严格首尾帧的画幅固定 `adaptive`。纯文本中的“编辑”不能替代真实母版附件。

API中的视频输入需要供应商可访问的URL，不能假定支持Base64或本地Cookie链接。执行端须提供受控限时链接。音频、图片可按官方API支持形式传递；仍检查实际请求体、文件格式、大小、分辨率和时长。不能把官方支持误写成当前部署已配置就绪。

## 样片与正式视频

默认 `draft=true,resolution=480p,duration=-1`。Draft的token用量和单价等同普通480p。用户要求升片后才准备独立确认。升片以相同model提交 `content=[{type:"draft_task",draft_task:{id:原样片远端ID}}]`、`resolution=1080p`，draft不传或false。禁止重传prompt、输入素材、duration、ratio、seed、generate_audio、omni_reference_task_type；这些自动复用样片参数。返回尾帧须重新设置 `return_last_frame=true`。

样片ID自供应商 `created_at` 起有效14天（2026-10-28 10:00 UTC+8之前创建的为7天）。本地保存视频不延长远端任务有效期。超过有效期时不能升片，也不能自动重新付费生成样片。视频下载URL另有有效期，应及时保存原片和官方尾帧。

## 计价

2.5 的480p／720p无输入视频刊例价为70元／百万tokens，有输入视频为42元；1080p无输入视频为77元，有输入视频为46元。输入图片和音频不算输入视频。参考视频按输入加输出时长计算，并可能有最低用量，价格不能只乘输出秒数。

样片与升片分别计费。升片是否含输入视频按原样片素材判定，样片本身不额外计入输入视频。预算可用官方5秒16:9无输入视频示例，480p约3.36元，1080p约18.71元；其他画幅、智能实长和输入视频情况另算，最终返回usage优先。费用确认冻结适用档位与价格日期，未知不得记零。按用量测算与实际账单扣款分别理解，不建立手工实付登记。
