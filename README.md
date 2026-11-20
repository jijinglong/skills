# Jijinglong Skills

Jijinglong 自有技能、第三方原样收录与注明来源的维护版本仓库。每个技能独立存放在 `skills/<name>/`，目录名与 `SKILL.md` 的 `name` 一致；自有技能不强制作者或品牌前缀，原样收录保留原文，用户授权的迭代版本单独标注名称、版本和来源。

| 技能                                                                                 | 用途                                                           |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| [ai-video-directing](skills/ai-video-directing/SKILL.md)                             | 将剧本组织成 AI 视频生成段，设计摄影、动作、节奏与首帧。       |
| [character-design](skills/character-design/SKILL.md)                                 | 设计角色身份、定妆板、换装与跨图一致性。                       |
| [seedance-2-5-prompt](skills/seedance-2-5-prompt/SKILL.md)                           | 编写和审查 Seedance 2.5 的提示词与生成方案。                   |
| [tag-character-assets](skills/tag-character-assets/SKILL.md)                         | 按项目字典标注角色素材，并校验候选标签。                       |
| [designing-product-showcase-cards](skills/designing-product-showcase-cards/SKILL.md) | 精选素材并用代码设计产品展示卡片，校准构图、层次与响应式呈现。 |
| [scene-generation](skills/scene-generation/SKILL.md)                                 | 从短剧剧情设计场景原画，确认后用 Blender 校正四个视图。        |
| [short-drama-breakdown](skills/short-drama-breakdown/SKILL.md)                       | 测量短剧成片的节奏，拆解开场与集尾，并与自家成片对照。          |

## 安装与使用

第三方来源的维护版本：

| 技能                                                       | 用途                                                                            | 来源                                                                                        |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [video-storyboarding](skills/video-storyboarding/SKILL.md) | 视频分镜设计：从创意或剧本到镜头、生成段和视频提示词，主要适用于 Seedance 2.0。 | 基于 FilmPromptDirector 1.0.0 重新整理的1.1.0维护版，见[来源记录](THIRD_PARTY_NOTICES.md)。 |

```bash
npx skills add jijinglong/skills --skill video-storyboarding
```

使用 skills CLI 选择要安装的技能：

```bash
npx skills add jijinglong/skills
```

也可以指定技能；Seedance 提示词技能应与导演技能一起安装：

```bash
npx skills add jijinglong/skills --skill ai-video-directing --skill seedance-2-5-prompt
```

`seedance-2-5-prompt` 通过相对路径引用 `ai-video-directing` 的参考资料，使用时应同时安装这两个技能。其他外部技能按各自正文说明使用，不复制第三方技能到本仓库冒充自有技能。

`short-drama-breakdown` 使用 FFmpeg 和 FFprobe 测量成片。需要把拆解结果纳入短剧创作项目时，按技能说明与 `short-drama-develop` 等技能配合使用。

角色素材标注脚本的现有测试可在仓库根目录运行：

```bash
python3 -B -m unittest discover -s skills/tag-character-assets/tests -v
```

## 维护与迁移

在本仓库维护技能源文件。本地开发可将客户端的技能安装目录链接到 `skills/<name>`，修改源文件后由新会话读取。更新名称时同步修改目录、frontmatter、调用示例、UI 元数据和技能之间的引用；同一安装目标出现同名技能时先核对来源，不覆盖未知内容。

前四个创作技能由原先的 `jjl-` 名称迁移而来，使用无前缀名称；创作规则和脚本逻辑保持原意。

产品展示卡片技能可单独安装，无额外技能依赖，也不附带项目私有图片：

```bash
npx skills add jijinglong/skills --skill designing-product-showcase-cards
```

调用示例：`使用 $designing-product-showcase-cards，为当前页面精选素材并实现产品展示卡片，检查桌面和手机效果。`

视频分镜设计1.1.0将主入口从673行整理为91行，摄影、素材、提示词、审核和示例按需读取。原始1.0.0保留在来源提交和本机备份中，当前安装使用 `$video-storyboarding`；不保留同一维护版本的新旧重复入口。
