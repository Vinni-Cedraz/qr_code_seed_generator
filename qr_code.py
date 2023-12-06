import subprocess
import tkinter as tk
import qrcode
from PIL import Image, ImageTk

seed = ''  # Global variable to store the seed


def generate_key():
    subprocess.run(["python3", "ft_totp.py", "-g", "key.txt"])


def generate_qr():
    global seed  # Update the seed global variable
    subprocess.run(["python3", "ft_totp.py", "-k", "key.txt"])

    # Generate QR code from the TOTP seed and save it as an image
    with open('key.txt', 'r') as file:
        seed = subprocess.run(
            ["python3", "ft_totp.py", "-k", file.name],
            capture_output=True, text=True).stdout.strip()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, border=4
    )
    qr.add_data(seed)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qrcode.png')  # Save QR code image

    # Display the QR code image in the GUI
    qr_img = Image.open('qrcode.png')
    qr_img = qr_img.resize((200, 200), Image.BILINEAR)
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    label_qr.config(image=qr_img_tk)
    label_qr.image = qr_img_tk


def display_otp():
    global seed  # Update the seed global variable
    otp = subprocess.run(
        ["python3", "ft_totp.py", "-k", "key.txt"],
        capture_output=True, text=True).stdout.strip()

    label_otp.config(text=f"PASSWORD: {otp}")
    # Display the generated PASSWORD in the GUI
    seed = otp  # Update seed with the new PASSWORD


# Create GUI
root = tk.Tk()

root.title("TOTP Generator")

btn_generate_key = tk.Button(root, text="Generate Key", command=generate_key)
btn_generate_key.pack()

btn_generate_qr = tk.Button(root, text="Generate QR Code", command=generate_qr)
btn_generate_qr.pack()

label_qr = tk.Label(root)
label_qr.pack()

btn_display_otp = tk.Button(root, text="Display PASSWORD", command=display_otp)
btn_display_otp.pack()

label_otp = tk.Label(root, text="PASSWORD: ")
label_otp.pack()

# Run the GUI
root.mainloop()
