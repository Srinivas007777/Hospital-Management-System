# Hospital Management System

A full-stack Hospital Management System built using **Python, FastAPI, SQLite, HTML, CSS, and JavaScript**. This application helps manage patients, doctors, appointments, and prescriptions through a web-based interface.

## Features

- User registration and login
- JWT-based authentication
- Password hashing using Argon2
- Role-based access control
- Patient management (Create, Read, Update, Delete)
- Doctor management (Create, Read, Update, Delete)
- Appointment management
- Prescription management
- Search and dashboard interface
- REST API documentation using Swagger UI

## Technology Stack

| Category | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Authentication | JWT |
| Password Security | Argon2 |
| Testing | Pytest, HTTPX |
| Version Control | Git, GitHub |

## User Roles

- **Admin:** Full access to the system.
- **Doctor:** Access to medical records, appointments, and prescriptions according to permissions.
- **Receptionist:** Patient registration and appointment management.

## Project Structure

```text
hospital_api/
│
├── main.py
├── database.py
├── security.py
├── dependencies.py
├── patients.py
├── doctors.py
├── appointments.py
├── prescriptions.py
├── auth.py
│
├── index.html
├── style.css
├── script.js
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

*Adjust the structure above if your actual filenames or folder organization differ.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Srinivas007777/Hospital-Management-System.git
cd Hospital-Management-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure a secure `SECRET_KEY` for JWT authentication.

Do not upload `.env` to GitHub.

### 6. Start the backend

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 7. Open API documentation

Visit:

http://127.0.0.1:8000/docs

### 8. Start the frontend

Open `index.html` using VS Code Live Server.

## API Modules

| Module | Description |
|---|---|
| Authentication | Registration, login, current user |
| Patients | Patient management |
| Doctors | Doctor management |
| Appointments | Appointment management |
| Prescriptions | Prescription management |

## Testing

Automated tests are written using Pytest.

Run the test suite:

```bash
python -m pytest -v
```

**Latest test result: 29 passed.**

## Security

- JWT-based authentication
- Argon2 password hashing
- Role-based endpoint authorization
- Environment-based secret configuration
- Protected database operations

## Future Improvements

- Deploy the application online
- Add automated database backups
- Add reporting and analytics
- Improve UI responsiveness
- Add pagination and advanced search

## Author

**Srinivas Reddy**

GitHub: https://github.com/Srinivas007777

---

This project was developed as a practical full-stack backend development project using Python and FastAPI.