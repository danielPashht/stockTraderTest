import time

import pytest
from pytest_bdd import scenarios, given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


scenarios('features/login.feature')

LOGIN_URL = 'https://stockstrader.roboforex.com/login'
DEFAULT_TIMEOUT = 10

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


@given('I am on the login page')
def navigate_to_login(driver):
    driver.get(LOGIN_URL)
    handle_cookie_consent(driver)


def handle_cookie_consent(driver):
    """Wait for and click the allow cookies button if present"""
    cookie_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//ion-button[@translate='cookies.allow']"))
    )
    cookie_button.click()
    time.sleep(1)  # a moment to update the page after clicking


@when('I enter valid credentials')
def enter_credentials(driver):
    email_input = driver.find_element(By.XPATH, "//ion-input[@id='email']//input")
    password_input = driver.find_element(By.XPATH, "//ion-input[@id='password']//input")

    email_input.send_keys("danielpashtetov@gmail.com")
    password_input.send_keys("946815Vip")
    time.sleep(0.2)  # or wait is-active condition for the button instead


@when('I click the continue button')
def click_continue(driver):
    continue_button = driver.find_element(By.CSS_SELECTOR, "div.login-action ion-button[type='button']")
    continue_button.click()


def verify_login_success(driver):
    deposit_button_xpath = "//ion-button[contains(@class, 'app__header_deposit')]"
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, deposit_button_xpath))
    )
    deposit_button = driver.find_element(By.XPATH, deposit_button_xpath)

    assert '/trading' in driver.current_url and deposit_button.is_displayed(), "Login failed"


def test_successful_login_with_valid_credentials(driver):
    navigate_to_login(driver)
    enter_credentials(driver)
    click_continue(driver)
    verify_login_success(driver)
