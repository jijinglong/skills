# 标注输出与校验

标注文件与 catalog 是任务产物，放在用户项目约定的位置；未指定时使用本次任务输出目录，不放到技能目录污染后续任务。

## catalog 快照

从项目实际字段与枚举导出，文件名及来源在交付中说明。它是本次校验输入，不替代项目代码。`values: null` 表示开放字符串，缺少 `maxValues` 表示脚本不限制该字段的值数；仅在判定标准明确要求时提供上限。`sources` 可省略，存在时限制来源系统标识。

```json
{
  "fields": {
    "form": { "label": "形态", "values": ["真人", "虚拟"], "maxValues": 1 },
    "art_style": {
      "label": "画风",
      "values": ["写实", "半写实", "二次元", "卡通", "Q版"],
      "maxValues": 1
    },
    "nationality": { "label": "国家", "values": null }
  },
  "sources": ["volcengine", "jimeng"]
}
```

这里仅示例三个字段，实际 catalog 必须覆盖本次任务允许标注的全部字段。不要把来源系统放进 `attributes`，或将已经移除的字段作为兼容别名。

## labels 标注文件

```json
{
  "schemaVersion": 1,
  "catalogRef": "catalog.json",
  "resources": [
    {
      "resourceId": "角色清单中的真实ID",
      "sourceSystem": "volcengine",
      "attributes": { "form": ["虚拟"] },
      "evidence": [
        {
          "field": "form",
          "value": "虚拟",
          "kind": "metadata",
          "ref": "原始清单.json#该ID.provenance",
          "confidence": "high",
          "reason": "来源清单明确此主体为原创虚构角色，而非从外貌判断。"
        }
      ],
      "pending": [
        {
          "field": "art_style",
          "candidates": ["写实", "半写实"],
          "reason": "仅有压缩缩略图，材质与比例边界需要原图复核。"
        }
      ],
      "proposedTerms": [],
      "issues": []
    }
  ]
}
```

- `resourceId` 与输入对应，批内唯一。未知来源省略 `sourceSystem`，可在待核中使用特殊字段 `sourceSystem` 说明缺口。
- `attributes` 只含已确定的字段，值为非空、去重的字符串数组。所有视觉／设定待核的值从属性中省略，不能写空字符串或自造“未知”。完全无法判断时允许空对象，并说明待核。
- `evidence` 每项对应一个已选字段和值，记录实际依据。`kind` 为 `image`、`metadata`、`provided_observation`、`user_confirmation`；不得用不存在的图片引用冒充已看图。`confidence: high` 表示满足当前判定标准，非概率。
- 中置信候选只进 `pending`，其 `candidates` 可省略；候选必须来自对应字段字典。字典未覆盖的词放 `proposedTerms`：包含 `field`、`value`、`reason`，不能写回属性。
- `issues` 记录组内不是同一角色、参考图版本矛盾、缺少原图等输入问题。校验脚本不判断图片真实性，也不核实任意引用是否存在，语义检查仍由执行者完成。
- 可另附创作者易读的表格，但 JSON 是回填候选，不得把解释文案、置信度或待核候选混入业务属性。仅此文件不代表已获写库授权。
