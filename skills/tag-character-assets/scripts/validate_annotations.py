#!/usr/bin/env python3
"""Read-only validation of character annotation manifests against a supplied catalog."""
import argparse
import json
import sys
from pathlib import Path


def text(value):
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def validate(data, catalog):
    errors = []
    if not isinstance(catalog, dict) or not isinstance(catalog.get('fields'), dict):
        return ['catalog.fields 必须为对象']
    fields = catalog['fields']
    for name, rule in fields.items():
        if not text(name) or not isinstance(rule, dict) or 'values' not in rule:
            errors.append(f'字典字段 {name!r} 缺少 values 配置')
            continue
        values = rule['values']
        if values is not None and (not isinstance(values, list) or not values or not all(text(v) for v in values)):
            errors.append(f'字典字段 {name!r} 的 values 必须为非空字符串数组或 null')
        maximum = rule.get('maxValues')
        if maximum is not None and (type(maximum) is not int or maximum < 1):
            errors.append(f'字典字段 {name!r} 的 maxValues 必须为正整数')
    sources = catalog.get('sources')
    if sources is not None and (not isinstance(sources, list) or not all(text(v) for v in sources)):
        errors.append('catalog.sources 必须为字符串数组')
    if errors:
        return errors
    if not isinstance(data, dict):
        return ['标注文件必须为对象']
    if type(data.get('schemaVersion')) is not int or data['schemaVersion'] != 1:
        errors.append('schemaVersion 必须为 1')
    if not text(data.get('catalogRef')):
        errors.append('缺少 catalogRef')
    resources = data.get('resources')
    if not isinstance(resources, list) or not resources:
        return errors + ['resources 必须为非空数组']
    seen = set()
    for index, row in enumerate(resources):
        prefix = f'resources[{index}]'
        if not isinstance(row, dict):
            errors.append(f'{prefix} 必须为对象')
            continue
        resource_id = row.get('resourceId')
        if not text(resource_id):
            errors.append(f'{prefix} 缺少有效 resourceId')
        elif resource_id in seen:
            errors.append(f'{prefix} 资源ID重复: {resource_id}')
        else:
            seen.add(resource_id)
        if 'sourceSystem' in row:
            source = row['sourceSystem']
            if not text(source) or (sources is not None and source not in sources):
                errors.append(f'{prefix} 来源不在字典或无有效来源标识')
        attributes = row.get('attributes')
        if not isinstance(attributes, dict):
            errors.append(f'{prefix}.attributes 必须为对象')
            attributes = {}
        assigned = set()
        for field, values in attributes.items():
            path = f'{prefix}.attributes.{field}'
            if field not in fields:
                errors.append(f'{path} 未知字段')
                continue
            if not isinstance(values, list) or not values:
                errors.append(f'{path} 必须为非空数组；未知字段应省略')
                continue
            maximum = fields[field].get("maxValues")
            if maximum is not None and len(values) > maximum:
                errors.append(f"{path} 最多 {maximum} 个值")
            selected = set()
            allowed = fields[field]['values']
            for value in values:
                if not text(value) or len(value) > 120:
                    errors.append(f'{path} 含空值、非规范字符串或超长值')
                    continue
                if value in selected:
                    errors.append(f'{path} 含重复值: {value}')
                selected.add(value)
                if allowed is not None and value not in allowed:
                    errors.append(f'{path} 值不在字典: {value}')
                assigned.add((field, value))
        evidence = row.get('evidence')
        supported = set()
        if not isinstance(evidence, list):
            errors.append(f'{prefix}.evidence 必须为数组')
            evidence = []
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(f'{prefix}.evidence 的条目必须为对象')
                continue
            field, value = item.get('field'), item.get('value')
            if not text(field) or not text(value) or (field, value) not in assigned:
                errors.append(f'{prefix}.evidence 引用了未赋值的标签')
                continue
            if item.get('confidence') != 'high':
                errors.append(f'{prefix}.{field} 赋值须有高置信证据，中低置信仅列待核')
                continue
            if item.get('kind') not in ('image', 'metadata', 'provided_observation', 'user_confirmation'):
                errors.append(f'{prefix}.{field} 依据类型无效')
                continue
            if not text(item.get('ref')) or not text(item.get('reason')):
                errors.append(f'{prefix}.{field} 缺少依据引用或理由')
                continue
            supported.add((field, value))
        for field, value in sorted(assigned - supported):
            errors.append(f'{prefix}.{field}={value} 缺少高置信证据')
        for collection in ('pending', 'proposedTerms'):
            items = row.get(collection, [])
            if not isinstance(items, list):
                errors.append(f'{prefix}.{collection} 必须为数组')
                continue
            for item in items:
                if not isinstance(item, dict):
                    errors.append(f'{prefix}.{collection} 的条目必须为对象')
                    continue
                field = item.get('field')
                if not isinstance(field, str) or (field not in fields and not (collection == 'pending' and field == 'sourceSystem')):
                    errors.append(f'{prefix}.{collection} 未知字段')
                    continue
                if not text(item.get('reason')):
                    errors.append(f'{prefix}.{collection}.{field} 缺少理由')
                if collection == 'proposedTerms':
                    if not text(item.get('value')):
                        errors.append(f'{prefix}.proposedTerms.{field} 缺少新词')
                    continue
                candidates = item.get('candidates', [])
                if not isinstance(candidates, list):
                    errors.append(f'{prefix}.pending.{field} 的 candidates 必须为数组')
                    continue
                allowed = sources if field == 'sourceSystem' else fields[field]['values']
                for candidate in candidates:
                    if not text(candidate) or (allowed is not None and candidate not in allowed):
                        errors.append(f'{prefix}.pending.{field} 候选不在字典: {candidate!r}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('annotations', type=Path)
    parser.add_argument('--catalog', required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.annotations.read_text(encoding='utf-8'))
        catalog = json.loads(args.catalog.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f'读取标注或字典失败: {error}', file=sys.stderr)
        return 1
    errors = validate(data, catalog)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    total = len(data['resources'])
    assigned = sum(len(values) for row in data['resources'] for values in row['attributes'].values())
    print(f'校验通过: {total} 项资源，{assigned} 个标签。仍需按项目标准核对语义与证据真实性。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
