import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


class TestLogin:
    """
    GHERKIN SYNTAX
    
    Scenario 1: Login dengan Kredensial yang Valid
        Terdapat halaman login yang dapat diakses
        Saya memasukkan username yang valid "tomsmith"
        Saya memasukkan password yang valid "SuperSecretPassword!"
        Saya mengklik tombol login
        Saya melihat pesan sukses "You logged into a secure area!"
        Saya diarahkan ke halaman secure area
        Saya melihat tombol logout
    
    Scenario 2: Login dengan Kredensial yang tidak Valid
        Terdapat halaman login yang dapat diakses
        Saya memasukkan username yang valid "tomsmith"
        Saya memasukkan password yang tidak valid "WrongPassword123"
        Saya mengklik tombol login
        Saya melihat pesan error "Your password is invalid!"
        Saya tetap berada di halaman login
        Saya melihat field username yang masih ditampilkan
    """
    
    BASE_URL = "https://the-internet.herokuapp.com/login"
    
    # Credentials
    VALID_USERNAME = "tomsmith"
    VALID_PASSWORD = "SuperSecretPassword!"
    INVALID_PASSWORD = "WrongPassword123"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """
        GIVEN Saya berada di halaman login
        Setup WebDriver before each test
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        
        try:
            driver_path = ChromeDriverManager().install()
            
            if not driver_path.endswith('.exe'):
                driver_dir = os.path.dirname(driver_path)
                actual_driver = os.path.join(driver_dir, 'chromedriver.exe')
                
                if not os.path.exists(actual_driver):
                    parent_dir = os.path.dirname(driver_dir)
                    for root, dirs, files in os.walk(parent_dir):
                        for file in files:
                            if file == 'chromedriver.exe':
                                actual_driver = os.path.join(root, file)
                                break
                
                driver_path = actual_driver
            
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            
            self.driver.get(self.BASE_URL)
        
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            raise
        
        yield
        
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def enter_username(self, username):
        """WHEN Saya memasukkan username"""
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.clear()
        username_field.send_keys(username)
    
    def enter_password(self, password):
        """AND Saya memasukkan password"""
        password_field = self.driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
    
    def click_login_button(self):
        """AND Saya mengklik tombol login"""
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
    
    def test_login_success(self):
        """
        Scenario 1: Login dengan Kredensial yang Valid
        Terdapat halaman login yang dapat diakses
        Saya memasukkan username yang valid "tomsmith"
        Saya memasukkan password yang valid "SuperSecretPassword!"
        Saya mengklik tombol login
        Saya melihat pesan sukses "You logged into a secure area!"
        Saya diarahkan ke halaman secure area
        Saya melihat tombol logout
        """
        self.enter_username(self.VALID_USERNAME)
        self.enter_password(self.VALID_PASSWORD)
        self.click_login_button()
        
        success_message = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
        )
        
        assert "You logged into a secure area!" in success_message.text, \
            "THEN Saya harus melihat pesan sukses 'You logged into a secure area!'"
        assert "success" in success_message.get_attribute("class"), \
            "AND Pesan sukses harus memiliki class 'success'"

        assert "/secure" in self.driver.current_url, \
            "AND Saya harus diarahkan ke halaman secure area"
        
        logout_button = self.driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
        assert logout_button.is_displayed(), \
            "AND Saya harus melihat tombol logout"
        
        print("✅ Scenario 1 PASSED: Login berhasil dengan kredensial valid")
    
    def test_login_failed_wrong_password(self):
        """
        Scenario 2: Login dengan Kredensial yang tidak Valid
        Terdapat halaman login yang dapat diakses
        Saya memasukkan username yang valid "tomsmith"
        Saya memasukkan password yang tidak valid "WrongPassword123"
        Saya mengklik tombol login
        Saya melihat pesan error "Your password is invalid!"
        Saya tetap berada di halaman login
        Saya melihat field username yang masih ditampilkan
        """
        self.enter_username(self.VALID_USERNAME)
        self.enter_password(self.INVALID_PASSWORD)
        self.click_login_button()
        
        error_message = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
        )
        
        assert "Your password is invalid!" in error_message.text, \
            "THEN Saya harus melihat pesan error 'Your password is invalid!'"
        assert "error" in error_message.get_attribute("class"), \
            "AND Pesan error harus memiliki class 'error'"

        assert "/login" in self.driver.current_url, \
            "AND Saya harus tetap di halaman login"

        username_field = self.driver.find_element(By.ID, "username")
        assert username_field.is_displayed(), \
            "AND Halaman login harus tetap menampilkan field username"
        print("✅ Scenario 2 PASSED: Login gagal dengan password salah")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])