import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from threading import Thread
from queue import Queue, Empty

from convert import convert_heic_to_jpg


ctk.set_appearance_mode("light")

BLUE = "#2563EB"
BLUE_HOVER = "#1D4ED8"
WHITE = "#FFFFFF"
TEXT = "#111827"
MUTED = "#64748B"
BORDER = "#303044"

selected_files = []
events = Queue()
converting = False

app = ctk.CTk()
app.title("HEIC to JPEG Converter")
app.geometry("900x700")
app.minsize(480, 480)
app.resizable(True, True)
app.configure(fg_color=WHITE)



def update_files():
    for widget in file_container.winfo_children():
        widget.destroy()

    count_label.configure(
        text=f"{len(selected_files)} files selected"
    )

    convert_button.configure(
        state="normal" if selected_files and not converting
        else "disabled"
    )

    if not selected_files:
        ctk.CTkLabel(
            file_container,
            text="No images selected yet",
            text_color=MUTED
        ).pack(pady=35)
        return

    for file in selected_files:
        row = ctk.CTkFrame(
            file_container,
            fg_color="#F7F9FC",
            corner_radius=8
        )
        row.pack(fill="x", padx=5, pady=3)

        ctk.CTkLabel(
            row,
            text=Path(file).name,
            text_color=TEXT,
            anchor="w"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=12,
            pady=8
        )

        ctk.CTkButton(
            row,
            text="Remove",
            width=70,
            height=28,
            fg_color="#FEE2E2",
            hover_color="#FECACA",
            text_color="#B91C1C",
            command=lambda f=file: remove_file(f)
        ).pack(side="right", padx=8)


def choose_files():
    if converting:
        return

    files = filedialog.askopenfilenames(
        title="Select HEIC Images",
        filetypes=[
            ("HEIC Images", "*.heic *.heif")
        ]
    )

    for file in files:
        if file not in selected_files:
            selected_files.append(file)

    update_files()


def remove_file(file):
    if converting:
        return

    if file in selected_files:
        selected_files.remove(file)

    update_files()


def clear_files():
    if converting:
        return

    selected_files.clear()
    update_files()



def start_conversion():
    global converting

    if converting or not selected_files:
        return


    folder = filedialog.askdirectory(
        title="Choose where to save JPEG images"
    )

    if not folder:
        return

    converting = True

    browse_button.configure(state="disabled")
    clear_button.configure(state="disabled")
    convert_button.configure(state="disabled")

    update_files()

    files_card.pack_forget()

    progress_card.pack(
        fill="both",
        expand="True",
        pady=(0, 15)
    )

    progress_bar.set(0)
    progress_label.configure(text="Converting... 0%")
    counter_label.configure(
        text=f"0 / {len(selected_files)} images"
    )

    files_to_convert = selected_files.copy()

    Thread(
        target=conversion_worker,
        args=(files_to_convert, folder),
        daemon=True
    ).start()


def conversion_worker(files, folder):
    try:
        def report_progress(current, total):
            events.put(("progress", current, total))

        converted, failed = convert_heic_to_jpg(
            files,
            folder,
            progress_callback=report_progress
        )

        events.put(("done", converted, failed))

    except Exception as error:
        events.put(("error", str(error)))


def check_events():
    try:
        while True:
            event = events.get_nowait()

            if event[0] == "progress":
                _, current, total = event

                percentage = current / total if total else 0

                progress_bar.set(percentage)

                progress_label.configure(
                    text=f"Converting... {percentage:.0%}"
                )

                counter_label.configure(
                    text=f"{current} / {total} images"
                )

            elif event[0] == "done":
                _, converted, failed = event

                progress_bar.set(1)

                if failed == 0:
                    progress_label.configure(
                        text="Done 👍",
                        text_color="#15803D"
                    )
                else:
                    progress_label.configure(
                        text=f"Done 👍  {converted} converted, "
                             f"{failed} failed",
                        text_color="#B45309"
                    )

                
                app.after(2000, reset_screen)

            elif event[0] == "error":
                progress_label.configure(
                    text="Conversion failed: " + event[1],
                    text_color="#DC2626"
                )
                app.after(2000, reset_screen)

    except Empty:
        pass

    app.after(100, check_events)


def reset_screen():
    global converting

    converting = False

    progress_card.pack_forget()

    files_card.pack(
        fill="x",
        pady=(0, 25)
    )

    browse_button.configure(state="normal")
    clear_button.configure(state="normal")

    update_files()




