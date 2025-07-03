# EZ-Assessment

# Secure File Sharing System – Backend API

A secure file-sharing system built using **Django**, **Django REST Framework**, **Celery**, and **Redis**, supporting role-based access for two user types: **Ops** and **Client**.

---

## 🚀 Features

### 👤 User Roles

- **Ops User**
  - Login
  - Upload files (only `.pptx`, `.docx`, `.xlsx`)

- **Client User**
  - Sign Up (receives encrypted verification link)
  - Verify Email (via tokenized link)
  - Login
  - Download files (via secure encrypted URL)
  - List uploaded files

---

## 🛠️ Tech Stack

| Component      | Technology                |
|----------------|---------------------------|
| Backend        | Django + DRF              |
| Async Tasks    | Celery                    |
| Task Broker    | Redis                     |
| Auth           | JWT (SimpleJWT)           |
| DB             | PostgreSQL / SQLite       |
| Email          | Django Email Backend      |
| File Storage   | Local (Media folder)      |
| Encryption     | `cryptography.Fernet`     |

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/secure-file-share.git
cd secure-file-share
