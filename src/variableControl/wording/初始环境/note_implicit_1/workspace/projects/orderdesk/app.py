from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for
from orderdesk.formatting import format_note
from orderdesk.repository import OrderRepository


def create_app(data_path=None):
    app = Flask(__name__)
    repository = OrderRepository(data_path or Path(__file__).parent / 'data/orders.json')

    @app.get('/')
    def home():
        return redirect(url_for('orders'))

    @app.get('/orders')
    def orders():
        return render_template('orders.html', orders=repository.list_orders())

    @app.get('/orders/<order_id>')
    def order_detail(order_id):
        order = repository.get(order_id)
        if order is None:
            abort(404)
        return render_template('order.html', order=order, note=order['customer_note'])

    @app.post('/orders/<order_id>/note')
    def save_customer_note(order_id):
        if repository.get(order_id) is None:
            abort(404)
        repository.save_note(order_id, 'customer_note', request.form.get('note', ''))
        return redirect(url_for('order_detail', order_id=order_id))

    @app.get('/backoffice/orders')
    def backoffice_orders():
        return render_template('backoffice.html', orders=repository.list_orders())

    @app.get('/backoffice/orders/<order_id>')
    def backoffice_detail(order_id):
        order = repository.get(order_id)
        if order is None:
            abort(404)
        return render_template('backoffice_detail.html', order=order,
                               note=format_note(order['staff_note']))

    @app.post('/backoffice/orders/<order_id>/note')
    def save_staff_note(order_id):
        if repository.get(order_id) is None:
            abort(404)
        repository.save_note(order_id, 'staff_note', request.form.get('note', ''))
        return redirect(url_for('backoffice_detail', order_id=order_id))

    @app.get('/health')
    def health():
        return {'status': 'ok', 'orders': len(repository.list_orders())}

    return app


if __name__ == '__main__':
    create_app().run(host='127.0.0.1', port=5050)
