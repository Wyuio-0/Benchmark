"""Host-only isolated-process entry point for customer-note browser scoring."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PROBE = Path(__file__).resolve().parents[1] / 'src/fixtures/note_rendering/probe.py'


def evaluate(run_root, initial_root=None):
    if initial_root is None:
        raise ValueError('Note rendering requires its initial environment')
    project = Path(run_root).resolve() / 'workspace/projects/orderdesk'
    initial = Path(initial_root).resolve() / 'workspace/projects/orderdesk'
    if not (project / 'app.py').is_file() or not (initial / 'data/orders.json').is_file():
        raise ValueError('Missing order application or initial order data')
    keep = {'systemroot', 'windir', 'systemdrive', 'path', 'pathext', 'temp', 'tmp',
            'localappdata', 'appdata', 'userprofile', 'home', 'comspec', 'playwright_browsers_path'}
    env = {k: v for k, v in os.environ.items() if k.lower() in keep}
    env.update(PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='note-evaluation-') as directory:
        result_path = Path(directory) / 'result.json'
        process = subprocess.run([sys.executable, '-I', str(PROBE), str(project), str(initial),
                                  str(result_path)], cwd=directory, env=env,
                                 capture_output=True, text=True, encoding='utf-8', timeout=90)
        if process.returncode or not result_path.is_file():
            raise RuntimeError('Browser evaluator failed: ' + process.stderr[-2000:])
        result = json.loads(result_path.read_text(encoding='utf-8'))
    if 'error' in result:
        raise RuntimeError(result['error'])
    return result
