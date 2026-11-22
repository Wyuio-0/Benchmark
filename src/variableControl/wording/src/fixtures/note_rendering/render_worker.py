"""Host-only child: render the candidate's real Flask routes with private inputs."""
import base64
import importlib.util
import json
from pathlib import Path
import sys


def capture(response):
    return {'status': response.status_code, 'body': base64.b64encode(response.data).decode(),
            'headers': {k: v for k, v in response.headers.items()
                        if k.lower() not in {'content-length', 'transfer-encoding', 'content-encoding'}}}


def main():
    project, data_path, inputs_path, output = map(Path, sys.argv[1:])
    inputs = json.loads(inputs_path.read_text(encoding='utf-8'))
    original = json.loads(data_path.read_text(encoding='utf-8'))
    sys.path.insert(0, str(project))
    spec = importlib.util.spec_from_file_location('candidate_app', project / 'app.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    app = module.create_app(data_path)
    app.config.update(TESTING=True)
    client = app.test_client()
    ids = [order['id'] for order in original['orders']]
    pages = {}
    for path in ['/orders', '/backoffice/orders', '/health', '/orders/not-found']:
        pages[path] = capture(client.get(path))
    for oid in ids:
        for prefix in ['/orders/', '/backoffice/orders/']:
            path = prefix + oid
            pages[path] = capture(client.get(path))
    assets = {}
    static = project / 'static'
    for file in static.rglob('*'):
        if file.is_file():
            path = '/static/' + file.relative_to(static).as_posix()
            assets[path] = capture(client.get(path))
    scenarios = []
    expected = json.loads(json.dumps(original))
    for entry in inputs:
        oid = entry.get('order_id', ids[0])
        field = 'staff_note' if entry['kind'] == 'staff' else 'customer_note'
        prefix = '/backoffice/orders/' if field == 'staff_note' else '/orders/'
        path = prefix + oid
        response = client.post(path + '/note', data={'note': entry['text']})
        for order in expected['orders']:
            if order['id'] == oid:
                order[field] = entry['text']
        persisted = json.loads(data_path.read_text(encoding='utf-8')) == expected
        first = capture(client.get(path))
        # A fresh application instance must observe the same saved value.
        again = module.create_app(data_path).test_client().get(path)
        scenarios.append(dict(entry, path=path, post_status=response.status_code,
                              persisted=persisted, response=first,
                              reloaded=capture(again)))
    output.write_text(json.dumps({'pages': pages, 'assets': assets, 'scenarios': scenarios},
                                ensure_ascii=False), encoding='utf-8')


if __name__ == '__main__':
    main()
