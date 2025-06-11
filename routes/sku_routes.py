from flask import Blueprint, request, jsonify
import pandas as pd
import uuid
from datetime import datetime
from models.sku import SKU, sku_store
from utils import generate_tags, generate_category_id, generate_mock_price

sku_bp = Blueprint('sku', __name__)

@sku_bp.route('/import-csv', methods=['POST'])
def import_csv():
    """
    Import products from a CSV file.
    
    The CSV file should contain the following columns:
    - barcode: Product barcode
    - title: Product title
    - brand: Brand name
    - image_url: URL to product image
    
    Returns:
        JSON response containing success message
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400

    try:
        df = pd.read_csv(file)
        required_columns = ['barcode', 'title', 'brand', 'image_url']
        
        if not all(col in df.columns for col in required_columns):
            return jsonify({'error': 'CSV must contain barcode, title, brand, and image_url columns'}), 400

        imported_count = 0
        for _, row in df.iterrows():
            sku_id = str(uuid.uuid4())
            tags = generate_tags(row['title'], row['brand'])
            
            sku = SKU(
                sku_id=sku_id,
                barcode=row['barcode'],
                title=row['title'],
                brand=row['brand'],
                image_url=row['image_url'],
                tags=tags
            )
            sku_store.append(sku)
            imported_count += 1

        return jsonify({
            'message': f'Successfully imported {imported_count} SKUs'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sku_bp.route('/sku/<sku_id>/listings', methods=['GET'])
def get_listings(sku_id):
    """
    Get marketplace-ready listings for a specific SKU.
    
    Args:
        sku_id: The unique identifier of the SKU
        
    Returns:
        JSON response containing marketplace listings for:
        - Depop: title, brand, tags, image
        - eBay: title, category_id, price, image
    """
    sku = next((s for s in sku_store if s.sku_id == sku_id), None)
    if not sku:
        return jsonify({'error': 'SKU not found'}), 404

    # Generate category ID from last tag
    category_id = generate_category_id(sku.tags[-1]) if sku.tags else 0
    
    # Generate price using brand and tags
    price = generate_mock_price(sku.brand, sku.tags)

    listings = {
        'depop': {
            'title': sku.title,
            'brand': sku.brand,
            'tags': sku.tags,
            'image': sku.image_url,
            'price': price
        },
        'ebay': {
            'title': sku.title,
            'category_id': category_id,
            'price': price,
            'image': sku.image_url
        }
    }

    return jsonify(listings), 200

@sku_bp.route('/listings', methods=['GET'])
def get_all_listings():
    """
    Get marketplace-ready listings for all SKUs.
    
    Returns:
        JSON response containing a list of marketplace listings for all SKUs
    """
    all_listings = []
    
    for sku in sku_store:
        # Generate category ID from last tag
        category_id = generate_category_id(sku.tags[-1]) if sku.tags else 0
        
        # Generate price using brand and tags
        price = generate_mock_price(sku.brand, sku.tags)

        listing = {
            'sku_id': sku.sku_id,
            'depop': {
                'title': sku.title,
                'brand': sku.brand,
                'tags': sku.tags,
                'image': sku.image_url,
                'price': price
            },
            'ebay': {
                'title': sku.title,
                'category_id': category_id,
                'price': price,
                'image': sku.image_url
            }
        }
        all_listings.append(listing)

    return jsonify(all_listings), 200 