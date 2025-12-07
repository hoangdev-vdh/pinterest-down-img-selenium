# src/utils/file_utils.py
import os

def create_directory(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def check_folder_exists(folder_name):
    """Check if a folder exists in the current directory."""
    return folder_name in [i.name for i in os.scandir() if i.is_dir()]

def log_urls(filepath, urls):
    """Appends a list of URLs to a file."""
    if not urls:
        return
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write('\n'.join(urls) + '\n')
