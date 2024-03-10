from selenium import webdriver
from selenium.webdriver.common.by import By

def login_to_brand24(username, password):


    driver = webdriver.Chrome()

    # Enter the URL for a specific mention form
    driver.get("https://app.brand24.com/searches/add-new-mention/?sid=1251282985")

    login_field = driver.find_element(By.ID, "login")
    password_field = driver.find_element(By.ID, "password")

    # Enter the login credentials
    login_field.send_keys("")
    password_field.send_keys("")

    login_button = driver.find_element(By.ID, "login_button")
    driver.execute_script("arguments[0].click();", login_button)

    return driver

