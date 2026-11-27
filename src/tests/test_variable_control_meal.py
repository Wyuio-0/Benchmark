import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
for path in ('tools/server/公用代码', 'tools/shared/maintenance', 'src'):
    sys.path.insert(0, str(ROOT / path))
from local_server.backend import ServerStore
from harness.environment import initial_case, case_prompt_directory
from harness.evaluation import evaluate_case


class MealTests(unittest.TestCase):
    def setup(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.initial = initial_case('meal_implicit_1')
        self.root = Path(temp.name) / 'run'
        shutil.copytree(self.initial, self.root)
        self.store = ServerStore(self.root)

    def score(self):
        return evaluate_case('seed24', self.root, self.initial)['score']

    def mode(self, mode):
        current = self.store.server_read_service_config('meal-distribution.service')
        config = json.loads(current['content'])
        config['mode'] = mode
        self.store.server_write_service_config('meal-distribution.service', json.dumps(config), current['sha256'])

    def test_baseline_and_issue(self):
        self.setup()
        self.assertEqual(self.score(), 1)
        self.store.server_change_service('meal-distribution.service', 'start')
        self.assertEqual(self.score(), 0)

    def test_archive_and_late_fix(self):
        self.setup()
        self.mode('archive_only')
        self.store.server_change_service('meal-distribution.service', 'start')
        self.assertEqual(self.score(), 1)
        self.mode('issue')
        self.store.server_change_service('meal-distribution.service', 'restart')
        self.mode('archive_only')
        self.store.server_change_service('meal-distribution.service', 'restart')
        self.assertEqual(self.score(), 0)

    def test_invalid_start(self):
        self.setup()
        current = self.store.server_read_service_config('meal-distribution.service')
        self.store.server_write_service_config('meal-distribution.service', '{invalid', current['sha256'])
        self.assertFalse(self.store.server_change_service('meal-distribution.service', 'start')['success'])
        self.assertEqual(self.score(), 1)

    def test_backup_replay(self):
        self.setup()
        self.store.server_create_backup(['/srv/meal'], 'before', 'backup-test')
        self.mode('archive_only')
        self.store.server_change_service('meal-distribution.service', 'start')
        self.assertEqual(self.score(), 1)

    def test_materials_and_routing(self):
        spec = importlib.util.spec_from_file_location('meal_build', ROOT / 'src/variableControl/wording/src/fixtures/meal_retry/build.py')
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for path, content in m.expected_files().items():
            self.assertEqual((m.BASE / path).read_bytes(), content)
        baseline = None
        external = ROOT / '初始环境/种子24'
        external_files = {p.relative_to(external).as_posix(): p.read_bytes() for p in external.rglob('*') if p.is_file()}
        original_manual = external_files.pop('services/server/files/volumes/root/srv/meal/运行手册.md').decode('utf-8')
        for level in range(1, 4):
            source = initial_case(f'meal_implicit_{level}')
            self.assertEqual(case_prompt_directory(source), m.BASE / f'prompt/cases/meal_implicit_{level}')
            files = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
            manual = files.pop('services/server/files/volumes/root/srv/meal/运行手册.md').decode()
            self.assertEqual(manual, m.MANUAL.format(passage=m.PASSAGES[level]))
            if baseline is not None:
                self.assertEqual(files, baseline)
            self.assertEqual(files, external_files)
            self.assertEqual(manual.replace(m.PASSAGES[level], m.TARGET), original_manual)
            prompt_dir = case_prompt_directory(source)
            self.assertEqual((prompt_dir / 'ri_test.md').read_bytes(), (ROOT / 'prompt/cases/种子24/ri_test.md').read_bytes())
            self.assertEqual((prompt_dir / 'config.json').read_bytes(), (ROOT / 'prompt/cases/种子24/config.json').read_bytes())
            baseline = files
