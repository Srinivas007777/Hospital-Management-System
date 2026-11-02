
import sqlite3


# ---------------- DATABASE CONNECTION ----------------

def get_connection():
    connection = sqlite3.connect(
        "hospital.db",
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")

    return connection


# ---------------- CREATE TABLES ----------------

def create_table():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Patients table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact_number TEXT
            )
        """)

        # Doctors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                contact_number TEXT
            )
        """)

        # Appointments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                doctor_id INTEGER NOT NULL,
                appointment_date DATE NOT NULL,
                status TEXT DEFAULT 'Scheduled',
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            )
        """)

        # Prescriptions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prescriptions (
                prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER NOT NULL,
                medication TEXT NOT NULL,
                dosage TEXT NOT NULL,
                instructions TEXT NOT NULL,
                FOREIGN KEY (appointment_id)
                    REFERENCES appointments(appointment_id)
            )
        """)

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'Receptionist'
            )
        """)

        # Add role column if it doesn't exist
        columns = cursor.execute(
            "PRAGMA table_info(users)"
        ).fetchall()

        column_names = [column["name"] for column in columns]

        if "role" not in column_names:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN role TEXT NOT NULL DEFAULT 'Receptionist'
            """)

            # Database indexes for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_appointments_patient_id
                ON appointments(patient_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_appointments_doctor_id
                ON appointments(doctor_id)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prescriptions_appointment_id
                ON prescriptions(appointment_id)
            """)

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------- PATIENT FUNCTIONS ----------------

def insert_patient(patient):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO patients
            (first_name, last_name, age, gender, contact_number)
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient["first_name"],
            patient["last_name"],
            patient["age"],
            patient["gender"],
            patient.get("contact_number")
        ))

        patient_id = cursor.lastrowid
        connection.commit()

        return patient_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fetch_all_patients():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM patients")

        return cursor.fetchall()

    finally:
        connection.close()


def fetch_patient_by_id(patient_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def update_patient(patient_id, patient):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE patients
            SET first_name = ?,
                last_name = ?,
                age = ?,
                gender = ?,
                contact_number = ?
            WHERE patient_id = ?
        """, (
            patient["first_name"],
            patient["last_name"],
            patient["age"],
            patient["gender"],
            patient.get("contact_number"),
            patient_id
        ))

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_patient(patient_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE patient_id = ?",
            (patient_id,)
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------- DOCTOR FUNCTIONS ----------------

def insert_doctor(doctor):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO doctors
            (first_name, last_name, specialty, contact_number)
            VALUES (?, ?, ?, ?)
        """, (
            doctor["first_name"],
            doctor["last_name"],
            doctor["specialty"],
            doctor.get("contact_number")
        ))

        doctor_id = cursor.lastrowid
        connection.commit()

        return doctor_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fetch_all_doctors():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM doctors")

        return cursor.fetchall()

    finally:
        connection.close()


def fetch_doctor_by_id(doctor_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def update_doctor(doctor_id, doctor):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE doctors
            SET first_name = ?,
                last_name = ?,
                specialty = ?,
                contact_number = ?
            WHERE doctor_id = ?
        """, (
            doctor["first_name"],
            doctor["last_name"],
            doctor["specialty"],
            doctor.get("contact_number"),
            doctor_id
        ))

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_doctor(doctor_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM doctors WHERE doctor_id = ?",
            (doctor_id,)
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------- APPOINTMENT FUNCTIONS ----------------

def insert_appointment(appointment):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO appointments
            (patient_id, doctor_id, appointment_date, status)
            VALUES (?, ?, ?, ?)
        """, (
            appointment["patient_id"],
            appointment["doctor_id"],
            appointment["appointment_date"],
            appointment["status"]
        ))

        appointment_id = cursor.lastrowid
        connection.commit()

        return appointment_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fetch_all_appointments():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM appointments")

        return cursor.fetchall()

    finally:
        connection.close()


def fetch_appointment_by_id(appointment_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id = ?",
            (appointment_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def update_appointment(appointment_id, appointment):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE appointments
            SET patient_id = ?,
                doctor_id = ?,
                appointment_date = ?,
                status = ?
            WHERE appointment_id = ?
        """, (
            appointment["patient_id"],
            appointment["doctor_id"],
            appointment["appointment_date"],
            appointment["status"],
            appointment_id
        ))

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_appointment(appointment_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM appointments WHERE appointment_id = ?",
            (appointment_id,)
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------- PRESCRIPTION FUNCTIONS ----------------

def insert_prescription(prescription):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO prescriptions
            (appointment_id, medication, dosage, instructions)
            VALUES (?, ?, ?, ?)
        """, (
            prescription["appointment_id"],
            prescription["medication"],
            prescription["dosage"],
            prescription["instructions"]
        ))

        prescription_id = cursor.lastrowid
        connection.commit()

        return prescription_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fetch_all_prescriptions():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM prescriptions")

        return cursor.fetchall()

    finally:
        connection.close()


def fetch_prescription_by_id(prescription_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM prescriptions WHERE prescription_id = ?",
            (prescription_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def update_prescription(prescription_id, prescription):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE prescriptions
            SET appointment_id = ?,
                medication = ?,
                dosage = ?,
                instructions = ?
            WHERE prescription_id = ?
        """, (
            prescription["appointment_id"],
            prescription["medication"],
            prescription["dosage"],
            prescription["instructions"],
            prescription_id
        ))

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def delete_prescription(prescription_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM prescriptions WHERE prescription_id = ?",
            (prescription_id,)
        )

        connection.commit()

        return cursor.rowcount

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


# ---------------- USER / AUTHENTICATION FUNCTIONS ----------------

def insert_user(username, email, hashed_password, role="Receptionist"):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, role)
            VALUES (?, ?, ?, ?)
        """, (username, email, hashed_password, role))

        user_id = cursor.lastrowid
        connection.commit()

        return user_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def fetch_user_by_username(username):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def fetch_user_by_id(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT user_id, username, email, role
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:
        connection.close()
