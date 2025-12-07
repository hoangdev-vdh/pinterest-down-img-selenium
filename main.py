# main.py
from src.core.pinterest_scraper import PinterestScraper
from src.utils.file_utils import check_folder_exists
from src import config

def main():
    """Main function to run the Pinterest image downloader."""
    print("--- Pinterest Image Downloader ---")

    # Validate credentials are set
    if not config.USERNAME or not config.PASSWORD or "default" in config.USERNAME:
        print("\nERROR: Pinterest credentials are not set.")
        print("Please create a '.env' file in the root directory with:")
        print("PINTEREST_USERNAME=your_email@example.com")
        print("PINTEREST_PASSWORD=your_password")
        return

    # Get folder name from user
    while True:
        folder_name_temp = input("Enter a base name for the download folders: ")
        if not folder_name_temp:
            print("Folder name cannot be empty.")
            continue
        
        if check_folder_exists(f"{folder_name_temp}_*"):
             print("Warning: Folders with this base name might already exist.")
        break
    
    # Initialize and run the scraper
    scraper = PinterestScraper(username=config.USERNAME, password=config.PASSWORD)
    scraper.run(base_folder_name=folder_name_temp)

    print("\n--- Process Finished ---")

if __name__ == "__main__":
    main()
