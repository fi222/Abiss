#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import hashlib
from password_prompt import show_password_prompt  # Move this below tkinter import

# Get absolute path to bundled resource
def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except AttributeError:
        return os.path.join(os.path.abspath("."), relative_path)

# Persistent storage in AppData\Roaming\TheAbyss\Vaults
APPDATA = os.getenv("APPDATA", os.path.expanduser("~"))
VAULT_DIR = os.path.join(APPDATA, "TheAbyss", "Vaults")
os.makedirs(VAULT_DIR, exist_ok=True)

ICON_BLUE = resource_path("Blue_folder.png")
ICON_AMBER = resource_path("Amber_folder.png")
ICON_SIZE = (64, 64)

def load_icon(path):
    try:
        return ImageTk.PhotoImage(Image.open(path).resize(ICON_SIZE))
    except Exception as e:
        print(f"❌ Failed to load icon {path}: {e}")
        return None

class FolderButton(tk.Frame):
    def __init__(self, master, label, controller, is_storage=False):
        super().__init__(master, padx=5, pady=5)
        self.ctrl = controller
        self.label = label

        icon_path = ICON_AMBER if is_storage else ICON_BLUE
        icon = load_icon(icon_path)

        btn = tk.Button(self, image=icon, text=label, compound="top",
                        width=ICON_SIZE[0], height=ICON_SIZE[1]+20, relief="flat")
        btn.image = icon
        btn.pack()

        if is_storage:
            btn.config(command=self.ctrl.open_storage)
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self.ctrl.on_drop)
        else:
            btn.config(command=lambda: self.ctrl.add_to_path(label))

class AbyssApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("The Abyss")
        self.path = []

        # UI elements
        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=(10, 2))

        self.status = tk.Label(self, text="Level: 0 | Path: (empty)", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(0, 2))

        self.hash_label = tk.Label(self, text="SHA256: ", anchor="w", fg="blue")
        self.hash_label.pack(fill="x", padx=10, pady=(0, 5))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=4)

        # Control buttons
        tk.Button(btn_frame, text="⬆ Up", command=self.go_up).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🏠 Root", command=self.go_root).pack(side="left", padx=5)

        # Folder grid
        for row in ["0123456789", "ABCDEFGHIJ", "KLMNOPQRS", "TUVWXYZ"]:
            frame = tk.Frame(self)
            frame.pack()
            for ch in row:
                FolderButton(frame, ch, controller=self).pack(side="left")

        # Storage
        FolderButton(self, "Storage", controller=self, is_storage=True).pack(pady=20)

        self.update_ui()

    def add_to_path(self, label):
        self.path.append(label)
        self.update_ui()

    def go_up(self):
        if self.path:
            self.path.pop()
        self.update_ui()

    def go_root(self):
        self.path.clear()
        self.update_ui()

    def update_ui(self):
        path_str = " > ".join(self.path) if self.path else "(empty)"
        self.status.config(text=f"Level: {len(self.path)} | Path: {path_str}")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, "/".join(self.path))
        self.hash_label.config(text=f"SHA256: {self.compute_hash()[:8]}...")

    def compute_hash(self):
        joined = "".join(self.path)
        return hashlib.sha256(joined.encode()).hexdigest()

    def get_vault_path(self):
        return os.path.join(VAULT_DIR, self.compute_hash())

    def on_drop(self, event):
        files = self.tk.splitlist(event.data)
        if not self.path:
            messagebox.showwarning("No Path", "Please build a path first.")
            return

        vault_path = self.get_vault_path()
        os.makedirs(vault_path, exist_ok=True)

        for file_path in files:
            try:
                shutil.copy2(file_path, vault_path)
                print(f"📦 Stored: {file_path}")
            except Exception as e:
                print(f"❌ Error storing {file_path}: {e}")

        messagebox.showinfo("Done", f"Stored {len(files)} file(s).")

    def open_storage(self):
        if not self.path:
            messagebox.showwarning("No Path", "Please build a path first.")
            return

        vault_path = self.get_vault_path()
        os.makedirs(vault_path, exist_ok=True)

        if sys.platform == "win32":
            os.startfile(vault_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", vault_path])
        else:
            subprocess.call(["xdg-open", vault_path])

if __name__ == "__main__":
    show_password_prompt()  # ← only call here, and AFTER all imports
    app = AbyssApp()
    app.mainloop()
