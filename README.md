🛍️ Django E-Commerce API
This is a Django-based RESTful API that supports user authentication with email verification, product and category management, and Stripe payment integration.

🚀 Features
1. 🔐 User Management
Custom user model with email as username
JWT authentication with Simple JWT
Profile endpoint returning user email and profile info
Email verification & password reset (via Django’s built-in auth system)

2. 🛒 Products & Categories
Models for Product and Category
Filter and paginate products by category
Search products by name or description

🛠️ Tech Stack
Python 3.10+
Django 4.x
Django REST Framework
djangorestframework-simplejwt
SQLite

⚙️ Setup Instructions
1. Clone the Repository
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api

3. Create Virtual Environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

5. Install Requirements:
pip install -r requirements.txt


4. Setup .env file:
Create a .env file at the project root with the following:
EMAIL_USER=salmanexample@gmail.com
EMAIL_PASS=kndv dfnd ffsk nfks
EMAIL_FROM=salmanexample@gmail.com

5. Apply Migrations:
python manage.py makemigrations
python manage.py migrate

6. Create Superuser:
python manage.py createsuperuser

8. Run Server:
python manage.py runserver

Authentication (JWT)
Use JWT for login.

Get token via:
POST /api/token/
{
  "email": "user@example.com",
  "password": "yourpassword"
}

Add this token to the Authorization header:
Authorization: Bearer <your_token>
