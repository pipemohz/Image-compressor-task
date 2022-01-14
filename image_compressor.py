from PIL import Image
import os

OJS_DIR = '/var/www/ojs3/'
IMAGES_PATH = '/ojs/public/journals/'
SIZE = (450, 580)


class ImageCompressor():
    def __init__(self) -> None:
        self.optimize_images()

    def get_platforms_dirs(self) -> list:
        try:
            os.listdir(OJS_DIR)
        except FileNotFoundError:
            return None
        else:
            return os.listdir(OJS_DIR)

    def optimize_images(self) -> None:
        if self.get_platforms_dirs():
            for _dir in self.get_platforms_dirs():
                self.compress(directory=_dir)

    def compress(self, directory: str) -> None:

        path = f'{OJS_DIR}{directory}{IMAGES_PATH}'

        try:
            os.listdir(path)
        except FileNotFoundError:
            pass
        else:
            folders = os.listdir(path)

            if folders:
                for folder in folders:
                    files = os.listdir(f"{path}{folder}")
                    covers = [file for file in files if file.startswith(
                        'cover_issue') and (file.endswith('png') or file.endswith('jpg'))]
                    if covers:
                        for image in covers:
                            with Image.open(f'{path}{folder}/{image}') as img:
                                img = img.resize(SIZE)
                                img.save(f'{path}{folder}/{image}')
