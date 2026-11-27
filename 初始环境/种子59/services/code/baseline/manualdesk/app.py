import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen
from flask import Flask, Response, abort, render_template, request, send_file
from manualdesk.catalog import Catalog
from manualdesk.paths import MANUALS_DIR, resolve_manual_path


def create_app():
    app = Flask(__name__)
    catalog = Catalog(Path(__file__).parent / 'data/catalog.json')

    @app.before_request
    def backoffice_identity():
        if request.path.startswith('/backoffice/') and request.remote_user != 'staff':
            abort(403)

    @app.get('/')
    def home():
        return render_template('index.html', manuals=catalog.list(), categories=catalog.categories(), selected='')

    @app.get('/manuals')
    def manuals():
        category = request.args.get('category', '')
        return render_template('index.html', manuals=catalog.list(category), categories=catalog.categories(), selected=category)

    @app.get('/manuals/<manual_id>')
    def detail(manual_id):
        item = catalog.get(manual_id)
        if item is None:
            abort(404)
        return render_template('detail.html', manual=item)

    @app.get('/manuals/<manual_id>/preview')
    def preview(manual_id):
        origin = os.environ.get('MANUAL_PREVIEW_ORIGIN', '').rstrip('/')
        if not origin:
            abort(503)
        try:
            with urlopen(origin + '/preview/' + quote(manual_id, safe=''), timeout=5) as upstream:
                return Response(upstream.read(), mimetype='application/pdf',
                                headers={'Content-Disposition': 'inline'})
        except HTTPError as error:
            abort(error.code)
        except (URLError, TimeoutError):
            abort(502)

    @app.get('/backoffice/manuals')
    def backoffice():
        return render_template('backoffice.html', manuals=catalog.list())

    @app.get('/backoffice/manuals/download')
    def staff_download():
        filename = request.args.get('filename', '')
        path = resolve_manual_path(filename)
        if not path.is_file():
            abort(404)
        return send_file(path, as_attachment=True, download_name=path.name)

    @app.get('/health')
    def health():
        return {'status': 'ok', 'manuals': len(catalog.list())}

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5051)
