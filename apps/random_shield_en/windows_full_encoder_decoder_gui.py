import tkinter as tk
from tkinter import messagebox, scrolledtext
from core_encryptor import encode_message, decode_message

def parse_key(key_str):
    try:
        return [int(k.strip()) for k in key_str.split(',') if k.strip()]
    except ValueError:
        return None

def encode():
    key = parse_key(key_entry.get())
    if not key:
        messagebox.showerror("Invalid Key", "Key must be comma-separated integers.")
        return

    message = message_input.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Input Error", "Please enter a message to encode.")
        return

    try:
        noise = int(noise_entry.get())
        if noise < 1 or noise > 15:
            raise ValueError
    except ValueError:
        messagebox.showerror("Noise Error", "Noise must be a number between 1 and 15.")
        return

    result = encode_message(message, key, noise)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, result)

def decode():
    key = parse_key(key_entry.get())
    if not key:
        messagebox.showerror("Invalid Key", "Key must be comma-separated integers.")
        return

    encoded = message_input.get("1.0", tk.END).strip()
    if not encoded:
        messagebox.showerror("Input Error", "Please enter the encoded message.")
        return

    result = decode_message(encoded, key)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, result)

def copy_output():
    root.clipboard_clear()
    root.clipboard_append(output_display.get("1.0", tk.END))
    messagebox.showinfo("Copied", "Output copied to clipboard.")

def paste_input():
    try:
        text = root.clipboard_get()
        message_input.delete("1.0", tk.END)
        message_input.insert(tk.END, text)
    except tk.TclError:
        messagebox.showerror("Paste Error", "Clipboard does not contain text.")

root = tk.Tk()
root.title("Secure Encoder/Decoder")

tk.Label(root, text="Message / Encoded Input:").pack(anchor='w', padx=10)
message_input = scrolledtext.ScrolledText(root, width=80, height=10)
message_input.pack(padx=10, pady=5)

tk.Label(root, text="Key (comma-separated integers):").pack(anchor='w', padx=10)
key_entry = tk.Entry(root, width=50)
key_entry.pack(padx=10, pady=5)

tk.Label(root, text="Noise (1–15, used only for encoding):").pack(anchor='w', padx=10)
noise_entry = tk.Entry(root, width=10)
noise_entry.insert(0, "5")
noise_entry.pack(padx=10, pady=5)

button_frame = tk.Frame(root)
tk.Button(button_frame, text="Encode", command=encode).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Decode", command=decode).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Paste Input", command=paste_input).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Copy Output", command=copy_output).pack(side=tk.LEFT, padx=10)
button_frame.pack(pady=10)

tk.Label(root, text="Output:").pack(anchor='w', padx=10)
output_display = scrolledtext.ScrolledText(root, width=80, height=10)
output_display.pack(padx=10, pady=5)

root.mainloop()