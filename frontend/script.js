// ========================================
// HOSPITAL MANAGEMENT SYSTEM - FRONTEND
// ========================================

const API_BASE = "http://127.0.0.1:8000";

// ========================================
// MODULE CONFIGURATION
// ========================================

const modules = {

    patients: {
        title: "Patients",
        endpoint: "/patients",
        id: "patient_id",

        fields: [
            { name: "first_name", label: "First name", required: true },
            { name: "last_name", label: "Last name", required: true },
            { name: "age", label: "Age", type: "number", required: true },
            {
                name: "gender",
                label: "Gender",
                type: "select",
                options: ["Male", "Female", "Other"],
                required: true
            },
            { name: "contact_number", label: "Contact number", required: true }
        ],

        columns: [
            "patient_id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "contact_number"
        ]
    },

    doctors: {
        title: "Doctors",
        endpoint: "/doctors",
        id: "doctor_id",

        fields: [
            { name: "first_name", label: "First name", required: true },
            { name: "last_name", label: "Last name", required: true },
            { name: "specialty", label: "Specialty", required: true },
            { name: "contact_number", label: "Contact number", required: true }
        ],

        columns: [
            "doctor_id",
            "first_name",
            "last_name",
            "specialty",
            "contact_number"
        ]
    },

    appointments: {
        title: "Appointments",
        endpoint: "/appointments",
        id: "appointment_id",

        fields: [
            {
                name: "patient_id",
                label: "Patient ID",
                type: "number",
                required: true
            },
            {
                name: "doctor_id",
                label: "Doctor ID",
                type: "number",
                required: true
            },
            {
                name: "appointment_date",
                label: "Appointment date",
                type: "date",
                required: true
            },
            {
                name: "status",
                label: "Status",
                type: "select",
                options: ["Scheduled", "Completed", "Cancelled"],
                required: true
            }
        ],

        columns: [
            "appointment_id",
            "patient_id",
            "doctor_id",
            "appointment_date",
            "status"
        ]
    },

    prescriptions: {
        title: "Prescriptions",
        endpoint: "/prescriptions",
        id: "prescription_id",

        fields: [
            {
                name: "appointment_id",
                label: "Appointment ID",
                type: "number",
                required: true
            },
            { name: "medication", label: "Medication", required: true },
            { name: "dosage", label: "Dosage", required: true },
            {
                name: "instructions",
                label: "Instructions",
                type: "textarea",
                required: true
            }
        ],

        columns: [
            "prescription_id",
            "appointment_id",
            "medication",
            "dosage",
            "instructions"
        ]
    }
};


// ========================================
// APPLICATION STATE
// ========================================

let currentUser = null;
let activeModule = null;
let editingId = null;

const records = {
    patients: [],
    doctors: [],
    appointments: [],
    prescriptions: []
};


// ========================================
// ROLE PERMISSIONS
// ========================================

const rolePermissions = {

    Admin: {
        patients: ["read", "create", "edit", "delete"],
        doctors: ["read", "create", "edit", "delete"],
        appointments: ["read", "create", "edit", "delete"],
        prescriptions: ["read", "create", "edit", "delete"]
    },

    Doctor: {
        patients: ["read"],
        doctors: ["read"],
        appointments: ["read"],
        prescriptions: ["read", "create", "edit", "delete"]
    },

    Receptionist: {
        patients: ["create"],
        doctors: [],
        appointments: ["read", "create", "edit"],
        prescriptions: []
    }
};


// ========================================
// HELPER FUNCTIONS
// ========================================

const $ = id => document.getElementById(id);

function permission(module, action) {
    return Boolean(
        rolePermissions[currentUser?.role]?.[module]?.includes(action)
    );
}

function token() {
    return localStorage.getItem("hospitalToken");
}

function setMessage(id, message, isError = true) {
    const element = $(id);

    if (element) {
        element.textContent = message;
        element.style.color = isError ? "#d04444" : "#15966a";
    }
}

function showToast(message) {
    const toast = $("toast");

    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2600);
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    }[char]));
}

