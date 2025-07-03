# 📂 EZ-Assessment

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
```

## 🚀 Deployment Plan

To deploy this Django-based secure file-sharing backend to production, I would follow these steps:

1. **Containerization (Docker)**  
   - Create a `Dockerfile` for the backend.
   - Use `docker-compose` to manage Django, Redis (for Celery), and PostgreSQL.

2. **Production Settings**
   - Set `DEBUG=False`, define `ALLOWED_HOSTS`.
   - Move secrets (like `FERNET_KEY`, DB credentials) to environment variables using `.env` + `python-decouple`.

3. **Web Server**
   - Use `gunicorn` as WSGI server.
   - Set up `nginx` as a reverse proxy and to serve media files.

4. **Database**
   - Use **PostgreSQL** on production.
   - Run `python manage.py migrate` after deployment.

5. **Task Queue (Celery)**
   - Deploy Celery workers and connect them to a **Redis** instance.
   - Optionally use **supervisord** or **systemd** to keep workers alive.

6. **Hosting Options**
   - Deploy on **Render**, **DigitalOcean**, **AWS EC2**, or **Heroku**.
   - Use HTTPS with Let's Encrypt or Cloudflare for secure file transfers.

7. **Logging & Monitoring**
   - Use tools like **Sentry** or **Prometheus** for monitoring.
   - Log errors and user activity securely.

```bash
touch DEPLOYMENT.md

