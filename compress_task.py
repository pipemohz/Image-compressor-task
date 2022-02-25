from image_compressor import ImageCompressor
import logging
from os.path import join
import datetime as dt

def main():
    logging.basicConfig(filename='compressor.log', level=logging.INFO)
    logging.info(f'[{dt.datetime.now()}] Compression task started.')
    compressor = ImageCompressor()
    logging.info(f'[{dt.datetime.now()}] Compression task finished.')

if __name__ == '__main__':
    main()