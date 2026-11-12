# 来源与取舍

核对日期2026-11-05。以下是重新编写的方法整合，没有捆绑或安装第三方实现，也没有实际运行它们的生图流程证明效果；技能可离线使用，不要求每次重新查网页。

| 来源及核对版本 | 实际读取 | 吸收 | 未采用 |
| --- | --- | --- | --- |
| [Saeyeon-developer / character-design-sheet](https://github.com/Saeyeon-developer/character-design-sheet/tree/09294c75c8a589f0f877d2a4bce3ac8117cedfee) | `skills/content/character-sheet/SKILL.md`、`character-sheet-simple/SKILL.md`、前者`references/prompt-guide.md` | 参考分工、整板一次生成、真实图复核、真人板简洁呈现 | 30/30/40三格；表情色卡标签；默认局部编辑 |
| [fal-ai-community / character-design](https://github.com/fal-ai-community/skills/tree/9ca850412943251fc9a466c4c29fdaf7a303a3d8/skills/character-design) | `SKILL.md`、`references/anchor-system.md`、`references/prompt-patterns.md` | 身份锚点与变化分离、图像参考、真实schema | 自动模型路由、genmedia及付费视频链路；永久锁所有衣服发式 |
| [byron-public / game-character-consistency](https://github.com/byron-public/grok-build-skills/blob/78f7974d4550b784347ca74e3c423ba373abc350/skills/game-character-consistency/SKILL.md) | 该`SKILL.md` | 左右映射、严格侧视、手物接触、状态连续性 | Grok专用调用、最近变体连续派生 |
| [Comfy：Character turnaround](https://comfy.org/hub/workflows/character-turnaround/) | 页面及内嵌工作流参数 | 单人参考派生多角度与脸部特写 | 付费云依赖、四角度／额外脸格、独立生成后拼接、节点强制出图指令 |
| [Riot：Clarity in League](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) | Silhouettes和换装章节 | 主次特征层级、换装保留身份 | 游戏形体与武器不能直接替代真人脸部设计 |
| [OpenAI：Image prompting](https://developers.openai.com/api/docs/guides/image-prompting#keep-a-character-consistent) | 一致性及参考分工示例 | 可复用身份图，后续实际传入并重复关键比例 | 示例故事、具体模型与参数不成为默认值 |

本地方法还吸收了`short-drama-assets`的身份／变体／镜头瞬态分层，`short-drama-image-prompts`的完整可复制正文与参考控制范围，以及`producing-character-short-video-assets`的身份、造型连续性思路。这些是方法来源，不是运行时强制安装依赖。

本技能自定部分：全角色差异表、每人3个主锚点、拆分群体身份、同母版单层派生、16:9和2560×1440目标、五视图2:1与右侧1:1、1像素白线、完整重生成、真实尺寸与选用状态、低上下文负担。它们是用户约定，优先于外部默认值；用户后续调整时按新要求更新。
