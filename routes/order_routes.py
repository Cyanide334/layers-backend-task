from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from dateutil import parser
from models.order import Order, order_store

order_bp = Blueprint('order', __name__)

@order_bp.route('/webhook/order-delivered', methods=['POST'])
def order_delivered():
    """
    Webhook endpoint for order delivery notifications.
    
    Expected JSON payload:
    {
        "skuId": "string",
        "delivered_at": "ISO8601 datetime string" (e.g. "2025-06-10T12:00:00Z")
    }
    
    Returns:
        JSON response with success message or error details
    """
    data = request.get_json()
    
    if not data or 'skuId' not in data or 'delivered_at' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        delivered_at = parser.parse(data['delivered_at'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid date format. Please use ISO8601 format (e.g. "2025-06-10T12:00:00Z")'}), 400

    order = Order(
        sku_id=data['skuId'],
        delivered_at=delivered_at
    )
    order_store.append(order)

    return jsonify({'message': 'Order delivery recorded successfully'}), 200

@order_bp.route('/payout-status/<sku_id>', methods=['GET'])
def get_payout_status(sku_id):
    """
    Get the payout status for a specific SKU.
    
    Args:
        sku_id: The unique identifier of the SKU
        
    Returns:
        JSON response containing:
        - status: "pending" if < 14 days since delivery, "eligible" if >= 14 days
    """
    order = next((o for o in order_store if o.sku_id == sku_id), None)
    if not order:
        return jsonify({'error': 'Order for this SKU not found'}), 404

    # Calculate if 14 days have passed since delivery
    is_eligible = datetime.now(order.delivered_at.tzinfo) - order.delivered_at >= timedelta(days=14)
    status = "eligible" if is_eligible else "pending"

    return jsonify({'status': status}), 200 