function labelFor(value) {
    return value
        .replaceAll("_", " ")
        .replace(/\b\w/g, char => char.toUpperCase());
}


// ========================================
// API REQUEST FUNCTION
// ========================================

async function apiRequest(path, options = {}) {

    const headers = {
        ...(options.headers || {})
    };

    if (token()) {
        headers.Authorization = `Bearer ${token()}`;
    }

    if (options.body && !(options.body instanceof FormData)) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(
        `${API_BASE}${path}`,
        {
            ...options,
            headers
        }
    );

    const raw = await response.text();

    let data = null;

    try {
        data = raw ? JSON.parse(raw) : null;
    } catch {
        data = raw;
    }

    if (!response.ok) {

        const detail = data?.detail;

        const message = Array.isArray(detail)
            ? detail.map(item => item.msg).join(", ")
            : (detail || data?.message || `Request failed (${response.status})`);

        throw new Error(message);
    }

    return data;
}


// ========================================
// HANDLE API LIST RESPONSES
// ========================================

function unwrapList(data) {

    if (Array.isArray(data)) {
        return data;
    }

    if (Array.isArray(data?.items)) {
        return data.items;
    }

    if (Array.isArray(data?.patients)) {
        return data.patients;
    }

    if (Array.isArray(data?.doctors)) {
        return data.doctors;
    }

    if (Array.isArray(data?.appointments)) {
        return data.appointments;
    }

    if (Array.isArray(data?.prescriptions)) {
        return data.prescriptions;
    }

    return [];
}


// ========================================
// LOGIN AND SESSION
// ========================================

function showLogin() {
    $("loginView").classList.remove("hidden");
    $("appView").classList.add("hidden");
}

function showApp(user) {

    currentUser = user;

    $("loginView").classList.add("hidden");
    $("appView").classList.remove("hidden");

    $("sidebarUsername").textContent = user.username;
    $("topUsername").textContent = user.username;
    $("sidebarRole").textContent = user.role;

    $("userAvatar").textContent =
        (user.username || "U").charAt(0).toUpperCase();

    // Display navigation according to role
    document.querySelectorAll(".nav-link").forEach(button => {

        const page = button.dataset.page;

        const allowed =
            page === "dashboard" ||
            permission(page, "read") ||
            permission(page, "create");

        button.classList.toggle("hidden", !allowed);
    });

    // Display add buttons according to role
    document.querySelectorAll(".add-button").forEach(button => {

        const module = button.dataset.add;

        button.classList.toggle(
            "hidden",
            !permission(module, "create")
        );
    });

    showPage("dashboard");

    loadDashboard();
}

