import logging
from abc import ABC, abstractmethod
from typing import Optional
import pyautogui
import keyboard
import time
from datetime import datetime
from core.logger import setup_logger

class BaseBot(ABC):
    def __init__(self, bot_name: str):
        self.bot_name = bot_name
        self.logger = setup_logger(bot_name)
        self.is_running = False
        self._setup_safety_features()

    def _setup_safety_features(self):
        """Setup safety features like emergency stop"""
        keyboard.add_hotkey('esc', self.emergency_stop)
        pyautogui.FAILSAFE = True

    def emergency_stop(self):
        """Emergency stop function triggered by ESC key"""
        self.logger.warning("Emergency stop triggered!")
        self.is_running = False
        # Add any cleanup code here

    def wait_and_click(self, image_path: str, confidence: float = 0.9, timeout: int = 10) -> bool:
        """
        Wait for an image to appear and click it
        
        Args:
            image_path: Path to the image to find
            confidence: Confidence level for image matching (0-1)
            timeout: Maximum time to wait in seconds
            
        Returns:
            bool: True if image was found and clicked, False otherwise
        """
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, timeout=timeout)
            if location:
                pyautogui.click(location)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error in wait_and_click: {str(e)}")
            return False

    def type_text(self, text: str, interval: float = 0.1):
        """
        Type text with specified interval between keystrokes
        
        Args:
            text: Text to type
            interval: Time between keystrokes in seconds
        """
        pyautogui.write(text, interval=interval)

    def press_key(self, key: str):
        """Press a single key"""
        pyautogui.press(key)

    def press_hotkey(self, *keys: str):
        """Press a combination of keys"""
        pyautogui.hotkey(*keys)

    def wait(self, seconds: float):
        """Wait for specified number of seconds"""
        time.sleep(seconds)

    @abstractmethod
    def run(self):
        """Main bot execution method to be implemented by child classes"""
        pass

    def execute_with_retry(self, func, *args, max_retries: int = 3, **kwargs):
        """
        Execute a function with retry logic
        
        Args:
            func: Function to execute
            max_retries: Maximum number of retry attempts
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            The result of the function if successful, None otherwise
        """
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    self.logger.error(f"All retry attempts failed: {str(e)}")
                    raise
                self.wait(2)  # Wait before retrying 