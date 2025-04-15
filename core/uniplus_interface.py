import os
import time
import pyautogui
import keyboard
from typing import Optional, Tuple, Union, List
from core.base_bot import BaseBot
from core.logger import setup_logger

class UniplusInterface(BaseBot):
    def __init__(self, bot_name: str):
        super().__init__(bot_name)
        self.uniplus_path = os.getenv('UNIPLUS_PATH', r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Uniplus\Uniplus.lnk')
        self.screenshot_dir = os.path.join('bots', bot_name, 'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
    def _wait_for_element(self, 
                         image_path: Optional[str] = None, 
                         text: Optional[str] = None,
                         confidence: float = 0.9,
                         timeout: int = 10) -> Optional[Tuple[int, int]]:
        """
        Wait for an element to appear on screen
        
        Args:
            image_path: Path to the image to find
            text: Text to find
            confidence: Confidence level for image matching
            timeout: Maximum time to wait in seconds
            
        Returns:
            Tuple of (x, y) coordinates if found, None otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if image_path:
                try:
                    location = pyautogui.locateCenterOnScreen(
                        os.path.join(self.screenshot_dir, image_path),
                        confidence=confidence
                    )
                    if location:
                        return location
                except Exception as e:
                    self.logger.debug(f"Error finding image: {str(e)}")
                    
            if text:
                # Implement OCR text detection here if needed
                pass
                
            time.sleep(0.5)
            
        return None
        
    def _click_element(self, 
                      image_path: Optional[str] = None,
                      text: Optional[str] = None,
                      confidence: float = 0.9,
                      timeout: int = 10) -> bool:
        """
        Click on an element
        
        Args:
            image_path: Path to the image to find
            text: Text to find
            confidence: Confidence level for image matching
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if clicked successfully, False otherwise
        """
        location = self._wait_for_element(image_path, text, confidence, timeout)
        if location:
            pyautogui.click(location)
            return True
        return False
        
    def _type_text(self, text: str, interval: float = 0.1):
        """
        Type text with specified interval
        
        Args:
            text: Text to type
            interval: Time between keystrokes
        """
        pyautogui.write(text, interval=interval)
        
    def _press_keys(self, *keys: str):
        """
        Press a combination of keys
        
        Args:
            *keys: Keys to press
        """
        pyautogui.hotkey(*keys)
        
    def _press_key(self, key: str):
        """
        Press a single key
        
        Args:
            key: Key to press
        """
        pyautogui.press(key)
        
    def open_uniplus(self) -> bool:
        """
        Open Uniplus application
        
        Returns:
            True if opened successfully, False otherwise
        """
        try:
            os.startfile(self.uniplus_path)
            time.sleep(1)
            # Press ESC multiple times to clear any popups
            for _ in range(9):
                self._press_key('esc')
                time.sleep(0.1)
            self.logger.info("Uniplus opened successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error opening Uniplus: {str(e)}")
            return False
            
    def navigate_to_menu(self, menu_path: List[str], image_prefix: str = 'screenshots/') -> bool:
        """
        Navigate through the Uniplus menu using multiple methods
        
        Args:
            menu_path: List of menu items to navigate through
            image_prefix: Prefix for image paths (default: 'screenshots/')
            
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            for menu_item in menu_path:
                menu_found = False
                
                # Method 1: Try with primary image
                image_path = f'{image_prefix}{menu_item}_1.png'
                if self._click_element(image_path=image_path):
                    menu_found = True
                    self.logger.info(f"Found menu item '{menu_item}' using primary image")
                
                # Method 2: Try with secondary image
                if not menu_found:
                    image_path = f'{image_prefix}{menu_item}_2.png'
                    if self._click_element(image_path=image_path):
                        menu_found = True
                        self.logger.info(f"Found menu item '{menu_item}' using secondary image")
                
                # Method 3: Try with coordinates from env
                if not menu_found:
                    # Get coordinates from environment variables
                    x = os.getenv(f'MENU_{menu_item.upper()}_X')
                    y = os.getenv(f'MENU_{menu_item.upper()}_Y')
                    
                    if x is not None and y is not None:
                        try:
                            x = int(x)
                            y = int(y)
                            if self._click_coordinates(x, y):
                                menu_found = True
                                self.logger.info(f"Found menu item '{menu_item}' using coordinates ({x}, {y})")
                        except ValueError:
                            self.logger.warning(f"Invalid coordinates for menu item '{menu_item}': x={x}, y={y}")
                
                if not menu_found:
                    self.logger.error(f"Could not find menu item: {menu_item}")
                    return False
                
                time.sleep(2)  # Wait for menu to load
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error navigating menu: {str(e)}")
            return False
            
    def save_report(self, filename: str, output_folder: str) -> bool:
        """
        Save a report to the specified folder
        
        Args:
            filename: Name of the file to save
            output_folder: Folder to save the file in
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Press F12 to open save dialog
            self._press_key('f12')
            time.sleep(0.5)
            
            # Type filename
            self._type_text(filename)
            time.sleep(0.5)
            
            # Press F4 to focus on folder input
            self._press_key('f4')
            time.sleep(0.5)
            
            # Type folder path
            self._press_keys('ctrl', 'a')  # Select all
            self._type_text(output_folder)
            time.sleep(0.5)
            
            # Press Enter and Alt+S to save
            self._press_key('enter')
            time.sleep(0.5)
            self._press_keys('alt', 's')
            
            self.logger.info(f"Report saved as {filename} in {output_folder}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving report: {str(e)}")
            return False

    def _click_coordinates(self, x: int, y: int) -> bool:
        """
        Click at specific coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if clicked successfully, False otherwise
        """
        try:
            pyautogui.click(x, y)
            return True
        except Exception as e:
            self.logger.error(f"Error clicking at coordinates ({x}, {y}): {str(e)}")
            return False 