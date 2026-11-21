# Render Cloud Deployment Guide — BankEase

This guide outlines how to deploy the **BankEase Net Banking Application** on **[Render](https://render.com/)** using either the automated Blueprint (`render.yaml`) or manual dashboard setup.

---

## Architecture on Render

- **Backend (Web Service):** Django 4.2 LTS + Gunicorn + WhiteNoise + SQLite/PostgreSQL (Python 3.11/3.13)
- **Frontend (Static Site):** React 18 + Vite (SPA with `/* -> /index.html` rewrite)

---

## Method 1: 1-Click Automated Blueprint (Recommended)

1. **Push Changes to Your GitHub Repository:**
   Ensure `render.yaml`, `backend/build.sh`, and `frontend/public/_redirects` are committed to your GitHub repository:
   ```bash
   git add .
   git commit -m "feat: configure render deployment and add transaction timestamps"
   git push origin main
   ```

2. **Log in to Render:**
   - Go to [dashboard.render.com](https://dashboard.render.com/).
   - Click **New +** ➔ **Blueprint**.

3. **Connect Your Repository:**
   - Select `The-Heroic/mca2-fsdpython-bankease-`.
   - Render will automatically parse `render.yaml` and discover both services:
     - `bankease-backend` (Python Web Service)
     - `bankease-frontend` (Static Site)

4. **Click "Apply":**
   - Render will build and deploy both services automatically in parallel.
   - Once `bankease-backend` is live, copy its URL (e.g. `https://bankease-backend-xxxx.onrender.com`).
   - In `bankease-frontend` settings, ensure `VITE_API_BASE_URL` points to `https://<your-backend-subdomain>.onrender.com/api/v1`.

---

## Method 2: Manual Dashboard Setup

If you prefer to configure services manually in Render's web console:

### A. Deploy Django Backend (Web Service)

1. Click **New +** ➔ **Web Service**.
2. Connect your GitHub repository.
3. Configure the following fields:
   - **Name:** `bankease-backend`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python seed_demo_data.py
     ```
   - **Start Command:**
     ```bash
     gunicorn bankease_config.wsgi:application
     ```
4. In **Environment Variables**, add:
   - `PYTHON_VERSION`: `3.11.9`
   - `DEBUG`: `False`
   - `USE_SQLITE`: `True`
   - `ALLOWED_HOSTS`: `*`
   - `CORS_ALLOW_ALL`: `True`
   - `SECRET_KEY`: *(Click Generate)*
5. Click **Deploy Web Service**.
6. Copy your live backend URL (e.g., `https://bankease-backend.onrender.com`).

---

### B. Deploy React Frontend (Static Site)

1. Click **New +** ➔ **Static Site**.
2. Connect your GitHub repository.
3. Configure the following fields:
   - **Name:** `bankease-frontend`
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. In **Redirects / Rewrites**:
   - Add a rewrite rule:
     - **Source:** `/*`
     - **Destination:** `/index.html`
     - **Action:** `Rewrite`
5. In **Environment Variables**, add:
   - `VITE_API_BASE_URL`: `https://bankease-backend.onrender.com/api/v1` *(Replace with your actual backend URL)*
6. Click **Deploy Static Site**.

---

## Production Demo Accounts on Render

| Role | Username / Email | Password | Pre-Configured Balance |
| :--- | :--- | :--- | :--- |
| **Retail Customer** | `aarav.sharma@example.com` *(or `aarav_gupta`)* | `Secure@123` | ₹1,25,000.00 |
| **Bank Officer** | `vikram.officer@bankease.com` *(or `officer_priya`)* | `Officer@123` | ₹1,50,000.00 |
| **System Admin** | `admin@bankease.com` *(or `admin_rajesh`)* | `Admin@123` | ₹1,50,000.00 |
| **Locked User** | `locked.user@example.com` | `Secure@123` | Account Locked (Security Demo) |
