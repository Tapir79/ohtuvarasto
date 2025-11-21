from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_service import WarehouseService

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

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
        name = request.form.get('name', '').strip()
        tilavuus_str = request.form.get('tilavuus', '').strip()
        saldo_str = request.form.get('saldo', '0').strip()

        # Validate inputs
        errors = []

        if not name:
            errors.append('Name is required')

        try:
            tilavuus = float(tilavuus_str)
            if tilavuus < 0:
                errors.append('Capacity must be non-negative')
        except ValueError:
            errors.append('Capacity must be a valid number')
            tilavuus = 0

        try:
            saldo = float(saldo_str)
            if saldo < 0:
                errors.append('Balance must be non-negative')
        except ValueError:
            errors.append('Balance must be a valid number')
            saldo = 0

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('create.html', name=name,
                                   tilavuus=tilavuus_str, saldo=saldo_str)

        warehouse_id = warehouse_service.create_warehouse(
            name, tilavuus, saldo)
        flash(f'Warehouse "{name}" created successfully!', 'success')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

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
        name = request.form.get('name', '').strip()
        tilavuus_str = request.form.get('tilavuus', '').strip()
        saldo_str = request.form.get('saldo', '').strip()

        # Validate inputs
        errors = []

        if not name:
            errors.append('Name is required')

        try:
            tilavuus = float(tilavuus_str)
            if tilavuus < 0:
                errors.append('Capacity must be non-negative')
        except ValueError:
            errors.append('Capacity must be a valid number')
            tilavuus = warehouse['tilavuus']

        try:
            saldo = float(saldo_str)
            if saldo < 0:
                errors.append('Balance must be non-negative')
        except ValueError:
            errors.append('Balance must be a valid number')
            saldo = warehouse['saldo']

        if errors:
            for error in errors:
                flash(error, 'error')
            warehouse['name'] = name
            warehouse['tilavuus'] = tilavuus
            warehouse['saldo'] = saldo
            return render_template('edit.html', warehouse=warehouse)

        warehouse_service.update_warehouse(warehouse_id, name=name,
                                           tilavuus=tilavuus, saldo=saldo)
        flash(f'Warehouse "{name}" updated successfully!', 'success')
        return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))

    return render_template('edit.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    maara_str = request.form.get('maara', '').strip()

    try:
        maara = float(maara_str)
        if maara < 0:
            flash('Amount must be non-negative', 'error')
        else:
            warehouse_service.add_to_warehouse(warehouse_id, maara)
            flash(f'Added {maara} items to warehouse', 'success')
    except ValueError:
        flash('Amount must be a valid number', 'error')

    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_items(warehouse_id):
    """Remove items from a warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    maara_str = request.form.get('maara', '').strip()

    try:
        maara = float(maara_str)
        if maara < 0:
            flash('Amount must be non-negative', 'error')
        else:
            removed = warehouse_service.remove_from_warehouse(
                warehouse_id, maara)
            flash(f'Removed {removed} items from warehouse', 'success')
    except ValueError:
        flash('Amount must be a valid number', 'error')

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
