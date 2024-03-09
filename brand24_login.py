from selenium import webdriver
from selenium.webdriver.common.by import By

def login_to_brand24(username, password):

    # Initialize the Chrome driver
    driver = webdriver.Chrome()
    driver.get("https://app.brand24.com/searches/add-new-mention/?sid=1239325662")

    login_field = driver.find_element(By.ID, "login")
    password_field = driver.find_element(By.ID, "password")

    # Enter the login credentials
    login_field.send_keys("login")
    password_field.send_keys("password")

    # Click the login button
    driver.find_element(By.ID, "login_button")

    login_button = driver.find_element(By.ID, "login_button")
    driver.execute_script("arguments[0].click();", login_button)

    return driver

