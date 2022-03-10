#!/usr/bin/env python3
import logging
from PIL import Image
from dotenv import dotenv_values
import os
from os.path import join, dirname
import datetime as dt


class ImageCompressor():
    def __init__(self, config:dict) -> None:
        self.config = config
        self.optimize_images()
        
    def check_env(self):
        """
        Check if a .env file exists in folder and contains required environment variables.
        """
        if not self.config.get('OJS_DIR') or not self.config.get('IMAGES_PATH'):
            logging.critical('There is no a valid .env file in folder.')
            raise FileNotFoundError('There is no a valid .env file in folder.')
        if not self.config.get('SIZE') or not ',' in self.config.get('SIZE'):
            logging.critical("Invalid configuration for SIZE parameter. Must have format 'height_dim, width_dim'.")
            raise NameError("Invalid configuration for SIZE parameter. Must have format 'height_dim, width_dim'.")
        else:
            self.size = tuple(int(dimension) for dimension in self.config.get('SIZE').split(','))

    def get_platforms_dirs(self) -> list:
        """
        Returns a list of all platforms installed in OJS_DIR. If folder not exists, it catches the error and returns a message.
        """
        try:
            os.listdir(self.config.get('OJS_DIR'))
        except FileNotFoundError:
            logging.error(f"[{dt.datetime.now()}] There are no platforms in {self.config.get('OJS_DIR')}.")
        else:
            return os.listdir(self.config.get('OJS_DIR'))

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

        path = f"{self.config.get('OJS_DIR')}/{directory}/{self.config.get('IMAGES_PATH')}"

        try:
            os.listdir(path)
        except FileNotFoundError:
            logging.error(f"[{dt.datetime.now()}] No journals folder found in {directory}.")
        else:
            folders = os.listdir(path)
            logging.info(f"[{dt.datetime.now()}] Checking folder {directory}.")
            if folders:
                for folder in folders:
                    logging.info(f"[{dt.datetime.now()}] Checking journal {folder}.")
                    files = os.listdir(f"{path}{folder}")
                    covers = [file for file in files if file.startswith(
                        'cover_issue') and (file.endswith('png') or file.endswith('jpg'))]
                    if covers:
                        for image in covers:
                            with Image.open(f'{path}{folder}/{image}') as img:
                                if img.size > self.size:
                                    img = img.resize(self.size)
                                    img.save(f'{path}{folder}/{image}')
                                    logging.info(f"[{dt.datetime.now()}] Image {image} compressed.")
