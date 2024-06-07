from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import getpass
import time
import os

class PanoptoSession:
    def __init__(self, panopto_url):
        # Get username and password from user
        self.username = input("Input your MWS email address: ")
        self.password = getpass.getpass("Input your MWS password: ")
        self.panopto_url = panopto_url

        print("URL: ", self.panopto_url)
        
        # Configure webdriver
        
        # Get the current directory
        current_dir = os.getcwd()

        # Append the file name to the current directory
        CHROMEDRIVER_PATH = os.path.join(current_dir, 'chromedriver.exe')
        

        service = Service(executable_path=CHROMEDRIVER_PATH)
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_argument('--ignore-certificate-errors')
        self.browser = webdriver.Chrome(service=service, options=chrome_options)
        
        # Login
        self.browser.get(self.panopto_url)

        time.sleep(5)

        # Get anchor element with text "Sign in"
        sign_in_button = self.browser.find_element(By.XPATH, "//a[contains(text(),'Sign in')]")
        sign_in_button.click()

        # Wait for the page to load
        time.sleep(5)
        
        username_input = self.browser.find_element(By.XPATH, "//input[@name='UserName']")
        password_input = self.browser.find_element(By.XPATH, "//input[@name='Password']")

        # Get submit button by text "LOG IN"
        submit_button = self.browser.find_element(By.XPATH, "//span[contains(text(),'Sign in')]")
        
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        
        submit_button.click()
        
        # Wait for 10 seconds
        print("wait ...")
        time.sleep(10)
        
        # Find all elements with the class "verification-code"
        elements = self.browser.find_elements(By.CLASS_NAME, "verification-code")
        
        # Print the text content of each element
        for element in elements:
            print("Verification code for DUO")
            print(element.text)

        # Countdown loop
        for i in range(20, 0, -1):
            print("You have {} seconds to enter your verification code.".format(i), end="\r")
            time.sleep(1)
        
        # Confirm trust browser
        try:
            self.browser.find_element(By.ID, "trust-browser-button").click()
            print("")
            print("Login Success.")
        except:
            print("")
            print("Login Failure")

if __name__ == "__main__":
    # Create a Canvas session
    panopto = PanoptoSession("https://liverpool.cloud.panopto.eu/Panopto/Pages/Auth/Login.aspx?Auth=FolderView&panoptoState=9aa3fa36-a76f-4e1d-a4c5-b18500fed7e7&ErrorKey=Controls_Login_NoFolderAccess")
    