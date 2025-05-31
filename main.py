import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from PyPDF2 import PdfReader, PdfWriter
import secrets
import string
import platform
import sv_ttk
import os
import sys
import darkdetect


VERSION = "Made for Matt with Love - v1.0.0"
def resource_path(relative_path):
    # Makes paths work with PyInstaller and regular runs
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def generate_password(length=12):
    charset = string.ascii_letters + string.digits
    return ''.join(secrets.choice(charset) for _ in range(length))

def encrypt_pdf(input_path, output_path, password):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    with open(output_path, 'wb') as f:
        writer.write(f)


def auto_generate_password():
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)




# GUI setup
root = tk.Tk()
root.title("PDFSeal - Seal Your PDF")
root.geometry("500x480")
root.iconbitmap(resource_path("visuals/icon.ico"))
# root.resizable(False, False)

# Theme
sv_ttk.set_theme(darkdetect.theme())
current_theme = ttk.Style().theme_use()

# Logo
LOGO_PNG = "visuals/logo.png"
image = Image.open(resource_path(LOGO_PNG))
image = image.resize((200,217), Image.Resampling.LANCZOS)  # adjust dimensions as needed, 170 for no title

logo_img = ImageTk.PhotoImage(image)
logo_label = tk.Label(root, image=logo_img)
logo_label.pack(pady=10)

def on_password_change(*args):
    # Enable the button only when password has content
    if password_var.get().strip():
        encrypt_button.config(state="normal")
    else:
        encrypt_button.config(state="disabled")

def handle_encrypt_click():
    input_path = filedialog.askopenfilename(
        title="Select PDF to Encrypt",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not input_path:
        return

    # Default to same name with "_encrypted" before the extension
    base, ext = os.path.splitext(input_path)
    default_name = f"{base}_encrypted{ext}"

    output_path = filedialog.asksaveasfilename(
        title="Save Encrypted PDF As",
        initialfile=os.path.basename(default_name),
        initialdir=os.path.dirname(input_path),
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not output_path:
        return

    try:
        encrypt_pdf(input_path, output_path, password_var.get().strip())
        show_success_popup(password_var.get().strip())
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed:\n{e}")

def center_popup(popup, parent):
    popup.update_idletasks()  # ensures geometry info is updated

    parent_x = parent.winfo_rootx()
    parent_y = parent.winfo_rooty()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()

    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()

    x = parent_x + (parent_width // 2) - (popup_width // 2)
    y = parent_y + (parent_height // 2) - (popup_height // 2)

    popup.geometry(f"+{x}+{y}")

def show_success_popup(password):
    popup = tk.Toplevel(root)
    popup.title("Success")
    popup.geometry("300x160")
    popup.resizable(False, False)
    popup.iconbitmap(resource_path("visuals/icon.ico"))
    center_popup(popup, root)


    ttk.Label(popup, text="PDF encrypted successfully!", font=("Segoe UI", 10)).pack(pady=(15, 5))
    ttk.Label(popup, text="⚠ Don't forget your password.", foreground="red").pack(pady=(0, 10))

    def copy_pw():
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        copy_btn.config(text="Copied!", state="disabled")
        popup.after(1000, popup.destroy)

    copy_btn = ttk.Button(popup, text="Copy Password", command=copy_pw)
    copy_btn.pack()

    ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=(10, 0))



def auto_generate_password():
    password = generate_password()
    password_var.set(password)

# Inside GUI setup
password_var = tk.StringVar()
password_var.trace_add("write", on_password_change)

ttk.Label(root, text="Password:").pack(pady=(10, 2))
# Create a custom font (e.g., size 14)
large_font = tkfont.Font(family="Segoe UI", size=14)

# Apply it to the password entry
password_entry = ttk.Entry(root, textvariable=password_var, width=20, font=large_font,  justify="center")
# password_entry = ttk.Entry(root, textvariable=password_var, width=30)
password_entry.pack(pady=5)

ttk.Button(root, text="Generate Password", command=auto_generate_password).pack(pady=5)

encrypt_button = ttk.Button(root, text="Encrypt PDF", state="disabled", command=handle_encrypt_click, style="Accent.TButton")
encrypt_button.pack(pady=20)


# Add version label with dark grey color and padding
version_label = ttk.Label(root, text=VERSION, font=("Segoe UI", 8), foreground="grey")
version_label.pack(pady=(20, 0))  # Add padding to move it down
root.mainloop()


