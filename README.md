# Daily Expenses Sharing Application with JWT Authentication

This is a backend project built using **Django REST Framework** that includes user authentication, authorization, and expense management functionality. The system uses JWT tokens to authenticate users and allows them to add and view expenses, grouped by split methods (Equal, Exact, Percentage). It includes features like downloading balance sheets and validating user data such as email and Indian mobile numbers.

## Table of Contents

1. Features
2. Technology Stack
3. Setup and Installation
4. API Endpoints
- User Registration
- User Login
- Add Expense
- View User Expenses
- View Overall Expenses
- Download Balance Sheet
5. Validation Details

### Features

- User Registration with email and Indian mobile number validation.
- JWT-based authentication (Login system with JWT tokens).
- Add Expenses: Users can add expenses with various split methods (Equal, Exact, Percentage).
- View Expenses: Users can view their own expenses, and there’s an endpoint to get the overall expenses of all users.
- Download Balance Sheet: Ability to download expenses in CSV format grouped by split type.
- Authenticated Access: Only authenticated users can access the expenses API.

### Technology Stack

- Backend: Django REST Framework
- Authentication: JWT (JSON Web Token)
- Database: SQLite (can be switched to PostgreSQL or MySQL)
- Postman: For API testing

### Setup and Installation

#### Prerequisites

- Python
- Django
- Pip (Python Package Manager)

#### Installation Steps

1. Clone the repository:
```
git clone https://github.com/krishna-teja18/Daily-Expenses-Sharing-Application.git
cd expense_sharing
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run migrations to set up the database:
```
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser to access the Django admin:
```
python manage.py createsuperuser
```

5. Start the Django server:

```
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000/` to access the project.

### API Endpoints

#### 1. User Registration

- **URL**: `http://127.0.0.1:8000/users/register/`

- **Method**: POST

- **Request Body** (example):
```
{
  "email": "testuser@example.com",
  "name": "Test User",
  "mobile_number": "+919876543210",
  "password": "Password123"
}

```
- **Response**: User is created if validation passes. Password is hashed in the database.

#### 2. User Login

- **URL**: `http://127.0.0.1:8000/users/login/`

- **Method**: POST

- **Request Body**:
```
{
  "email": "testuser@example.com",
  "password": "Password123"
}
```

- **Response**:
```
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}

```

The access token is used to authenticate requests to other endpoints.

#### 3. Add Expense

- **URL**: `http://127.0.0.1:8000/expenses/add/`

- **Method**: POST

- **Request Body** (example for EQUAL split method):
```
{
  "total_amount": 3000,
  "split_method": "EQUAL",
  "participants": [
    {"participant": 1},
    {"participant": 2},
    {"participant": 3}
  ]
}
```

- **Request Body** (example for EXACT split method):
```
{
    "creator": 2,
    "total_amount": 5000.00,
    "split_method": "EXACT",
    "participants": [
        {"participant": 2, "amount": 2000.00},
        {"participant": 3, "amount": 3000.00}
    ]
}
```

- **Request Body** (example for PERCENTAGE split method):
```
{
    "creator": 1,
    "total_amount": 4000.00,
    "split_method": "PERCENTAGE",
    "participants": [
        {"participant": 2, "percentage": 50},
        {"participant": 3, "percentage": 50}
    ]
}
```

- **Headers**: Authorization: Bearer `<access_token>`

- **Response**: Expense is created, and split among the participants equally.

#### 4. View User Expenses
- **URL**: `http://127.0.0.1:8000/expenses/user/<int:user_id>/`

- **Method**: GET

- **Response**: List of all expenses related to the user.

#### 5. View Overall Expenses
- **URL**: `http://127.0.0.1:8000/expenses/overall/`

- **Method**: GET

- **Response**: Total amount of expenses across all users.

#### Download Balance Sheet

- **URL**: `http://127.0.0.1:8000/expenses/download/`

- **Method**: GET

- **Response**: A CSV file downloaded containing all expenses grouped by split method (Equal, Exact, Percentage).

### Screenshots (Postman Testing)

1. **User Registration**

2. **User Login**

3. **Add Expense**

4. **View User Expenses**

5. **Download Balance Sheet**

### Validation Details

1. **Email Validation**: Email is checked for standard format (must include `@` and domain like `.com`, `.net`, etc.).

2. **Indian Mobile Number Validation**: Mobile number is validated with a regex for Indian format (`+91` followed by 10 digits).

3. **Password Validation**: Basic length and complexity checks can be added based on project requirements.

