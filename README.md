# Jijinglong Skills

Jijinglong 自有技能的统一维护仓库。每个技能独立存放在 `skills/<name>/`，目录名与 `SKILL.md` 的 `name` 一致，不强制作者或品牌前缀。

| 技能                                                                                 | 用途                                                           |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| [ai-video-directing](skills/ai-video-directing/SKILL.md)                             | 将剧本组织成 AI 视频生成段，设计摄影、动作、节奏与首帧。       |
| [character-design](skills/character-design/SKILL.md)                                 | 设计角色身份、定妆板、换装与跨图一致性。                       |
| [seedance-2-5-prompt](skills/seedance-2-5-prompt/SKILL.md)                           | 编写和审查 Seedance 2.5 的提示词与生成方案。                   |
| [tag-character-assets](skills/tag-character-assets/SKILL.md)                         | 按项目字典标注角色素材，并校验候选标签。                       |
| [designing-product-showcase-cards](skills/designing-product-showcase-cards/SKILL.md) | 精选素材并用代码设计产品展示卡片，校准构图、层次与响应式呈现。 |

## 安装与使用

使用 skills CLI 选择要安装的技能：

```bash
npx skills add jijinglong/skills
```

也可以指定技能；Seedance 提示词技能应与导演技能一起安装：

```bash
npx skills add jijinglong/skills --skill ai-video-directing --skill seedance-2-5-prompt
```

`seedance-2-5-prompt` 通过相对路径引用 `ai-video-directing` 的参考资料，使用时应同时安装这两个技能。其他外部技能按各自正文说明使用，不复制第三方技能到本仓库冒充自有技能。

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
