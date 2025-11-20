"""Flask web application for managing warehouse instances."""
from flask import Flask, render_template, request, redirect, url_for, flash
from warehouse_service import WarehouseService

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'  # For flash messages

# Initialize the warehouse service
warehouse_service = WarehouseService()


@app.route('/')
def index():
    """Redirect to warehouses list."""
    return redirect(url_for('list_warehouses'))


@app.route('/warehouses')
def list_warehouses():
    """GET /warehouses – list all warehouses."""
    warehouses = warehouse_service.get_all_warehouses()
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouses/new')
def new_warehouse():
    """GET /warehouses/new – form to create a new warehouse."""
    return render_template('create_warehouse.html')


@app.route('/warehouses', methods=['POST'])
def create_warehouse():
    """POST /warehouses – create warehouse."""
    name = request.form.get('name', '').strip()

    # Validate name
    if not name:
        flash('Warehouse name is required', 'error')
        return redirect(url_for('new_warehouse'))

    # Get and validate capacity (tilavuus)
    try:
        tilavuus = float(request.form.get('tilavuus', 0))
        if tilavuus <= 0:
            flash('Capacity must be greater than 0', 'error')
            return redirect(url_for('new_warehouse'))
    except ValueError:
        flash('Invalid capacity value', 'error')
        return redirect(url_for('new_warehouse'))

    # Get and validate initial balance (alku_saldo)
    try:
        alku_saldo = float(request.form.get('alku_saldo', 0))
        if alku_saldo < 0:
            flash('Initial balance cannot be negative', 'error')
            return redirect(url_for('new_warehouse'))
    except ValueError:
        flash('Invalid initial balance value', 'error')
        return redirect(url_for('new_warehouse'))

    # Create the warehouse
    warehouse_id = warehouse_service.create_warehouse(
        name, tilavuus, alku_saldo)
    flash(f'Warehouse "{name}" created successfully', 'success')
    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouses/<int:warehouse_id>')
def warehouse_detail(warehouse_id):
    """GET /warehouses/<id> – view single warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    return render_template('warehouse_detail.html', warehouse=warehouse)


@app.route('/warehouses/<int:warehouse_id>/add', methods=['POST'])
def add_items(warehouse_id):
    """POST /warehouses/<id>/add – add items."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    # Get and validate amount
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(
                url_for(
                    'warehouse_detail',
                    warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid amount value', 'error')
        return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))

    # Add items
    warehouse_service.add_to_warehouse(warehouse_id, amount)
    flash(f'Added {amount} items to warehouse', 'success')
    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouses/<int:warehouse_id>/remove', methods=['POST'])
def remove_items(warehouse_id):
    """POST /warehouses/<id>/remove – remove items."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    # Get and validate amount
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(
                url_for(
                    'warehouse_detail',
                    warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid amount value', 'error')
        return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))

    # Remove items
    removed = warehouse_service.remove_from_warehouse(warehouse_id, amount)
    if removed is not None:
        flash(f'Removed {removed} items from warehouse', 'success')
    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouses/<int:warehouse_id>/edit')
def edit_warehouse(warehouse_id):
    """GET /warehouses/<id>/edit – form to edit."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    return render_template('edit_warehouse.html', warehouse=warehouse)


@app.route('/warehouses/<int:warehouse_id>/edit', methods=['POST'])
def update_warehouse(warehouse_id):
    """POST /warehouses/<id>/edit – update warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if not warehouse:
        flash('Warehouse not found', 'error')
        return redirect(url_for('list_warehouses'))

    # Get and validate name
    name = request.form.get('name', '').strip()
    if not name:
        flash('Warehouse name is required', 'error')
        return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))

    # Get and validate capacity
    try:
        tilavuus = float(request.form.get('tilavuus', 0))
        if tilavuus <= 0:
            flash('Capacity must be greater than 0', 'error')
            return redirect(
                url_for(
                    'edit_warehouse',
                    warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid capacity value', 'error')
        return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))

    # Get and validate balance
    try:
        saldo = float(request.form.get('saldo', 0))
        if saldo < 0:
            flash('Balance cannot be negative', 'error')
            return redirect(
                url_for(
                    'edit_warehouse',
                    warehouse_id=warehouse_id))
    except ValueError:
        flash('Invalid balance value', 'error')
        return redirect(url_for('edit_warehouse', warehouse_id=warehouse_id))

    # Update warehouse
    warehouse_service.update_warehouse(
        warehouse_id,
        name=name,
        tilavuus=tilavuus,
        saldo=saldo)
    flash(f'Warehouse "{name}" updated successfully', 'success')
    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouses/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """POST /warehouses/<id>/delete – delete warehouse."""
    warehouse = warehouse_service.get_warehouse(warehouse_id)
    if warehouse:
        name = warehouse['name']
        warehouse_service.delete_warehouse(warehouse_id)
        flash(f'Warehouse "{name}" deleted successfully', 'success')
    else:
        flash('Warehouse not found', 'error')

    return redirect(url_for('list_warehouses'))


if __name__ == '__main__':
    app.run(debug=True)
