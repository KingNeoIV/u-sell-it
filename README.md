<div align="center">

<br>

<img src="https://img.shields.io/badge/u--sell--it-Marketplace%20Platform-6C63FF?style=for-the-badge&logo=python&logoColor=white" />

# 🛍️ **u‑sell‑it**

### A Modern Cross‑Platform Marketplace Platform

**FastAPI • React • PostgreSQL • Docker**  
**PyQt6 • C++ • iOS • Android • macOS • Windows**

<br>

<img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" />
<img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Python-3.12-yellow?style=flat-square&logo=python" />
<img src="https://img.shields.io/badge/FastAPI-Ready-009688?style=flat-square&logo=fastapi" />
<img src="https://img.shields.io/badge/React-Incoming-61DAFB?style=flat-square&logo=react" />

<br><br>

</div>

---

<div align="center">

### ⚡ A full‑stack rebuild of the original desktop prototype

### ⚡ Designed for Windows, macOS, Linux, iPhone (iOS), and Android

### ⚡ Built for scalability, performance, and modern development

</div>

---

# 🌍 **Platform Support**

<div align="center">

| Platform         | Status      | Notes                           |
| ---------------- | ----------- | ------------------------------- |
| **Windows**      | ✔ Supported | Primary development environment |
| **macOS**        | ✔ Supported | Backend + future desktop client |
| **iPhone (iOS)** | ✔ Planned   | React Native or SwiftUI client  |
| **Android**      | ✔ Planned   | React Native or Flutter client  |
| **Linux**        | ✔ Supported | Backend + server deployment     |

</div>

u‑sell‑it is being built as a **true cross‑platform ecosystem**, with:

- A backend that runs on **Windows, macOS, and Linux**
- A frontend that runs in any modern browser
- A future mobile app for **iOS and Android**
- A future desktop app for **macOS and Windows** (Tauri/Electron)

---

# 🎨 **Project Vision**

u‑sell‑it is transforming from a standalone PyQt6 desktop app into a **full‑stack, production‑ready marketplace platform** with:

- 🔐 Secure authentication
- 🛒 Item listings
- 📦 Local buying/selling
- 📱 Native mobile apps (iOS + Android)
- 🖥️ Desktop apps (macOS + Windows)
- 🧱 Clean, scalable architecture

This repo contains **both** the legacy desktop version and the new modern stack.

---

# 🧱 **Tech Stack**

<div align="center">

| Layer          | Technologies                               |
| -------------- | ------------------------------------------ |
| **Frontend**   | React, TypeScript, Tailwind, Vite          |
| **Backend**    | FastAPI, SQLAlchemy 2.0, Alembic, JWT      |
| **Database**   | PostgreSQL (Docker)                        |
| **Mobile**     | React Native (iOS + Android) — planned     |
| **Desktop**    | Tauri/Electron (macOS + Windows) — planned |
| **Legacy App** | PyQt6, C++, PostgreSQL                     |

</div>

---

# 📁 **Repository Structure**

```text
u-sell-it/
│
├── backend/                 # FastAPI backend (new)
│   ├── app/
│   ├── alembic/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/                # React + TypeScript frontend (coming soon)
│   ├── src/
│   ├── public/
│   └── package.json
│
├── desktop-legacy/          # Original PyQt6 + C++ prototype
│   ├── main.py
│   ├── assets/
│   ├── schema/
│   ├── DLL Files/
│   ├── linuxDemo/
│   ├── requirements.txt
│   └── README.md
│
├── docker-compose.yml       # Runs backend + database (+ frontend later)
├── .env                     # Environment variables (not committed)
└── README.md                # You are here
```

---

# 🔐 **Backend Features (FastAPI)**

### **Authentication**

- Email‑based registration
- Login
- JWT access token (24 hours)
- JWT refresh token (90 days)
- Password hashing (bcrypt)

### **User System**

- Create user
- Fetch user
- Protected routes (coming soon)

### **Item System**

- Create item
- List items
- Item ownership

### **Database**

- PostgreSQL
- SQLAlchemy 2.0
- Alembic migrations

### **API Docs**

- `/docs` → Swagger UI
- `/redoc` → ReDoc

---

# 🛠️ **Running the Backend (Windows/macOS/Linux)**

```bash
cd backend
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open API docs:  
👉 http://127.0.0.1:8000/docs

---

# 🐳 **Running Backend + PostgreSQL via Docker**

```bash
docker-compose up --build
```

This starts:

- PostgreSQL
- FastAPI backend
- (Frontend coming soon)

---

# 🖥️ **Legacy Desktop App (PyQt6 + C++)**

The original standalone desktop prototype is preserved in:

```
desktop-legacy/
```

Includes:

- PyQt6 UI
- C++ backend logic
- PostgreSQL schema
- Screenshots and design assets

This version remains functional and serves as a historical reference and portfolio piece.

---

# 🗺️ **Development Roadmap**

### **Phase 1 — Backend Foundation (In Progress)**

- ✔ FastAPI project structure
- ✔ JWT authentication
- ✔ User model + service
- ✔ Item model + service
- ⬜ Protected routes
- ⬜ Alembic migrations

### **Phase 2 — Frontend (React + TypeScript)**

- ⬜ Project scaffold
- ⬜ Login/Register pages
- ⬜ Auth context
- ⬜ API integration
- ⬜ Item listing UI

### **Phase 3 — Mobile Apps (iOS + Android)**

- ⬜ React Native scaffold
- ⬜ Mobile auth
- ⬜ Mobile item listing
- ⬜ Push notifications

### **Phase 4 — Desktop Apps (macOS + Windows)**

- ⬜ Tauri/Electron scaffold
- ⬜ Desktop UI
- ⬜ Local caching

### **Phase 5 — Deployment**

- ⬜ Deploy backend to Ubuntu VM
- ⬜ Deploy frontend
- ⬜ CI/CD pipeline

---

<div align="center">

# 🙌 **Author**

**Michael Rios**  
Junior Computer Science Major • Full‑Stack Developer • AI Engineer  
Texas A&M University–Victoria

</div>
