<p align="center">
  <img src="assets/u-sell-it_icon_black.png" width="200" alt="u-sell-it">
</p>

# 🛍️ u-sell-it (Standalone Desktop App)

**u-sell-it** is a standalone desktop application in active development, designed to help users buy, sell, and trade items locally. Built with a modular architecture and refined user interface, this app is the foundation for a scalable offline-first platform focused on community commerce.

---

## 🎯 Purpose

This project is designed for individuals who want to learn how to build their own desktop application while also setting up and managing a PostgreSQL database on Ubuntu. It’s a hands‑on learning experience that combines frontend development (PyQt6), backend logic (C++ DLL), and database management (PostgreSQL).

The goal is not only to serve as a personal learning journey, but also to provide a foundation for others who want to explore building standalone apps with modular architecture.

---

## 📚 Learning & Portfolio

For now, **u-sell-it** is a learning project — a way to practice connecting UI, backend, and database layers in a real application. Once the project matures and looks polished, it will also serve as part of my professional portfolio.

When the app reaches a stable and functional state, I plan to invest in services to officially publish it, making it fully functional and available for broader use.

---

## 🚧 Current Development Status

This project is still in its early stages:

- ✅ **Login screen** completed (PyQt6)
- 🔄 **Registration form** in progress
- 🧩 **Backend logic** written in C++ (DLL integration planned)
- 🗄️ **Database setup**: PostgreSQL installed on Ubuntu, schema design in progress

> Note: This is a desktop application, not a web-based `.com` platform.

---

## 🚀 Planned Features

- **Login/Register UI (PyQt6)**
  - Transparent overlays and professional layout
  - Two-column field arrangement for clarity and flow
  - Dynamic resizing and label positioning
  - Custom icons and assets for branded presentation

- **Backend Integration (C++ DLL)**
  - Secure function calls via statically linked `.dll`
  - Cross-language communication via `ctypes` or `cffi`
  - Modular backend design for future expansion

- **Database Connectivity (PostgreSQL)**
  - SQL-based schema for user accounts, item listings, and transactions
  - Designed to support both local and remote database configurations
  - Future integration with bidding logic and transaction history

- **Standalone Execution**
  - No internet required for core functionality
  - Lightweight and fast startup
  - Designed for future growth into a connected platform

---

## 🧱 Architecture

- **Frontend**: PyQt6  
- **Backend**: C++ (compiled into `.dll`)  
- **Database**: PostgreSQL (Ubuntu setup complete, schema design in progress)  
- **Design Philosophy**:
  - Modular components
  - Fully commented codebase
  - Separation of concerns
  - UI/UX refinement through iterative testing
  - Structured data management via normalized tables and secure queries

---

## 📦 Assets Included

- Login screen icons and layout files  
- Screenshot of the `.py` UI implementation  
- App icon (`u-sell-it-icon.png`)  

---

## 📥 Installation (Dev Mode)

If you're running from source:

```bash
git clone https://github.com/KingNeoIV/u-sell-it.git
cd u-sell-it
pip install -r requirements.txt
python main.py