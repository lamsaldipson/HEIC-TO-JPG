from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()

source = Path(r"D:\HEIC")
output = Path(r"D:\JPG")
output.mkdir(parents=True, exist_ok=True)

files = [
    p for p in source.rglob("*")
    if p.suffix.lower() == ".heic"
]

for index, file in enumerate(files, 1):
    try:
        relative = file.relative_to(source)
        destination = (output / relative).with_suffix(".jpg")
        destination.parent.mkdir(parents=True, exist_ok=True)

        with Image.open(file) as image:
            image = ImageOps.exif_transpose(image)
            image = image.convert("RGB")

            image.save(
                destination,
                "JPEG",
                quality=100,
                subsampling=0,
                exif=image.getexif().tobytes()
            )

        print(f"[{index}/{len(files)}] Converted: {file.name}")

    except Exception as e:
        print(f"Error: {file.name}: {e}")

print("Conversion finished!")