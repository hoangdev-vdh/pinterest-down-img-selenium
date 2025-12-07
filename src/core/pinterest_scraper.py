# src/core/pinterest_scraper.py
import random
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src import config
from src.core.downloader import ImageDownloader
from src.utils.file_utils import create_directory

class PinterestScraper:
    """
    A Selenium-based scraper for downloading images from Pinterest boards.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.downloader = ImageDownloader()
        self.driver = self._setup_driver()

    def _setup_driver(self):
        """Initializes and configures the Chrome WebDriver."""
        options = Options()
        options.add_argument(f"user-agent={config.USER_AGENT}")
        options.add_argument(f"window-size={config.WINDOW_SIZE}")
        options.add_argument("--disable-notifications")
        # The Service object is now managed automatically by Selenium Manager
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(config.IMPLICIT_WAIT_TIME)
        return driver

    def login(self):
        """Logs into Pinterest."""
        print("Navigating to Pinterest and logging in...")
        self.driver.get(config.BASE_URL)
        wait = WebDriverWait(self.driver, config.EXPLICIT_WAIT_TIMEOUT)
        
        try:
            # Click login button
            login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, config.LOGIN_BUTTON_SELECTOR)))
            login_button.click()
            sleep(random.uniform(*config.SHORT_WAIT))

            # Enter credentials
            email_field = wait.until(EC.presence_of_element_located((By.ID, config.EMAIL_INPUT_ID)))
            email_field.send_keys(self.username)

            password_field = self.driver.find_element(By.ID, config.PASSWORD_INPUT_ID)
            password_field.send_keys(self.password)
            sleep(1)
            password_field.send_keys(Keys.RETURN)
            
            # Wait for login to complete by checking for avatar
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, config.AVATAR_SELECTOR)))
            print("Login successful.")
            sleep(random.uniform(*config.SHORT_WAIT))
        except Exception as e:
            print(f"Error during login: {e}")
            self.quit()
            raise

    def navigate_to_profile(self):
        """Navigates to the user's profile page."""
        print("Navigating to profile page...")
        try:
            avatar = WebDriverWait(self.driver, config.EXPLICIT_WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, config.AVATAR_SELECTOR))
            )
            avatar.click()
            print("Profile page loaded.")
            sleep(random.uniform(*config.SHORT_WAIT))
        except Exception as e:
            print(f"Error navigating to profile page: {e}")
            self.quit()
            raise

    def get_boards(self):
        """Scrapes the profile page to find all user boards."""
        print("Finding all boards on the profile page...")
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        board_elements = soup.select(config.BOARD_TITLE_SELECTOR)
        board_names = [board.text for board in board_elements]
        print(f"Found boards: {board_names}")
        return board_names

    def scrape_images_from_board(self, board_name):
        """
        Navigates to a specific board and scrapes all image URLs.
        This involves scrolling down the page to load all images.
        """
        print(f"\n--- Starting scrape for board: {board_name} ---")
        image_urls = []
        try:
            # Navigate to the board
            board_link = self.driver.find_element(By.XPATH, f"//h2[text()='{board_name}']")
            board_link.click()
            sleep(random.uniform(*config.MEDIUM_WAIT))

            # Scroll down to load all images
            scroll_pause_time = 2  # Time to wait for new content to load
            no_change_count = 0
            max_no_change = 5  # Stop after 5 consecutive scrolls with no new height
            
            while True:
                # Get current scroll height BEFORE scrolling
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # Scroll to the bottom of the page
                # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Scroll 800 length
                self.driver.execute_script("window.scrollBy(0, 1000);")
                
                # Wait for new content to load
                sleep(scroll_pause_time + random.uniform(0.5, 1.5))
                
                # Collect images from current page state
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                images = soup.select(config.IMAGE_SELECTOR)
                
                for image in images:
                    if image.get('srcset'):
                        image_urls.append(image['srcset'])
                
                # Get new scroll height AFTER scrolling and waiting
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                print(f"Scrolled: {len(set(image_urls))} unique images found. Height: {last_height} -> {new_height}")
                
                # Check if we've reached the bottom (no new content loaded)
                if new_height == last_height:
                    no_change_count += 1
                    print(f"No new content loaded ({no_change_count}/{max_no_change})")
                    if no_change_count >= max_no_change:
                        print("Reached the end of the page.")
                        break
                else:
                    no_change_count = 0  # Reset counter if new content was loaded
            
            unique_urls = list(set(image_urls))
            print(f"Total unique images found: {len(unique_urls)}")
            return unique_urls

        except Exception as e:
            print(f"Could not scrape board '{board_name}'. Reason: {e}")
            return []
        finally:
            # Go back to profile page for the next board
            print("Returning to profile page.")
            self.driver.back()
            sleep(random.uniform(*config.MEDIUM_WAIT))


    def run(self, base_folder_name):
        """Main method to run the entire scraping process."""
        try:
            self.login()
            self.navigate_to_profile()
            boards = self.get_boards()

            for board_name in boards:
                # Create a dedicated folder for the board
                folder_name = f"{base_folder_name}_{board_name.replace(' ', '_')}"
                create_directory(folder_name)

                # Scrape URLs from the board
                image_urls = self.scrape_images_from_board(board_name)

                # Download the images
                if image_urls:
                    self.downloader.download_images(image_urls, folder_name)
                else:
                    print(f"No images found or scraped for board '{board_name}'.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self.quit()

    def quit(self):
        """Closes the WebDriver."""
        print("\nClosing the browser.")
        if self.driver:
            self.driver.quit()
