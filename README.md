# 🤖 Industrial Robot Control System

A Python-based industrial robot control application built as part of a software programming assignment.

---

## 📦 What's Inside

| File            | Description                          |
| --------------- | ------------------------------------ |
| `robot.py`      | Core robot logic (move, pick, place) |
| `app.py`        | GUI control panel                    |
| `database.py`   | Event logging database               |
| `simulator.py`  | 3D PyBullet robot simulation         |
| `test_robot.py` | Performance tests                    |

---

## ▶️ How to Run

**1. Clone the repo:**

```bash
git clone THE_REPO_URL
cd robot_project
```

**2. Create and activate virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies:**

```bash
pip install pybullet
```

**4. Run the app:**

```bash
python app.py
```

Two windows will open — the control panel and a live 3D robot simulation.

---

## 🛠️ Built With

- Python
- Tkinter — GUI
- SQLite — Event database
- PyBullet — 3D robot simulation
