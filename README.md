# Flask Project Setup

This document provides instructions for setting up and running the Flask project, including initializing a virtual environment, installing dependencies, applying CRUD operations, and other related information.

## Prerequisites

- Python 3.9.6 installed on your system.
- `pip` (Python package installer) installed.

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/muhammadkhalid621/python_CRUD
cd python_CRUD
```

### 2. Create a Virtual Environment

python -m venv venv

### 3. Activate the Virtual Environment

venv\Scripts\activate

### 4. On macOS/Linux:

source venv/bin/activate

### 5. Install Dependencies

pip install -r requirements.txt

### 6. Run the Flask Application

flask run / python app.py  

## CRUD OPERATIONS


### 1. Create a User

Endpoint: POST /users

Request Body:

{
  "username": "newUsername",
  "password": "newStrongPassword",
  "active": true
}


### 2. Retrieve All Users

Endpoint: GET /users

### 3. Retrieve a User by ID

Endpoint: GET /users/<id>

### 4. Update a User

Endpoint: POST /users/update/<id>

### 5. Delete a User

Endpoint: DELETE /users/<id>
