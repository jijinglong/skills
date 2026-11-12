import copy
import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'validate_annotations.py'
SPEC = importlib.util.spec_from_file_location('validator', SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class AnnotationValidationTests(unittest.TestCase):
    def setUp(self):
        self.catalog = {'fields': {
            'form': {'values': ['真人', '虚拟'], 'maxValues': 1},
            'genre': {'values': ['医疗', '科幻']},
            'nationality': {'values': None},
        }, 'sources': ['volcengine', 'jimeng']}
        self.data = {'schemaVersion': 1, 'catalogRef': 'catalog.json', 'resources': [{
            'resourceId': 'asset-1', 'sourceSystem': 'volcengine',
            'attributes': {'form': ['虚拟']},
            'evidence': [{'field': 'form', 'value': '虚拟', 'kind': 'metadata',
                          'ref': 'manifest.json#asset-1', 'confidence': 'high',
                          'reason': '明确的原创虚构人物来源'}],
            'pending': [],
        }]}

    def errors(self):
        return validator.validate(self.data, self.catalog)

    def test_valid_annotations_and_open_country(self):
        row = self.data['resources'][0]
        row['attributes']['nationality'] = ['来源明确的新国家']
        row['evidence'].append({'field': 'nationality', 'value': '来源明确的新国家',
                               'kind': 'user_confirmation', 'ref': 'creator-note',
                               'confidence': 'high', 'reason': '创作者明确国家设定'})
        self.assertEqual(self.errors(), [])

    def test_unknown_field_and_out_of_vocabulary_are_rejected(self):
        row = self.data['resources'][0]
        row['attributes'].update({'portrait_type': ['虚拟写实'], 'form': ['AI人']})
        self.assertTrue(any('未知字段' in error for error in self.errors()))
        self.assertTrue(any('不在字典' in error for error in self.errors()))

    def test_no_missing_evidence_or_medium_confidence_in_attributes(self):
        self.data['resources'][0]['evidence'] = []
        self.assertTrue(any('缺少高置信证据' in error for error in self.errors()))
        self.data['resources'][0]['evidence'] = [{'field': 'form', 'value': '虚拟',
            'kind': 'image', 'ref': 'view.png', 'confidence': 'medium', 'reason': '边界不清'}]
        self.assertTrue(any('高置信' in error for error in self.errors()))

    def test_duplicates_empty_values_and_cardinality_are_rejected(self):
        self.data['resources'][0]['attributes']['form'] = ['真人', '虚拟', '虚拟', '']
        errors = self.errors()
        self.assertTrue(any('重复' in error for error in errors))
        self.assertTrue(any('空值' in error for error in errors))
        self.assertTrue(any('最多' in error for error in errors))

    def test_pending_and_proposed_terms_do_not_need_to_be_assigned(self):
        row = self.data['resources'][0]
        row['pending'] = [{'field': 'genre', 'candidates': ['科幻'], 'reason': '需要原图'}]
        row['proposedTerms'] = [{'field': 'genre', 'value': '乡村', 'reason': '当前字典未覆盖'}]
        self.assertEqual(self.errors(), [])
        row['pending'][0]['candidates'] = ['乡村']
        self.assertTrue(any('候选不在字典' in error for error in self.errors()))

    def test_duplicate_resources_and_unknown_sources_are_rejected(self):
        self.data['resources'].append(copy.deepcopy(self.data['resources'][0]))
        self.data['resources'][0]['sourceSystem'] = 'guessed-source'
        self.assertTrue(any('资源ID重复' in error for error in self.errors()))
        self.assertTrue(any('来源不在字典' in error for error in self.errors()))

    def test_non_objects_and_bad_evidence_are_reported_without_crash(self):
        self.assertTrue(validator.validate([], self.catalog))
        self.assertTrue(validator.validate(self.data, []))
        self.data['resources'][0]['evidence'] = [False]
        self.assertTrue(self.errors())

    def test_unknowns_can_stay_unassigned(self):
        row = self.data['resources'][0]
        row.pop('sourceSystem')
        row['attributes'] = {}
        row['evidence'] = []
        row['pending'] = [{'field': 'sourceSystem', 'reason': '缺少来源说明'}]
        self.assertEqual(self.errors(), [])


if __name__ == '__main__':
    unittest.main()
