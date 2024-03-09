import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import datetime
from brand24_login import login_to_brand24
import time

def select_dropdown_option_by_text(driver, element_id, text):
    try:
        dropdown = Select(driver.find_element(By.ID, element_id))
        dropdown.select_by_visible_text(text)
    except NoSuchElementException:
        print(f"Dropdown with ID '{element_id}' not found.")
    except Exception as e:
        print(f"Failed to select dropdown option by text with error: {e}")

def fill_field_by_id(driver, field_id, text):
    try:
        field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, field_id)))
        field.send_keys(text)
    except TimeoutException:
        print(f"Field with ID '{field_id}' not clickable.")
    except Exception as e:
        print(f"Failed to fill field by ID with error: {e}")

def set_readonly_field(driver, field_id, value):
    try:
        field = driver.find_element(By.ID, field_id)
        driver.execute_script("arguments[0].value = arguments[1];", field, value)
    except NoSuchElementException:
        print(f"Readonly field with ID '{field_id}' not found.")
    except Exception as e:
        print(f"Failed to set readonly field with error: {e}")

def click_submit_button(driver):
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='image'][@onclick='return addMentionToDatabase()']"))
        )
        submit_button.click()
        return True
    except TimeoutException:
        print("Submit button not clickable.")
        return False
    except Exception as e:
        print(f"Failed to click the submit button with error: {e}")
        return False

# Login to the website
driver = login_to_brand24(username="username", password="password")
data = pd.read_csv("C:/Users/pozar/Desktop/W/B24_test_IG.csv")

for index, row in data.iterrows():
    fill_field_by_id(driver, "mention_url", row['Entry address'])
    select_dropdown_option_by_text(driver, 'mention_category', 'Instagram')
    select_dropdown_option_by_text(driver, 'mention_country', 'RO')
    fill_field_by_id(driver, "mention_title", row['Entry title'])
    fill_field_by_id(driver, "mention_content", row['Mention content'])
    fill_field_by_id(driver, "mention_likes", str(row['Likes']))
    fill_field_by_id(driver, "mention_views", str(row['Pageviews']))
    fill_field_by_id(driver, "mention_comments", str(row['Comments']))

    # Handle date conversion
    try:
        date_obj = datetime.strptime(str(row['Date']), '%m/%d/%Y')
        set_readonly_field(driver, "mention_created_date_day", date_obj.strftime('%d-%m-%Y'))
        set_readonly_field(driver, "mention_created_date_hour", "12")
        set_readonly_field(driver, "mention_created_date_minute", "00")
    except ValueError as ve:
        print(f"Date parsing error on row {index} with value '{row['Date']}': {ve}")
        continue

    click_submit_button(driver)

    # Checking for an error message indicating a duplicate entry
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(., 'There is the entry with this address in the project already')]"))
        )
        if "There is the entry with this address in the project already" in error_message.text:
            print(f"Duplicate entry on row {index} with address: {row['Entry address']}")
            continue  # Skip the rest of the loop and proceed with the next row
    except TimeoutException:
        # If no error message is found, assume the submission was successful
        pass

        #small delay before continuing to the next iteration
        time.sleep(1)

    # Check for the end of the data
    if index >= len(data) - 1:
        break  # Exit the loop if this was the last row

driver.quit()
