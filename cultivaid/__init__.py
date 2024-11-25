from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mongoengine as me
import stripe



app = Flask(__name__)
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51QMnNYKuNnSzGhzCL8qNIXmueQZrBOEKMXJGvZnYIszidgVlPvcfb9qfNpR3p3npXtHuyKtdGcHIqIA1G4Kt6JH700v6YACziK'
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51QMnNYKuNnSzGhzCDU9S8EFsbuT14nJ8USnV7j9EUrZShIM1tJGCLsR6yRyHweXNmjS95nIJWzy0IxcFq7JK3WA500HDsbAUCP'
app.config['SECRET_KEY'] = '74190f5f81f60d69899a'
app.config["MONGODB_SETTINGS"] = {
    'db': 'myflaskdb',  # Changed to your database name
    'host': 'localhost',
    'port': 27017
}

stripe.api_key = app.config['STRIPE_SECRET_KEY']

# Initialize LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'auth'  # Redirect to auth route when login is required

# Add error handling for database connection
try:
    db = MongoEngine(app)
    # Test the connection
    with app.app_context():
        db.get_db()
    print("✅ Successfully connected to MongoDB!")
except me.connection.ConnectionFailure as e:
    print(f"❌ Failed to connect to MongoDB. Error: {e}")
    print("Please check if MongoDB service is running!")
except Exception as e:
    print(f"❌ An error occurred: {e}")

bcrypt = Bcrypt(app)

# Import routes after initializing app and extensions
from cultivaid import routes