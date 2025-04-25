# 📝 TodoTask API

A clean and scalable task management API built using the latest version of **Django** and **Django REST Framework**, focused on productivity apps with:

- 🔐 JWT Authentication
- 📁 Projects, Tasks, and Subtasks
- ⚙️ Query Handling in Serializers
- ✅ Modern & Minimal Endpoint Design

---

## 🚀 Features

- User Registration & Login
- JWT-based Token Authentication & Refresh
- Full CRUD for Projects, Tasks, and Subtasks
- Clear separation of logic using serializers
- Modern REST API structure

---

## 🧰 Tech Stack

- **Python 3.11+**
- **Django 5.x**
- **Django REST Framework**
- **djangorestframework-simplejwt**

---

## 🔐 Authentication Endpoints

| Method | Endpoint                 | Description                      |
|--------|--------------------------|----------------------------------|
| POST   | `/api/login_user/`       | Log in user (returns JWT)        |
| POST   | `/api/create_user/`      | Register a new user              |

---

## 👤 User Endpoints

| Method | Endpoint             | Description          |
|--------|----------------------|----------------------|
| GET    | `/api/users/`        | List all users       |

---

## 📁 Project Endpoints

| Method | Endpoint                          | Description                |
|--------|-----------------------------------|----------------------------|
| GET    | `/api/projects/`                  | Get all projects           |
| POST   | `/api/create_project/`            | Create a new project       |
| PUT    | `/api/update_project/`            | Update existing project    |
| DELETE | `/api/delete_project/<id>/`       | Delete a project by ID     |

---

## ✅ Task Endpoints

| Method | Endpoint                          | Description                |
|--------|-----------------------------------|----------------------------|
| GET    | `/api/tasks/`                     | Get all tasks              |
| POST   | `/api/create_task/`               | Create a new task          |
| PUT    | `/api/update_task/`               | Update existing task       |
| DELETE | `/api/delete_task/<id>/`          | Delete a task by ID        |

---

## 📌 Subtask Endpoints

| Method | Endpoint                          | Description                   |
|--------|-----------------------------------|-------------------------------|
| GET    | `/api/subtasks/`                  | Get all subtasks              |
| POST   | `/api/create_subtask/`            | Create a new subtask          |
| PUT    | `/api/update_subtask/`            | Update existing subtask       |
| DELETE | `/api/delete_subtask/<id>/`       | Delete a subtask by ID        |

---

## 🧠 Business Logic in Serializers

This project follows a clean architecture where most of the complex logic, validation, and relational data handling is done inside **serializers** — keeping the views light and focused on routing only.

---

## ⚒️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/itx-zeeshan/todotask-api-django.git
cd todotask-api-django

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # For Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations and run server
python manage.py migrate
python manage.py runserver
