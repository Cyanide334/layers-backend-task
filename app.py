from flask import Flask
from routes.sku_routes import sku_bp
from routes.order_routes import order_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(sku_bp)
app.register_blueprint(order_bp)

if __name__ == '__main__':
    app.run(debug=True) 