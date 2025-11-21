import os
from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_service import WarehouseService
from validation import (ValidationError, validate_warehouse_creation,
                        validate_warehouse_update, validate_amount)

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY', 'dev-secret-key-change-in-production')

# Create a global warehouse service instance
warehouse_service = WarehouseService()


@app.route('/')
def list_warehouses():
    """List all warehouses."""
    warehouses = warehouse_service.list_warehouses()
    return render_template('list.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        name = request.form.get('name', '')
        tilavuus_str = request.form.get('tilavuus', '')
        saldo_str = request.form.get('saldo', '0')

        try:
            validated_name, tilavuus, saldo = validate_warehouse_creation(
                name, tilavuus_str, saldo_str)

            warehouse_id = warehouse_service.create_warehouse(
                validated_name, tilavuus, saldo)
            flash(f'Warehouse "{validated_name}" created successfully!',
                  'success')
            return redirect(url_for('view_warehouse',
                                    warehouse_id=warehouse_id))

        except ValidationError as e:
            for error in e.errors:
                flash(error, 'error')
            return render_template('create.html', name=name,
                                   tilavuus=tilavuus_str, saldo=saldo_str)

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """View a single warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    return render_template('view.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """Edit a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    if request.method == 'POST':
        name = request.form.get('name', '')
        tilavuus_str = request.form.get('tilavuus', '')
        saldo_str = request.form.get('saldo', '')

        try:
            validated_name, tilavuus, saldo = validate_warehouse_update(
                name, tilavuus_str, saldo_str)

            warehouse_service.update_warehouse(
                warehouse_id, name=validated_name,
                tilavuus=tilavuus, saldo=saldo)
            flash(f'Warehouse "{validated_name}" updated successfully!',
                  'success')
            return redirect(url_for('view_warehouse',
                                    warehouse_id=warehouse_id))

        except ValidationError as e:
            for error in e.errors:
                flash(error, 'error')
            warehouse['name'] = name
            warehouse['tilavuus'] = tilavuus_str
            warehouse['saldo'] = saldo_str
            return render_template('edit.html', warehouse=warehouse)

    return render_template('edit.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    maara_str = request.form.get('maara', '')

    try:
        maara = validate_amount(maara_str)
        warehouse_service.add_to_warehouse(warehouse_id, maara)
        flash(f'Added {maara} items to warehouse', 'success')
    except ValidationError as e:
        for error in e.errors:
            flash(error, 'error')

    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_items(warehouse_id):
    """Remove items from a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    maara_str = request.form.get('maara', '')

    try:
        maara = validate_amount(maara_str)
        removed = warehouse_service.remove_from_warehouse(warehouse_id, maara)
        flash(f'Removed {removed} items from warehouse', 'success')
    except ValidationError as e:
        for error in e.errors:
            flash(error, 'error')

    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    name = warehouse['name']
    warehouse_service.delete_warehouse(warehouse_id)
    flash(f'Warehouse "{name}" deleted successfully!', 'success')
    return redirect(url_for('list_warehouses'))


if __name__ == '__main__':
    app.run(debug=True)