async function login(username, password) {

    const body = new URLSearchParams({
        username,
        password
    });

    const response = await fetch(
        `${API_BASE}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body
        }
    );

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(
            data.detail || "Login failed. Check your username and password."
        );
    }

    if (!data.access_token) {
        throw new Error("Login response did not contain an access token.");
    }

    localStorage.setItem("hospitalToken", data.access_token);

    const me = await apiRequest("/auth/me");

    showApp(me.user || me);
}

async function restoreSession() {

    if (!token()) {
        showLogin();
        return;
    }

    try {

        const me = await apiRequest("/auth/me");

        showApp(me.user || me);

    } catch {

        localStorage.removeItem("hospitalToken");

        showLogin();
    }
}


// ========================================
// NAVIGATION
// ========================================

function showPage(page) {

    document.querySelectorAll(".page").forEach(element => {
        element.classList.add("hidden");
    });

    $(`${page}Page`).classList.remove("hidden");

    document.querySelectorAll(".nav-link").forEach(element => {

        element.classList.toggle(
            "active",
            element.dataset.page === page
        );
    });

    $("pageTitle").textContent =
        page === "dashboard"
            ? "Dashboard"
            : modules[page].title;

    if (modules[page]) {
        loadModule(page);
    }
}


// ========================================
// DASHBOARD
// ========================================

async function loadDashboard() {

    const countTargets = {
        patients: "patientCount",
        doctors: "doctorCount",
        appointments: "appointmentCount",
        prescriptions: "prescriptionCount"
    };

    for (const module of Object.keys(countTargets)) {

        const target = $(countTargets[module]);

        if (!permission(module, "read")) {
            target.textContent = "—";
            continue;
        }

        try {

            const data = await apiRequest(
                modules[module].endpoint
            );

            const list = unwrapList(data);

            records[module] = list;

            target.textContent = list.length;

        } catch {

            target.textContent = "—";
        }
    }
}


// ========================================
// LOAD MODULE RECORDS
// ========================================

async function loadModule(module) {

    const config = modules[module];

    const body = $(`${module}Body`);
    const head = $(`${module}Head`);
    const message = $(`${module}Message`);

    if (!permission(module, "read")) {

        head.innerHTML = "";
        body.innerHTML = "";

        message.textContent =
            "Your account does not have permission to view these records.";

        return;
    }

    message.textContent = "Loading records...";

    try {

        const data = await apiRequest(config.endpoint);

        records[module] = unwrapList(data);

        renderTable(module);

    } catch (error) {

        message.textContent = error.message;

        body.innerHTML = "";
    }
}


// ========================================
// DISPLAY TABLE
// ========================================

function renderTable(module, search = "") {

    const config = modules[module];

    const head = $(`${module}Head`);
    const body = $(`${module}Body`);
    const message = $(`${module}Message`);

    head.innerHTML = `
        <tr>
            ${config.columns.map(column =>
                `<th>${labelFor(column)}</th>`
            ).join("")}
            <th>Actions</th>
        </tr>
    `;

    const filtered = records[module].filter(record => {

        return config.columns.some(column => {

            return String(record[column] ?? "")
                .toLowerCase()
                .includes(search.toLowerCase());

        });
    });

    body.innerHTML = filtered.map(record => {

        const cells = config.columns.map(column => {

            return `<td>${escapeHtml(record[column] ?? "—")}</td>`;

        }).join("");

        const actions = `
            ${
                permission(module, "edit")
                ? `<button class="small-button"
                    data-edit="${module}"
                    data-id="${record[config.id]}">
                    Edit
                   </button>`
                : ""
            }

            ${
                permission(module, "delete")
                ? `<button class="small-button delete"
                    data-delete="${module}"
                    data-id="${record[config.id]}">
                    Delete
                   </button>`
                : ""
            }
        `;

        return `
            <tr>
                ${cells}
                <td>
                    <div class="action-cell">
                        ${actions || "—"}
                    </div>
                </td>
            </tr>
        `;

    }).join("");

    message.textContent = filtered.length
        ? `${filtered.length} record(s)`
        : "No records found.";
}


// ========================================
// ADD / EDIT RECORD MODAL
// ========================================

function openModal(module, record = null) {

    activeModule = module;

    editingId = record
        ? record[modules[module].id]
        : null;

    const title = modules[module].title;

    const singularTitle = {
        patients: "patient",
        doctors: "doctor",
        appointments: "appointment",
        prescriptions: "prescription"
    }[module];

    $("modalTitle").textContent =
        `${record ? "Edit" : "Add"} ${singularTitle}`;

    $("formMessage").textContent = "";

    $("formFields").innerHTML =
        modules[module].fields.map(field => {

            const value = record?.[field.name] ?? "";

            let control = "";

            if (field.type === "select") {

                control = `
                    <select
                        id="field_${field.name}"
                        name="${field.name}"
                        ${field.required ? "required" : ""}
                    >
                        <option value="">
                            Select ${field.label.toLowerCase()}
                        </option>

                        ${field.options.map(option => `
                            <option
                                value="${option}"
                                ${String(value) === option ? "selected" : ""}
                            >
                                ${option}
                            </option>
                        `).join("")}
                    </select>
                `;

            } else if (field.type === "textarea") {

                control = `
                    <textarea
                        id="field_${field.name}"
                        name="${field.name}"
                        ${field.required ? "required" : ""}
                    >${escapeHtml(value)}</textarea>
                `;

            } else {

                control = `
                    <input
                        id="field_${field.name}"
                        name="${field.name}"
                        type="${field.type || "text"}"
                        value="${escapeHtml(value)}"
                        ${field.required ? "required" : ""}
                        ${field.type === "number" ? 'min="0"' : ""}
                    >
                `;
            }

            return `
                <div class="field">
                    <label for="field_${field.name}">
                        ${field.label}
                        ${field.required ? "*" : ""}
                    </label>

                    ${control}
                </div>
            `;

        }).join("");

    $("recordModal").classList.remove("hidden");
}

function closeModal() {

    $("recordModal").classList.add("hidden");

    $("recordForm").reset();
}


// ========================================
// SAVE RECORD
// ========================================

async function saveRecord(event) {

    event.preventDefault();

    const config = modules[activeModule];

    const formData = new FormData(event.currentTarget);

    const payload = {};

    config.fields.forEach(field => {

        const value = formData.get(field.name);

        payload[field.name] =
            field.type === "number"
                ? Number(value)
                : value;
    });

    try {

        const path = editingId === null
            ? config.endpoint
            : `${config.endpoint}/${editingId}`;

        await apiRequest(
            path,
            {
                method: editingId === null ? "POST" : "PUT",
                body: JSON.stringify(payload)
            }
        );

        const wasEditing = editingId !== null;

        closeModal();

        showToast(
            wasEditing
                ? "Record updated successfully."
                : "Record created successfully."
        );

        await loadModule(activeModule);

        loadDashboard();

    } catch (error) {

        setMessage("formMessage", error.message);
    }
}


// ========================================
// DELETE RECORD
// ========================================

async function deleteRecord(module, id) {

    const confirmed = confirm(
        "Are you sure you want to delete this record?"
    );

    if (!confirmed) {
        return;
    }

    try {

        await apiRequest(
            `${modules[module].endpoint}/${id}`,
            {
                method: "DELETE"
            }
        );

        showToast("Record deleted successfully.");

        await loadModule(module);

        loadDashboard();

    } catch (error) {

        showToast(error.message);
    }
}


// ========================================
// EVENT LISTENERS
// ========================================

// Login form
$("loginForm").addEventListener("submit", async event => {

    event.preventDefault();

    setMessage("loginMessage", "");

    const username = $("username").value.trim();
    const password = $("password").value;

    try {

        await login(username, password);

    } catch (error) {

        setMessage("loginMessage", error.message);
    }
});


// Logout
$("logoutButton").addEventListener("click", () => {

    localStorage.removeItem("hospitalToken");

    currentUser = null;

    showLogin();
});


// Navigation
document.querySelectorAll(".nav-link").forEach(button => {

    button.addEventListener("click", () => {

        showPage(button.dataset.page);

    });
});


// Add buttons
document.querySelectorAll(".add-button").forEach(button => {

    button.addEventListener("click", () => {

        openModal(button.dataset.add);

    });
});


// Search
document.querySelectorAll(".search-input").forEach(input => {

    input.addEventListener("input", () => {

        renderTable(
            input.dataset.search,
            input.value
        );

    });
});


// Edit and delete buttons
document.addEventListener("click", event => {

    const editButton = event.target.closest("[data-edit]");
    const deleteButton = event.target.closest("[data-delete]");

    if (editButton) {

        const module = editButton.dataset.edit;

        const record = records[module].find(item =>

            String(item[modules[module].id]) === editButton.dataset.id

        );

        if (record) {
            openModal(module, record);
        }
    }

    if (deleteButton) {

        deleteRecord(
            deleteButton.dataset.delete,
            deleteButton.dataset.id
        );
    }
});


// Save form
$("recordForm").addEventListener("submit", saveRecord);


// Close modal
$("closeModal").addEventListener("click", closeModal);

$("cancelModal").addEventListener("click", closeModal);


// Close modal when clicking outside
$("recordModal").addEventListener("click", event => {

    if (event.target === $("recordModal")) {
        closeModal();
    }
});


// ========================================
// INITIALIZE APPLICATION
// ========================================

restoreSession();