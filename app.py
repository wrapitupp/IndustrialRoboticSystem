# app.py
# Full integration: GUI + Robot + Database + PyBullet Simulator

import tkinter as tk
from tkinter import messagebox
from robot import IndustrialRobot
from database import RobotDatabase
from simulator import RobotSimulator

# --- Setup ---
robot = IndustrialRobot("RoboArm-1")
db = RobotDatabase()
sim = RobotSimulator()  # This opens the 3D window immediately!

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

# --- Refresh Status ---
def refresh_status():
    s = robot.get_status()
    holding = s["holding"] if s["holding"] else "Nothing"
    status_var.set(
        f"Status: {s['status'].capitalize()} | "
        f"Position: {s['position']} | "
        f"Holding: {holding}"
    )

# --- Log function ---
def log(message):
    log_box.config(state="normal")
    log_box.insert("end", f"→ {message}\n")
    log_box.see("end")
    log_box.config(state="disabled")

# --- Move Robot ---
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
        robot.move_to(x, y, z)       # Update robot state
        sim.move_to(x, y, z)         # Move 3D arm!
        refresh_status()
        db.log_event("MOVE", f"Moved to ({x},{y},{z})", robot.position, "success")
        log(f"Moved to ({x}, {y}, {z})")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for X, Y, Z")

tk.Button(move_frame, text="▶ Move Robot",
          command=move_robot,
          bg="#89b4fa", fg="#1e1e2e",
          font=("Arial", 10, "bold"), pady=5).pack(pady=5)

# --- Pick Item ---
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
        messagebox.showwarning("Warning", f"Already holding: {robot.holding_item}")
    else:
        sim.pick(item)               # 3D arm picks!
        db.log_event("PICK", f"Picked {item}", robot.position, "success")
        log(f"Picked up: {item}")
    refresh_status()

tk.Button(pick_frame, text="🤏 Pick",
          command=pick_item,
          bg="#a6e3a1", fg="#1e1e2e",
          font=("Arial", 10, "bold")).pack(side="left", padx=5)

# --- Place Item ---
place_frame = tk.LabelFrame(window, text=" Place Item ",
                             bg="#1e1e2e", fg="#f38ba8",
                             font=("Arial", 11, "bold"), padx=10, pady=10)
place_frame.pack(fill="x", padx=20, pady=5)

def place_item():
    result = robot.place()
    if not result:
        messagebox.showwarning("Warning", "Robot is not holding anything!")
    else:
        sim.place()                  # 3D arm places!
        db.log_event("PLACE", f"Placed at {robot.position}", robot.position, "success")
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

# --- Close everything cleanly ---
def on_close():
    db.close()
    sim.disconnect()    # Close 3D window too
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)

log("Robot app started with PyBullet simulation!")

# --- Start ---
window.mainloop()