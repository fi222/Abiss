# secure_encoder_gui_he.py
import tkinter as tk
from tkinter import messagebox, scrolledtext
from core_encryptor_hebrew import encode_message, decode_message

# Translations
translations = {
    'en': {
        'title': 'Secure Encoder/Decoder (Hebrew Enabled)',
        'msg_input': 'Message / Encoded Input:',
        'key_label': 'Key (comma-separated integers):',
        'noise_label': 'Noise (1–15, used only for encoding):',
        'encode': 'Encode',
        'decode': 'Decode',
        'paste_input': 'Paste Input',
        'copy_output': 'Copy Output',
        'output_label': 'Output:',
        'error_invalid_key_title': 'Invalid Key',
        'error_invalid_key_msg': 'Key must be comma-separated integers.',
        'error_input_error_title': 'Input Error',
        'error_input_error_msg_encode': 'Please enter a message to encode.',
        'error_input_error_msg_decode': 'Please enter the encoded message to decode.',
        'error_noise_error_title': 'Noise Error',
        'error_noise_error_msg': 'Noise must be a number between 1 and 15.',
        'info_copied_title': 'Copied',
        'info_copied_msg': 'Output copied to clipboard.',
        'error_paste_title': 'Paste Error',
        'error_paste_msg': 'Clipboard does not contain text.',
    },
    'he': {
        'title': 'מקודד/מפענח מאובטח (עברית)',
        'msg_input': 'הודעה / קלט מקודד:',
        'key_label': 'מפתח (מספרים מופרדים בפסיקים):',
        'noise_label': 'רעש (1–15, להצפנה בלבד):',
        'encode': 'הצפן',
        'decode': 'פענח',
        'paste_input': 'הדבק קלט',
        'copy_output': 'העתק פלט',
        'output_label': 'פלט:',
        'error_invalid_key_title': 'מפתח שגוי',
        'error_invalid_key_msg': 'המפתח חייב להיות מספרים מופרדים בפסיקים.',
        'error_input_error_title': 'שגיאת קלט',
        'error_input_error_msg_encode': 'אנא הזן הודעה להצפנה.',
        'error_input_error_msg_decode': 'אנא הזן הודעה מקודדת לפענוח.',
        'error_noise_error_title': 'שגיאת רעש',
        'error_noise_error_msg': 'הרעש חייב להיות מספר בין 1 ל-15.',
        'info_copied_title': 'הועתק',
        'info_copied_msg': 'הפלט הועתק ללוח.',
        'error_paste_title': 'שגיאת הדבקה',
        'error_paste_msg': 'הלוח אינו מכיל טקסט.',
    }
}

def parse_key(key_str):
    try:
        return [int(k.strip()) for k in key_str.split(',') if k.strip()]
    except ValueError:
        return None

def set_language(lang):
    global current_lang
    current_lang = lang
    root.title(translations[lang]['title'])
    msg_label.config(text=translations[lang]['msg_input'], bg=bg_color)
    key_label.config(text=translations[lang]['key_label'], bg=bg_color)
    noise_label.config(text=translations[lang]['noise_label'], bg=bg_color)
    output_label.config(text=translations[lang]['output_label'], bg=bg_color)
    encode_button.config(text=translations[lang]['encode'])
    decode_button.config(text=translations[lang]['decode'])
    paste_button.config(text=translations[lang]['paste_input'])
    copy_button.config(text=translations[lang]['copy_output'])
    justify = 'right' if lang == 'he' else 'left'
    message_input.tag_configure('all', justify=justify)
    output_display.tag_configure('all', justify=justify)
    key_entry.config(justify=justify)
    noise_entry.config(justify=justify)
    message_input.tag_add('all', '1.0', tk.END)
    output_display.tag_add('all', '1.0', tk.END)

def encode():
    lang = current_lang
    key = parse_key(key_entry.get())
    if not key:
        messagebox.showerror(translations[lang]['error_invalid_key_title'],
                             translations[lang]['error_invalid_key_msg'])
        return
    message = message_input.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror(translations[lang]['error_input_error_title'],
                             translations[lang]['error_input_error_msg_encode'])
        return
    try:
        noise = int(noise_entry.get())
        if noise < 1 or noise > 15:
            raise ValueError
    except ValueError:
        messagebox.showerror(translations[lang]['error_noise_error_title'],
                             translations[lang]['error_noise_error_msg'])
        return
    result = encode_message(message, key, noise)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, result, 'all')

def decode():
    lang = current_lang
    key = parse_key(key_entry.get())
    if not key:
        messagebox.showerror(translations[lang]['error_invalid_key_title'],
                             translations[lang]['error_invalid_key_msg'])
        return
    encoded = message_input.get("1.0", tk.END).strip()
    if not encoded:
        messagebox.showerror(translations[lang]['error_input_error_title'],
                             translations[lang]['error_input_error_msg_decode'])
        return
    result = decode_message(encoded, key)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, result, 'all')

def copy_output():
    lang = current_lang
    root.clipboard_clear()
    root.clipboard_append(output_display.get("1.0", tk.END))
    messagebox.showinfo(translations[lang]['info_copied_title'],
                        translations[lang]['info_copied_msg'])

def paste_input():
    lang = current_lang
    try:
        text = root.clipboard_get()
        message_input.delete("1.0", tk.END)
        message_input.insert(tk.END, text, 'all')
    except tk.TclError:
        messagebox.showerror(translations[lang]['error_paste_title'],
                             translations[lang]['error_paste_msg'])

# === GUI Setup ===
bg_color = '#d4ebf2'  # Light blue background

root = tk.Tk()
root.configure(bg=bg_color)
current_lang = 'en'

lang_var = tk.StringVar(value=current_lang)
lang_menu = tk.OptionMenu(root, lang_var, *translations.keys(), command=set_language)
lang_menu.config(bg='white')
lang_menu.pack(anchor='ne', padx=10, pady=5)

msg_label = tk.Label(root, text='', bg=bg_color)
msg_label.pack(anchor='w', padx=10)
message_input = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD)
message_input.tag_configure('all', justify='left')
message_input.pack(padx=10, pady=5)

key_label = tk.Label(root, text='', bg=bg_color)
key_label.pack(anchor='w', padx=10)
key_entry = tk.Entry(root, width=50, justify='left')
key_entry.pack(padx=10, pady=5)

noise_label = tk.Label(root, text='', bg=bg_color)
noise_label.pack(anchor='w', padx=10)
noise_entry = tk.Entry(root, width=10, justify='left')
noise_entry.insert(0, "5")
noise_entry.pack(padx=10, pady=5)

button_frame = tk.Frame(root, bg=bg_color)
encode_button = tk.Button(button_frame, text='', command=encode)
encode_button.pack(side=tk.LEFT, padx=10)
decode_button = tk.Button(button_frame, text='', command=decode)
decode_button.pack(side=tk.LEFT, padx=10)
paste_button = tk.Button(button_frame, text='', command=paste_input)
paste_button.pack(side=tk.LEFT, padx=10)
copy_button = tk.Button(button_frame, text='', command=copy_output)
copy_button.pack(side=tk.LEFT, padx=10)
button_frame.pack(pady=10)

output_label = tk.Label(root, text='', bg=bg_color)
output_label.pack(anchor='w', padx=10)
output_display = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD)
output_display.tag_configure('all', justify='left')
output_display.pack(padx=10, pady=5)

set_language(current_lang)
root.mainloop()
