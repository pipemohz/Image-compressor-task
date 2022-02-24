from PIL import Image
from dotenv import load_dotenv, dotenv_values
import os
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '.env')
config = dotenv_values(dotenv_path=dotenv_path)
SIZE = (450, 580)


class ImageCompressor():
    def __init__(self) -> None:
        self.optimize_images()

    def check_env(self):
        """
        Check if a .env file exists in folder and contains required environment variables.
        """
        if config.get('OJS_DIR') == None or config.get('IMAGES_PATH') == None:
            raise FileNotFoundError('There is no a valid .env file in folder.')

    def get_platforms_dirs(self) -> list:
        """
        Returns a list of all platforms installed in OJS_DIR. If folder not exists, it catches the error and returns a message.
        """
        try:
            os.listdir(config.get('OJS_DIR'))
        except FileNotFoundError:
            print(f"There are no platforms in {config.get('OJS_DIR')}.")
        else:
            return os.listdir(config.get('OJS_DIR'))

    def optimize_images(self) -> None:
        """
        Initializes the compression task of images in the IMAGES_PATH of each platform in OJS_DIR.
        """
        self.check_env()
        if self.get_platforms_dirs():
            for _dir in self.get_platforms_dirs():
                self.compress(directory=_dir)

    def compress(self, directory: str) -> None:
        """
        Executes the compression of images in the IMAGES_PATH of a directory in OJS_DIR. If journals folder not exist, it catches the error and returns a message.
        """

        path = f"{config.get('OJS_DIR')}/{directory}/{config.get('IMAGES_PATH')}"

        try:
            os.listdir(path)
        except FileNotFoundError:
            print(f"There are no journals in {directory}.")
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
                                if img.size > SIZE:
                                    img = img.resize(SIZE)
                                    img.save(f'{path}{folder}/{image}')
