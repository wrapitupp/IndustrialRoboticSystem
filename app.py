# app.py
# Part b) + Part c) - Software application + Event driven database integration

import tkinter as tk
from tkinter import messagebox
from robot import IndustrialRobot
from database import RobotDatabase

# --- Setup ---
robot = IndustrialRobot("RoboArm-1")
db = RobotDatabase()

# --- Main Window ---
window = tk.Tk()
window.title("Industrial Robot Control Panel")
window.geometry("500x580")
window.config(bg="#1e1e2e")

# --- Title ---
title = tk.Label(window, text="🤖 Robot Control Panel",
                 font=("Arial", 18, "bold"),
                 bg="#1e1e2e", fg="#cdd6f4")
title.pack(pady=15)

# --- Status Display ---
status_var = tk.StringVar()
status_var.set("Status: Idle | Position: (0,0,0) | Holding: Nothing")

status_label = tk.Label(window, textvariable=status_var,
                        font=("Arial", 10),
                        bg="#313244", fg="#a6e3a1",
                        wraplength=460, pady=8)
status_label.pack(fill="x", padx=20)

# --- Function to refresh status display ---
def refresh_status():
    s = robot.get_status()
    holding = s["holding"] if s["holding"] else "Nothing"
    status_var.set(
        f"Status: {s['status'].capitalize()} | "
        f"Position: {s['position']} | "
        f"Holding: {holding}"
    )

# --- Log Box function (defined early so other functions can use it) ---
def log(message):
    log_box.config(state="normal")
    log_box.insert("end", f"→ {message}\n")
    log_box.see("end")
    log_box.config(state="disabled")

# --- Section: Move Robot ---
move_frame = tk.LabelFrame(window, text=" Move Robot ",
                            bg="#1e1e2e", fg="#89b4fa",
                            font=("Arial", 11, "bold"), padx=10, pady=10)
move_frame.pack(fill="x", padx=20, pady=10)

coords = {}
for axis in ["X", "Y", "Z"]:
    row = tk.Frame(move_frame, bg="#1e1e2e")
    row.pack(fill="x", pady=3)
    tk.Label(row, text=f"{axis}:", width=4,
             bg="#1e1e2e", fg="white").pack(side="left")
    entry = tk.Entry(row, width=10)
    entry.insert(0, "0")
    entry.pack(side="left", padx=5)
    coords[axis] = entry

def move_robot():
    try:
        x = int(coords["X"].get())
        y = int(coords["Y"].get())
        z = int(coords["Z"].get())
        robot.move_to(x, y, z)
        refresh_status()
        db.log_event("MOVE", f"Moved to ({x},{y},{z})", robot.position, "success")
        log(f"Moved to ({x}, {y}, {z})")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for X, Y, Z")

tk.Button(move_frame, text="▶ Move Robot",
          command=move_robot,
          bg="#89b4fa", fg="#1e1e2e",
          font=("Arial", 10, "bold"), pady=5).pack(pady=5)

# --- Section: Pick Item ---
pick_frame = tk.LabelFrame(window, text=" Pick Item ",
                            bg="#1e1e2e", fg="#a6e3a1",
                            font=("Arial", 11, "bold"), padx=10, pady=10)
pick_frame.pack(fill="x", padx=20, pady=5)

item_entry = tk.Entry(pick_frame, width=25)
item_entry.insert(0, "Metal Part")
item_entry.pack(side="left", padx=5)

def pick_item():
    item = item_entry.get().strip()
    if not item:
        messagebox.showerror("Error", "Please enter an item name")
        return
    result = robot.pick(item)
    if not result:
        messagebox.showwarning("Warning", f"Robot is already holding: {robot.holding_item}")
    else:
        db.log_event("PICK", f"Picked {item}", robot.position, "success")
        log(f"Picked up: {item}")
    refresh_status()

tk.Button(pick_frame, text="🤏 Pick",
          command=pick_item,
          bg="#a6e3a1", fg="#1e1e2e",
          font=("Arial", 10, "bold")).pack(side="left", padx=5)

# --- Section: Place Item ---
place_frame = tk.LabelFrame(window, text=" Place Item ",
                             bg="#1e1e2e", fg="#f38ba8",
                             font=("Arial", 11, "bold"), padx=10, pady=10)
place_frame.pack(fill="x", padx=20, pady=5)

def place_item():
    result = robot.place()
    if not result:
        messagebox.showwarning("Warning", "Robot is not holding anything!")
    else:
        db.log_event("PLACE", f"Placed item at {robot.position}", robot.position, "success")
        log(f"Placed item at {robot.position}")
    refresh_status()

tk.Button(place_frame, text="📦 Place Item",
          command=place_item,
          bg="#f38ba8", fg="#1e1e2e",
          font=("Arial", 10, "bold"), pady=5).pack()

# --- Log Box ---
log_frame = tk.LabelFrame(window, text=" Action Log ",
                           bg="#1e1e2e", fg="#cdd6f4",
                           font=("Arial", 11, "bold"), padx=10, pady=5)
log_frame.pack(fill="both", padx=20, pady=10, expand=True)

log_box = tk.Text(log_frame, height=6, bg="#181825",
                  fg="#cdd6f4", font=("Courier", 9), state="disabled")
log_box.pack(fill="both", expand=True)

# --- Close database when window is closed ---
def on_close():
    db.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)

log("Robot app started. Ready for commands.")

# --- Start App ---
window.mainloop()