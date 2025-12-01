# 🤝 Contributing to u-sell-it

Thank you for your interest in contributing to **u-sell-it**! 🎉  
This project is a learning journey and portfolio piece, and contributions help make it stronger, more modular, and more beginner‑friendly.

---

## 🎯 Purpose of This Guide

The goal of this document is to provide clear instructions for collaborators around the world. Whether you’re new to GitHub or an experienced developer, this guide explains how to fork, branch, commit, and submit changes so we can build **u-sell-it** together.

---

## 📋 How to Contribute

### 1. Fork the repository
- Click the **Fork** button on GitHub to create your own copy of the repo.

### 2. Clone your fork locally
```bash
git clone https://github.com/<your-username>/u-sell-it.git
cd u-sell-it
```

### 3. Install dependencies
Make sure you have **Python 3.10+** installed. Then run:
```bash
pip install -r requirements.txt
```

### 4. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

### 5. Make your changes
- Keep code modular and well‑commented.  
- Follow the existing project structure (`demo/`, `assets/`, etc.).  
- If adding new dependencies, update `requirements.txt`.  
- Add screenshots or assets to the `assets/` folder.  

### 6. Commit your changes
```bash
git add .
git commit -m "Add: short description of your change"
```

### 7. Push your branch
```bash
git push origin feature/your-feature-name
```

### 8. Open a Pull Request (PR)
- Go to your fork on GitHub.  
- Click **Compare & pull request**.  
- Describe what you changed and why.  

---

## 🧾 Guidelines

- **Coding style**  
  - Python: follow [PEP8](https://peps.python.org/pep-0008/) conventions.  
  - C++: keep functions modular, documented, and consistent with existing DLL code.  

- **Documentation**  
  - Update `README.md` if your changes affect installation or usage.  
  - Add comments to explain logic, especially in demo mode code.  

- **Assets**  
  - Place images/icons in `assets/`.  
  - Keep filenames descriptive and consistent.  

---

## 🚀 Communication

- Use **GitHub Issues** to report bugs or request features.  
- Use **Pull Request comments** to discuss changes.  
- Contributions are welcome from anywhere in the world — GitHub keeps everything synced.  

---

## ✅ Code of Conduct

Be respectful, collaborative, and constructive. This project is about learning and building together.  
Harassment, discrimination, or toxic behavior will not be tolerated.  

---

## 🛠️ Local Development Quickstart

```bash
# Clone the repo
git clone https://github.com/KingNeoIV/u-sell-it.git
cd u-sell-it

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

---

## 📦 Adding Dependencies

If your feature requires new Python libraries:
1. Add them to `requirements.txt`.  
2. Run `pip freeze > requirements.txt` to update the file.  
3. Commit the updated file with your changes.  

---

## 🐛 Issue Templates

When opening an issue, please use one of the following formats:

### Bug Report
- **Description**: What went wrong?  
- **Steps to reproduce**: How can we replicate the bug?  
- **Expected behavior**: What should have happened?  
- **Screenshots/logs**: Optional but helpful.  

### Feature Request
- **Description**: What feature would you like to see?  
- **Why**: Why is this feature useful?  
- **Implementation ideas**: Optional suggestions for how to build it.  

---

Thank you for helping improve **u-sell-it**! 🙌  
Your contributions make this project better for everyone.