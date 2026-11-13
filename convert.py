from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()


def convert_heic_to_jpg(files, output_folder):

    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)

    converted = 0
    failed = 0

    for index, file in enumerate(files, 1):
        try:
            source = Path(file)

            destination = output / (source.stem + ".jpg")

            # Avoid overwriting existing images
            number = 1

            while destination.exists():
                destination = output / f"{source.stem}_{number}.jpg"
                number += 1

            with Image.open(source) as image:
                image = ImageOps.exif_transpose(image)

                exif_data = image.getexif().tobytes()

                image = image.convert("RGB")

                image.save(
                    destination,
                    "JPEG",
                    quality=100,
                    subsampling=0,
                    exif=exif_data
                )

            converted += 1
            print(f"[{index}/{len(files)}] Converted: {source.name}")

        except Exception as error:
            failed += 1
            print(f"Error: {file.name if isinstance(file, Path) else file}")
            print(error)

    return converted, failed