# src/core/downloader.py
import urllib.request
from src.utils.file_utils import log_urls
from src.config import DOWNLOADED_LOG, NOT_DOWNLOADED_LOG
import os

class ImageDownloader:
    """Handles downloading images and logging results."""

    def download_images(self, image_urls, folder_name):
        """
        Downloads images from a list of URLs into a specified folder.

        Args:
            image_urls (list): A list of image source URLs.
            folder_name (str): The name of the folder to save images to.
        """
        downloaded_urls = []
        not_downloaded_urls = []

        unique_urls = sorted(list(set(image_urls)))
        print(f"\nFound {len(unique_urls)} unique images to download for board '{os.path.basename(folder_name)}'.")

        for url in unique_urls:
            try:
                # The last URL in the srcset is the highest resolution
                highest_res_url = url.split(',')[-1].replace(' 4x', '').strip()
                filename = highest_res_url.split('/')[-1].split('?')[0] # Clean filename
                
                print(f"Downloading: {filename}")
                urllib.request.urlretrieve(highest_res_url, os.path.join(folder_name, filename))
                downloaded_urls.append(highest_res_url)
            except Exception as e:
                print(f"Error downloading image: {highest_res_url}")
                print(f"Reason: {e}")
                not_downloaded_urls.append(highest_res_url)

        # Log results
        log_urls(DOWNLOADED_LOG, downloaded_urls)
        log_urls(NOT_DOWNLOADED_LOG, not_downloaded_urls)

        print(f"Finished downloading for board. {len(downloaded_urls)} succeeded, {len(not_downloaded_urls)} failed.")
