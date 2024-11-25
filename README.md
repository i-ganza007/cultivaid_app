# CultivAid 🌱
### Agricultural Services Marketplace Platform

CultivAid is a web-based platform that connects farmers with agricultural service providers, facilitating easy access to essential farming services like soil testing, equipment rental, and expert consultations.

## Features 🚀

### User Authentication System
- Secure registration and login
- Password hashing with bcrypt
- Profile management
- Role-based access control (Service providers vs Customers)

### Service Management
- Browse available agricultural services
- Service creation and editing for providers
- Detailed service descriptions and pricing
- Category-based service organization

### Booking System
- Real-time service booking
- Booking management for providers
- Service scheduling
- Status tracking

### Payment Integration
- Secure payment processing with Stripe
- Multiple payment method support
- Transaction history

## Technology Stack 💻

### Backend
- Flask (Python web framework)
- MongoDB (Database)
- Flask-MongoEngine (ODM)
- Flask-Login (Authentication)
- Flask-WTF (Forms)

### Frontend
- HTML5/CSS3
- Bootstrap 5
- JavaScript
- Font Awesome Icons

### Database
- MongoDB Atlas
- MongoEngine ODM

### Payment
- Stripe API Integration

## Installation 🔧

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your_username/cultivaid.git

**Set Up Virtual Environment**

python3 -m venv venv

**Install Dependencies**
pip install -r requirements.txt

** Environment Variables ** 

**Create a .env file in the root directory**:

SECRET_KEY=your_secret_key
MONGODB_URI=your_mongodb_uri
STRIPE_API_KEY=your_stripe_api_key

**Run the Application**
    flask run**
    
cultivaid/
├── cultivaid/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── forms.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── layout.html
│       ├── home.html
│       ├── auth.html
│       └── ...
├── wsgi.py
├── requirements.txt
└── README.md

**API Documentation 📚
Authentication Endpoints**

    POST /auth/register - User registration
    POST /auth/login - User login
    GET /auth/logout - User logout

**Service Endpoints**

    GET /services - List all services
    POST /services/create - Create new service
    PUT /services/<id> - Update service
    DELETE /services/<id> - Delete service

**Booking Endpoints**

    POST /book/<service_id> - Book a service
    GET /bookings - View user's bookings
    PUT /bookings/<id> - Update booking status

Contributing 🤝

    Fork the repository
    Create a feature branch (git checkout -b feature/AmazingFeature)
    Commit changes (git commit -m 'Add AmazingFeature')
    Push to branch (git push origin feature/AmazingFeature)
    Open a Pull Request

**Database Schema 🗄️**
**User Collection**

{
  "email": String,
  "password": String (hashed),
  "name": String,
  "role": String,
  "created_at": DateTime
}

**Service Collection**

{
  "title": String,
  "description": String,
  "price": Float,
  "provider": ObjectId (ref: User),
  "category": String,
  "created_at": DateTime
}

**Booking Collection**

{
  "service": ObjectId (ref: Service),
  "user": ObjectId (ref: User),
  "status": String,
  "booking_date": DateTime,
  "created_at": DateTime
}

**Deployment 🚀**

The application is deployed on Render with MongoDB Atlas as the database service.
Deployment Steps:

    Create a MongoDB Atlas cluster
    Configure Render web service
    Set environment variables on Render
    Deploy from GitHub

**License 📝**

This project is licensed under the MIT License - see the LICENSE.md file for details.
Support 🆘

For support, email support@cultivaid.com or join our Slack channel.
Acknowledgments 🙏

    Flask Documentation
    MongoDB Documentation
    Stripe API Documentation
    Bootstrap Templates

