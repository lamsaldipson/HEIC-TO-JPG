# HEIC to JPEG Converter

I built this little Windows app to make converting HEIC photos to JPEGs easier. Instead of converting images one at a time, you can select a bunch of them, choose where you want the results saved, and let the app handle the rest.

It's made with **Python** and **CustomTkinter**, with a simple interface that keeps everything in one place.

## What it can do

- **Convert multiple photos at once.** Add `.heic` and `.heif` files using the Browse Files button.
- **Rename files before converting.** Click the pencil next to a photo, type the JPEG name you want, then press Enter or click the checkmark. You can edit the name right in the list—no extra popup.
- **Remove photos from the list.** Use the small X beside a file or Clear All to start over.
- **Choose where to save them.** The folder picker appears when you click Convert to JPEG.
- **Handle duplicate names.** If a JPEG with the same name already exists—or two selected photos would use the same output name—you can rename, replace, or skip it. There are also options for handling several conflicts together.
- **Follow the progress.** A progress bar shows how the conversion is going. When the batch finishes, the app shows **Done 👍** and returns to an empty selection after about two seconds.

The original HEIC files are left alone. JPEGs are saved at quality 100 with chroma subsampling disabled, and EXIF metadata is kept where supported. Keep in mind that JPEG is still a *lossy* format, so quality 100 doesn't make it truly lossless. Some HEIC features, such as HDR, might not carry over perfectly.

## Getting started

You'll need **Windows 10 or 11**, Python, and a few Python packages. Make sure the packages you install support your Python version.

Open PowerShell in the project folder and install the dependencies:

```powershell
py -m pip install customtkinter Pillow pillow-heif
```

Then start the app:

```powershell
py main.py
```

That's it—the converter should open in its own window.

### Project files

```text
Heic to Jpg/
├── main.py       # The interface, rename controls, conflict screen and progress bar
├── convert.py    # Reads HEIC/HEIF images and saves JPEGs
└── README.md
```

If you're using the files from **Step 2**, rename `main_step2.py` to `main.py` and `convert_step2.py` to `convert.py`. Keep them in the same folder.

## How to use it

1. Open the app and click **+ Browse Files** to add your images.
2. Want a different output name? Click **✎** beside the image, edit the name in place, and click **✓** (or press Enter).
3. Click **Convert to JPEG** and pick a folder for the finished images. The button stays disabled if you haven't selected anything.
4. If the app finds duplicate filenames, choose what to do:
   - **Rename** keeps the existing file and gives the new JPEG another name. Automatic names can look like `IMG_5555_1.jpg`.
   - **Replace** overwrites the existing destination JPEG after confirmation.
   - **Skip** leaves that image out of the conversion.
5. Watch the progress bar. Once the batch finishes, the app returns to the empty selection screen so you can start another batch.

For example, you could select `IMG_5555.HEIC`, rename its output to `Holiday Photo`, and get `Holiday Photo.jpg`. Your original HEIC photo is not renamed or deleted.

## A note about replacing files

**Replace really does overwrite the JPEG that's already in your destination folder.** There isn't an undo button for that, so I'd recommend trying it with test photos first. If you want to keep both images, choose Rename instead.

The converter checks output names before starting and avoids silently overwriting a newly conflicting name during a normal save. It also uses a temporary output file to reduce the chance of leaving an incomplete JPEG behind if something goes wrong.

## If something goes wrong

**The app says `ModuleNotFoundError`.** You're probably missing a dependency or installed it for a different Python interpreter. Try running:

```powershell
py -m pip install customtkinter Pillow pillow-heif
```

**Python shows `IndentationError`.** Check the indentation in your code—Python uses spaces to determine which lines belong together. You can check both source files without launching the window:

```powershell
py -m py_compile main.py convert.py
```

