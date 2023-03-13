from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginWeb:
    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "pass")
        self.login_button = (By.NAME, "login")

    def enter_email(self, email):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.email_field)).send_keys(email)

    def enter_password(self, password):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.password_field)).send_keys(password)

    def click_login(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.login_button)).click()

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.post_input = (By.TAG_NAME, "p")
        self.post_field = (By.XPATH, "//span[contains(text(),'your mind')]")
        self.post_button = (By.XPATH,"//span[contains(text(),'Post')]")
        self.post_text = (By.CLASS_NAME, "x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld")
        self.logo = (By.XPATH, "//a[@aria-label='Facebook']")

    def home_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.logo)).click()
    def click_input(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.post_field)).click()

    def enter_post(self, post):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.post_input)).send_keys(post)

    def click_post(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.post_button)).click()

    def get_post_text(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.post_text)).text()

    def post_message(self, message):
        self.click_input()
        self.enter_post(message)
        self.click_post()