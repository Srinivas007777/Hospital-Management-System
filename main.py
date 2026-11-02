from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from routes.patient_routes import router as patient_router
from routes.doctor_routes import router as doctor_router
from routes.appointment_routes import router as appointment_router
from routes.prescription_routes import router as prescription_router
from routes.auth_routes import router as auth_router

from database import create_table
from logging_config import logger


app = FastAPI(
    title="Hospital Management System API",
    description="""
    A Hospital Management API built using Python and FastAPI.

    Features:
    - Patient management
    - Doctor management
    - Appointment management
    - Prescription management
    - User authentication using JWT
    - Role-Based Access Control (RBAC)
    """,
    version="1.0.0",
    contact={
        "name": "Hospital API Developer",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
create_table()


# Register API routers
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(prescription_router)
app.include_router(auth_router)


@app.get("/", tags=["General"], summary="Home")
def home():
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to Hospital Management API"}


@app.get("/about", tags=["General"], summary="About the project")
def about():
    return {
        "project": "Hospital Management System",
        "developer": "Srinivas"
    }


@app.get("/health", tags=["General"], summary="Health check")
def health():
    return {"status": "running"}
