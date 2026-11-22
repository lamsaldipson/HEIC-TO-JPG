from pathlib import Path
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
import os
import tempfile

register_heif_opener()


def convert_heic_to_jpg(jobs, output_folder, progress_callback=None):
    """jobs: iterable of (source_path, destination_filename, action).

    action is 'new', 'replace', or 'skip'. The caller resolves conflicts first.
    """
    output = Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)
    converted = failed = skipped = 0
    jobs = list(jobs)
    total = len(jobs)
    for index, (source, filename, action) in enumerate(jobs, 1):
        temporary = None
        created_target = None
        try:
            if action == 'skip':
                skipped += 1
                continue
            target = output / filename
            if (target.parent.resolve() != output.resolve()
                    or target.suffix.lower() not in ('.jpg', '.jpeg')
                    or target.name != filename):
                raise ValueError('Invalid destination filename')
            if action == 'new' and target.exists():
                raise FileExistsError(f'{target.name} already exists')
            if action not in ('new', 'replace'):
                raise ValueError('Unknown conversion action')
            # Write the JPEG completely before touching any existing file.
            fd, temp_name = tempfile.mkstemp(prefix='.heic_jpg_', suffix='.tmp', dir=output)
            os.close(fd)
            temporary = Path(temp_name)
            with Image.open(source) as opened:
                oriented = ImageOps.exif_transpose(opened)
                exif_bytes = oriented.getexif().tobytes()
                oriented.convert('RGB').save(
                    temporary, format='JPEG', quality=100,
                    subsampling=0, exif=exif_bytes
                )
            if action == 'replace':
                os.replace(temporary, target)
            else:
                # Exclusive creation prevents accidental overwrite if a file
                # appeared after the user approved the conversion.
                with open(temporary, 'rb') as src, open(target, 'xb') as dst:
                    created_target = target
                    while True:
                        chunk = src.read(1024 * 1024)
                        if not chunk:
                            break
                        dst.write(chunk)
            converted += 1
        except Exception as exc:
            failed += 1
            print(f'Failed to convert {source}: {exc}')
            if created_target is not None:
                created_target.unlink(missing_ok=True)
            # Existing files are unchanged unless replacement succeeded.
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
            if progress_callback:
                progress_callback(index, total)
    return converted, failed, skipped
