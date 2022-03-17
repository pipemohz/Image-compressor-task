import logging
from PIL import Image
import os
import datetime as dt


class ImageCompressor():
    def __init__(self, config: dict) -> None:
        self.check_env(config)
        self.optimize_images()

    def check_env(self, config: dict):
        """
        Check if a .env file exists in folder and contains required environment variables.
        """
        if not config.get('OJS_DIR') or not config.get('IMAGES_PATH'):
            logging.critical(
                f'[{dt.datetime.now()}] There is not an OJS_DIR OR IMAGES_PATH value in .env file.')
            raise NameError(
                'There is not an OJS_DIR OR IMAGES_PATH value in .env file.')
        else:
            self.ojs_dir = config.get('OJS_DIR')
            self.images_path = config.get('IMAGES_PATH')

        if not config.get('SIZE') or not ',' in config.get('SIZE'):
            logging.critical(
                f"[{dt.datetime.now()}] Invalid configuration for SIZE parameter. Must have format 'width_dim,height_dim'.")
            raise NameError(
                "Invalid configuration for SIZE parameter. Must have format 'width_dim,height_dim'.")
        else:
            self.size = tuple(int(dimension)
                              for dimension in config.get('SIZE').split(','))

    def get_platforms_dirs(self) -> list:
        """
        Returns a list of all platforms installed in OJS_DIR. If folder not exists, it catches the error and returns a message.
        """
        try:
            os.listdir(self.ojs_dir)
        except FileNotFoundError:
            logging.error(
                f"[{dt.datetime.now()}] There are no platforms in {self.ojs_dir}.")
        else:
            return os.listdir(self.ojs_dir)

    def optimize_images(self) -> None:
        """
        Initializes the compression task of images in the IMAGES_PATH of each platform in OJS_DIR.
        """
        if self.get_platforms_dirs():
            for _dir in self.get_platforms_dirs():
                self.compress(directory=_dir)

    def compress(self, directory: str) -> None:
        """
        Executes the compression of images in the IMAGES_PATH of a directory in OJS_DIR. If journals folder not exist, it catches the error and returns a message.
        """

        path = f"{self.ojs_dir}/{directory}/{self.images_path}"

        try:
            os.listdir(path)
        except FileNotFoundError:
            logging.error(
                f"[{dt.datetime.now()}] No journals folder found in {directory}.")
        else:
            folders = os.listdir(path)
            logging.info(f"[{dt.datetime.now()}] Checking folder {directory}.")
            if folders:
                for folder in folders:
                    logging.info(
                        f"[{dt.datetime.now()}] Checking journal {folder}.")
                    files = os.listdir(f"{path}{folder}")
                    covers = [file for file in files if file.startswith(
                        'cover_issue') and (file.endswith('png') or file.endswith('jpg'))]
                    if covers:
                        for image in covers:
                            with Image.open(f'{path}{folder}/{image}') as img:
                                if img.size > self.size:
                                    img = img.resize(self.size)
                                    img.save(f'{path}{folder}/{image}')
                                    logging.info(
                                        f"[{dt.datetime.now()}] Image {image} compressed.")
