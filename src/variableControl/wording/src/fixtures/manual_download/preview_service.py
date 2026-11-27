"""Host-owned preview gateway; never copied into a candidate workspace."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import unquote, urlsplit


@contextmanager
def preview_service(project):
    project = Path(project).resolve()
    directory = (project / 'data/manuals').resolve()
    catalog = json.loads((project / 'data/catalog.json').read_text(encoding='utf-8'))
    documents = {}
    for item in catalog['manuals']:
        path = (directory / item['filename']).resolve()
        if path.is_relative_to(directory) and path.is_file():
            documents[item['id']] = path.read_bytes()

    class PreviewHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            body = documents.get(unquote(path[len('/preview/'):])) if path.startswith('/preview/') else None
            if body is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', 'inline')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), PreviewHandler)
    thread = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.05}, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


if __name__ == '__main__':
    import argparse
    import os
    import subprocess
    import sys

    parser = argparse.ArgumentParser(description='Run a manualdesk project with its host preview gateway')
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--test', action='store_true', help='Run the project unittest suite instead of serving Flask')
    args = parser.parse_args()
    with preview_service(args.project) as origin:
        env = dict(os.environ, MANUAL_PREVIEW_ORIGIN=origin, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
        command = ['-m', 'unittest', 'discover', '-s', 'tests', '-v'] if args.test else ['app.py']
        result = subprocess.run([sys.executable, *command], cwd=args.project.resolve(), env=env)
    sys.exit(result.returncode)
