import customtkinter as ctk
from tkinter import filedialog 
from PIL import Image, ImageChops
from pillow_heif import register_heif_opener
from pathlib import Path
selected_files = []
register_heif_opener()


app = ctk.CTk()

app.title("HEIC to JPEG Converter")
app.geometry("700x650")

heading = ctk.CTkLabel(
    app,
    text="HEIC TO JPEG",
    font=("Arial", 35, "bold")
    
)
heading.pack(pady=(60,10))

subtitle = ctk.CTkLabel(
    app,
    text="Convert your HEIC photos to high-quality JPEG images with ease.",
    font=("Arial", 15)
)
subtitle.pack(pady=10)

def choose_files():
    files = filedialog.askopenfilenames(
        title="Select HEIC Images",
        filetypes=[
            ("HEIC Images", "*.heic *.heif")
        ]
    )

    if files:
        selected_files.clear()
        selected_files.extend(files)

        file_list.delete("1.0", "end")

        for file in selected_files:
            file_list.insert("end", file + "\n")


def convert_images():
    if not selected_files:
        print("Please select HEIC images first.")
        return

    output_folder = filedialog.askdirectory(
        title="Choose output folder"
    )

    if not output_folder:
        print("No output folder selected.")
        return

    print("Selected output folder:", output_folder)

    output_label.configure(
        text="Output folder: " + output_folder
    )

    print("Images ready for conversion:", len(selected_files))

choose_button = ctk.CTkButton(
    app,
    text="Choose Files",
    width=180,
    height=45,
    command=choose_files
)

choose_button.pack(pady=30)
    
file_list = ctk.CTkTextbox(
    app,
    width=500,
    height=150
)

file_list.pack(pady=10)

convert_button = ctk.CTkButton(
    app,
    text="Convert to JPEG",
    width=200,
    height=45,
    command=convert_images
)

convert_button.pack(pady=20)

output_label = ctk.CTkLabel(
    app,
    text="Output Folder: Not selected",
    font=("Arial", 12)
)
output_label.pack(pady=10)

    
app.mainloop()
