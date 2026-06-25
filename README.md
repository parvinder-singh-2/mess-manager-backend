# Mess Manager Backend

A production-ready backend API for managing a tiffin/mess business. The application handles customer management, meal tracking, payments, and user authentication with role-based access.

## Features

* JWT-based Authentication and Authorization
* Secure password hashing using bcrypt
* Customer Management
* Customer Account Management
* Meal Transaction Management
* Payment Tracking
* Protected API Endpoints
* Role-based access control
* PostgreSQL database integration
* Automatic API documentation using Swagger/OpenAPI
* Dockerized application
* Production deployment on Railway

---

## Tech Stack

### Backend

* FastAPI
* Python 3.13
* SQLAlchemy ORM
* Pydantic

### Authentication

* JWT (JSON Web Tokens)
* Passlib
* Bcrypt
* Python-JOSE

### Database

* PostgreSQL

### Deployment

* Docker
* Railway

---

## Project Structure

```bash
Backend/
│
├── api/
│   ├── auth.py
│   ├── customers.py
│   ├── payments.py
│   └── meal_transactions.py
│
├── schemas/
│   ├── customer.py
│   ├── customer_account.py
│   ├── payment.py
│   ├── meal_transaction.py
│   └── user.py
│
├── utils/
│   └── auth.py
│
├── database.py
├── models.py
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── .env.example
```

---

## Authentication APIs

| Method | Endpoint       | Description                  |
| ------ | -------------- | ---------------------------- |
| POST   | /auth/register | Register new user            |
| POST   | /auth/login    | Login and receive JWT token  |
| GET    | /auth/me       | Get currently logged in user |

---

## Customer APIs

| Method | Endpoint                   |
| ------ | -------------------------- |
| GET    | /customers/                |
| POST   | /customers/                |
| GET    | /customers/search          |
| PUT    | /customers/{id}            |
| PATCH  | /customers/{id}/deactivate |
| PATCH  | /customers/{id}/reactivate |
| GET    | /customers/{id}/account    |
| PUT    | /customers/{id}/account    |

---

## Payment APIs

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | /payments/              |
| POST   | /payments/              |
| GET    | /payments/customer/{id} |
| GET    | /payments/{id}          |
| PUT    | /payments/{id}          |
| DELETE | /payments/{id}          |

---

## Meal Transaction APIs

| Method | Endpoint                               |
| ------ | -------------------------------------- |
| GET    | /meal-transactions/                    |
| POST   | /meal-transactions/                    |
| GET    | /meal-transactions/{id}                |
| PUT    | /meal-transactions/{id}                |
| DELETE | /meal-transactions/{id}                |
| GET    | /meal-transactions/customer/{id}       |
| GET    | /meal-transactions/delivery/{date}     |
| PATCH  | /meal-transactions/{id}/mark-delivered |

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/parvinder-singh-2/mess-manager-backend.git
cd mess-manager-backend
```

### Create Virtual Environment

```bash
python -m venv env
```

### Activate Virtual Environment

Windows:

```bash
env\Scripts\activate
```

Linux/Mac:

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=True
```

### Run Application

```bash
uvicorn main:app --reload
```

---

## Docker Setup

Build Docker image:

```bash
docker build -t mess-manager-backend .
```

Run container:

```bash
docker run -p 8000:8000 mess-manager-backend
```

---

## API Documentation

Swagger UI:

https://mess-manager-backend-production.up.railway.app/docs

OpenAPI JSON:

https://mess-manager-backend-production.up.railway.app/openapi.json

---

## Live Deployment

Backend URL:

https://mess-manager-backend-production.up.railway.app

---

## Future Enhancements

* React Frontend Integration
* Dashboard Analytics
* Expense Management
* Delivery Management Module
* SMS/Email Notifications
* Reports and Export Functionality
* Role-based Permissions Enhancement

---

## Author

**Parvinder Singh Gandhi**

LinkedIn: http://linkedin.com/in/parvinder-singh-gandhi2304/

GitHub: https://github.com/parvinder-singh-2
