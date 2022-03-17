from image_compressor import ImageCompressor
import logging
from os.path import join
import datetime as dt
from dotenv import dotenv_values
from os.path import join, dirname


def main():
    dotenv_path = join(dirname(__file__), '.env')
    config = dotenv_values(dotenv_path=dotenv_path)

    if config.get('LOG_FILE_PATH'):
        logging.basicConfig(filename=config.get(
            'LOG_FILE_PATH'), level=logging.INFO)
        logging.info(f'[{dt.datetime.now()}] Compression task started.')
        compressor = ImageCompressor(config)
        logging.info(f'[{dt.datetime.now()}] Compression task finished.')

    else:
        raise FileNotFoundError(
            ".env config file doesn't exist or there is not a LOG_FILE_PATH value set.")


if __name__ == '__main__':
    main()
