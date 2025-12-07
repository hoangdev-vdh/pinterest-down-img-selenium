# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- Credentials ---
USERNAME = os.getenv("PINTEREST_USERNAME", "default_user@example.com")
PASSWORD = os.getenv("PINTEREST_PASSWORD", "default_password")

# --- WebDriver Settings ---
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.3029.110 Safari/537.36"
WINDOW_SIZE = "1200,800"

# --- Pinterest URLs & Selectors ---
BASE_URL = "https://www.pinterest.com"

# Using more stable selectors
LOGIN_BUTTON_SELECTOR = "div[data-test-id='simple-login-button']"
EMAIL_INPUT_ID = "email"
PASSWORD_INPUT_ID = "password"
AVATAR_SELECTOR = "div[data-test-id='gestalt-avatar-svg']"
BOARD_TITLE_SELECTOR = "div[data-test-id='board-card-title'] h2"  # Selector for board titles on profile page
ALL_PINS_BUTTON_SELECTOR = "div[class='Jea hs0 zI7 iyn Hsu']"
IMAGE_SELECTOR = "img[srcset]"

# --- Timing ---
SHORT_WAIT = (2, 4)
MEDIUM_WAIT = (3, 5)
LONG_WAIT = 7
IMPLICIT_WAIT_TIME = 10
EXPLICIT_WAIT_TIMEOUT = 20

# --- File Paths ---
DOWNLOADED_LOG = 'downloaded.txt'
NOT_DOWNLOADED_LOG = 'downloaded_not.txt'
