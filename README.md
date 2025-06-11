# Fashion Product Backend

A Flask-based backend service for managing fashion products, SKUs, and order processing.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The server will start at `http://localhost:5000`

> **Note:** This is a development version that uses in-memory storage (no database required). All data will be reset when the server restarts. No environment variables or configuration files are needed.

## Sample Data

### Download Sample CSV
You can download a complete sample CSV file with 100 fashion products:
[Download Sample CSV](https://file.notion.so/f/f/8b0a0363-15d9-813d-9f8c-000363dbe729/8eea5615-d3a2-40d0-8e51-62dff1ed6daa/layers_sample_products.csv?table=block&id=20fa0363-15d9-80b5-afdb-e71ab2972de5&spaceId=8b0a0363-15d9-813d-9f8c-000363dbe729&expirationTimestamp=1749664800000&signature=vCvOAM5s93R6-5txuCXAFUF2CRQWr_q2Xyepbr1sLMU&downloadName=layers+sample+products.csv)

### Example CSV Format
| barcode | title | brand | image_url |
|---------|-------|-------|-----------|
| 1000000000 | Levi's Jeans | Levi's | https://example.com/img1.jpg |
| 1000000001 | Carhartt T-Shirts | Carhartt | https://example.com/img2.jpg |
| 1000000002 | North Face Hoodies | North Face | https://example.com/img3.jpg |
| 1000000003 | Patagonia Sneakers | Patagonia | https://example.com/img4.jpg |
| 1000000004 | Levi's Jackets | Levi's | https://example.com/img5.jpg |
| 1000000005 | North Face Shirts | North Face | https://example.com/img6.jpg |
| 1000000006 | Adidas Shorts | Adidas | https://example.com/img7.jpg |
| 1000000007 | Adidas Dresses | Adidas | https://example.com/img8.jpg |
| 1000000008 | North Face Skirts | North Face | https://example.com/img9.jpg |
| 1000000009 | Levi's Coats | Levi's | https://example.com/img10.jpg |

The sample file contains 100 products from various brands including Levi's, Carhartt, North Face, Patagonia, Adidas, Nike, Uniqlo, H&M, Zara, and Dickies.

## API Endpoints

### 1. Import Products
**POST** `/import-csv`

Import products from a CSV file.

```bash
curl -X POST http://localhost:5000/import-csv \
  -F "file=@products.csv"
```

Response:
```json
{
    "message": "Successfully imported 4 SKUs"
}
```

### 2. Get Listings
**GET** `/sku/:skuId/listings`

Get marketplace-ready listings for a specific SKU.

```bash
curl http://localhost:5000/sku/123e4567-e89b-12d3-a456-426614174000/listings
```

Response:
```json
{
    "depop": {
        "title": "Levi's Jeans",
        "brand": "Levi's",
        "tags": ["jeans"],
        "image": "https://example.com/img1.jpg",
        "price": 17.99
    },
    "ebay": {
        "title": "Levi's Jeans",
        "category_id": 123,
        "price": 17.99,
        "image": "https://example.com/img1.jpg"
    }
}
```

Also added an endpoint to get all SKUs since the initial SKU ids are randomly generated.

**GET** `/sku/listings`

```bash
curl http://localhost:5000/sku/listings
```

### 3. Order Delivery Webhook
**POST** `/webhook/order-delivered`

Record an order delivery.

```bash
curl -X POST http://localhost:5000/webhook/order-delivered \
  -H "Content-Type: application/json" \
  -d '{
    "skuId": "123e4567-e89b-12d3-a456-426614174000",
    "delivered_at": "2025-06-10T12:00:00Z"
  }'
```

Response:
```json
{
    "message": "Order delivery recorded successfully"
}
```

### 4. Check Payout Status
**GET** `/payout-status/:skuId`

Check if a SKU is eligible for payout.

```bash
curl http://localhost:5000/payout-status/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
    "status": "pending"  // or "eligible" if >= 14 days since delivery
}
```

## Features

> **Note**: This is an in-memory implementation using server memory instead of a database. All data will be reset when the server restarts.

- **Data Integrity**: Enforces unique constraints on SKU IDs and barcodes
- **Smart Order Management**: Automatically updates existing orders when new delivery notifications are received for the same SKU
- **Efficient Lookups**: Uses optimized data structures for fast SKU and order retrieval
- **Duplicate Prevention**: Automatically skips duplicate SKUs during CSV import
- **Dynamic Tag Generation**: Intelligently extracts relevant tags from product titles while excluding brand names
- **Smart Pricing**: Calculates prices using a weighted formula: 30% brand value, 60% product category, 10% tag complexity
- **Category ID Generation**: Derives marketplace category IDs from product tags for accurate listing placement
- **Consistent Mock Values**: All generated values (tags, prices, categories) are deterministic based on product title and brand, ensuring consistency across imports
- **Order Validation**: Ensures orders can only be created for existing SKUs, maintaining data consistency
