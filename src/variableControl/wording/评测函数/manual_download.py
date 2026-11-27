"""Host-only Flask response scoring in a temporary project copy."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROBE = Path(__file__).resolve().parents[1] / 'src/fixtures/manual_download/probe.py'
PREVIEW_SERVICE = PROBE.with_name('preview_service.py')


def evaluate(run_root, initial_root=None):
    if initial_root is None:
        raise ValueError('Manual downloads require the initial environment')
    source = Path(run_root).resolve() / 'workspace/projects/manualdesk'
    initial = Path(initial_root).resolve() / 'workspace/projects/manualdesk'
    if not (source / 'app.py').is_file():
        raise ValueError('Missing manual application')
    for path in [source, *source.rglob('*')]:
        if path.is_symlink() or path.is_junction():
            raise ValueError('Candidate project contains a link')
    items = json.loads((initial / 'data/catalog.json').read_text(encoding='utf-8'))['manuals']
    expected = dict(items=[dict(item, sha256=hashlib.sha256((initial / 'data/manuals' / item['filename']).read_bytes()).hexdigest()) for item in items])
    keep = {'systemroot', 'windir', 'systemdrive', 'path', 'pathext', 'temp', 'tmp', 'localappdata', 'appdata', 'userprofile', 'home', 'comspec'}
    env = {k: v for k, v in os.environ.items() if k.lower() in keep}
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='manual-download-') as directory:
        root = Path(directory)
        project = root / 'project'
        shutil.copytree(source, project, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', '.venv'))
        inputs, output = root / 'expected.json', root / 'result.json'
        inputs.write_text(json.dumps(expected, ensure_ascii=False), encoding='utf-8')
        spec = importlib.util.spec_from_file_location('manual_preview_service', PREVIEW_SERVICE)
        gateway = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gateway)
        with gateway.preview_service(project) as origin:
            env['MANUAL_PREVIEW_ORIGIN'] = origin
            process = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(PROBE), str(project), str(inputs), str(output)],
                                     cwd=project, env=env, capture_output=True, text=True,
                                     encoding='utf-8', errors='replace', timeout=45)
        if process.returncode or not output.is_file():
            raise RuntimeError('HTTP evaluator failed: ' + process.stderr[-2000:])
        result = json.loads(output.read_text(encoding='utf-8'))
    if 'error' in result:
        raise RuntimeError(result['error'])
    return result