main = ctk.CTkFrame(
    app,
    fg_color="transparent"
)
main.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=12
)

bottom_frame = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

bottom_frame.pack(
    side="bottom",
    fill="x",
    padx=20,
    pady=(0, 15)
)

ctk.CTkLabel(
    main,
    text="HEIC To JPEG",
    font=("Arial", 38, "bold"),
    text_color="#000000"
).pack(pady=(0, 10))

ctk.CTkLabel(
    main,
    text="Convert your images quickly, privately, and in high quality",
    font=("Arial", 16, "bold"),
    text_color=TEXT
).pack(pady=(0, 25))


upload_card = ctk.CTkFrame(
    main,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER,
    corner_radius=16
)
upload_card.pack(fill="x", pady=(0, 25))

ctk.CTkLabel(
    upload_card,
    text="↑",
    font=("Arial", 32),
    text_color=BLUE
).pack(pady=(10, 0))

ctk.CTkLabel(
    upload_card,
    text="Add your HEIC images",
    font=("Arial", 19, "bold"),
    text_color=TEXT
).pack()

ctk.CTkLabel(
    upload_card,
    text="Select one or multiple HEIC / HEIF images",
    font=("Arial", 12),
    text_color=MUTED
).pack(pady=5)

browse_button = ctk.CTkButton(
    upload_card,
    text="+ Browse Files",
    width=180,
    height=42,
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    command=choose_files
)
browse_button.pack(pady=(10, 15))



files_card = ctk.CTkFrame(
    main,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER,
    corner_radius=16
)
files_card.pack(fill="x", pady=(0, 25))

files_header = ctk.CTkFrame(
    files_card,
    fg_color="transparent"
)
files_header.pack(fill="x", padx=20, pady=(12, 5))

ctk.CTkLabel(
    files_header,
    text="Selected Images",
    font=("Arial", 15, "bold"),
    text_color=TEXT
).pack(side="left")

clear_button = ctk.CTkButton(
    files_header,
    text="Clear All",
    width=80,
    height=28,
    fg_color="#F1F5F9",
    text_color=TEXT,
    hover_color="#E2E8F0",
    command=clear_files
)
clear_button.pack(side="right")

count_label = ctk.CTkLabel(
    files_card,
    text="0 files selected",
    text_color=MUTED,
    font=("Arial", 11)
)
count_label.pack(anchor="w", padx=20)

file_container = ctk.CTkScrollableFrame(
    files_card,
    fg_color="transparent",
    height=140
)
file_container.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(5, 12)
)



progress_card = ctk.CTkFrame(
    main,
    fg_color=WHITE,
    border_width=1,
    border_color=BORDER,
    corner_radius=16
)

progress_label = ctk.CTkLabel(
    progress_card,
    text="Converting... 0%",
    font=("Arial", 20, "bold"),
    text_color=TEXT
)
progress_label.pack(pady=(25, 10))

progress_bar = ctk.CTkProgressBar(
    progress_card,
    height=12,
    progress_color=BLUE
)
progress_bar.pack(
    fill="x",
    padx=30,
    pady=10
)
progress_bar.set(0)

counter_label = ctk.CTkLabel(
    progress_card,
    text="0 / 0 images",
    text_color=MUTED
)
counter_label.pack(pady=(0, 25))



convert_button = ctk.CTkButton(
    bottom_frame,
    text="Convert to JPEG",
    height=65,
    font=("Arial", 22, "bold"),
    fg_color=BLUE,
    hover_color=BLUE_HOVER,
    corner_radius=12,
    command=start_conversion
)
convert_button.pack(
    fill="x",
    padx=10,
    pady=(0, 10)
)

update_files()

app.after(100, check_events)

def on_resize(event):
    if event.widget != app:
        return

    width = app.winfo_width()

    if width < 650:
        title_font = ("Arial", 26, "bold")
        padding = 10
    else:
        title_font = ("Arial", 38, "bold")
        padding = 20

    main.configure(
        
    )

    
    for widget in main.winfo_children():
        if isinstance(widget, ctk.CTkLabel):
            if widget.cget("text") == "HEIC To JPEG":
                widget.configure(font=title_font)
                
app.bind("<Configure>", on_resize)

app.mainloop()