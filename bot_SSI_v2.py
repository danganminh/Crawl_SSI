import time
import pandas as pd
import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from datetime import date

from functions.processing_his_soup import get_his_dict

global url 
url = "https://iboard.ssi.com.vn/"


def check_banner_block(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, 'img.w-full.object-contain')
    if elements:
        print('Waiting banner!')
        return True
    return False


def crawl_history(driver, ID, date_start):

    # Click to history page
    statistics_button_locator = (By.XPATH, '//*[@id="stock-detail-tab"]/ul/li[7]/a')
    statistics_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(statistics_button_locator))
    statistics_button.click()

    # Fill value date to FromDate
    FromDate = driver.find_elements(By.XPATH, '//*[@id="fromDate"]')[-1]
    FromDate.send_keys(Keys.CONTROL,"a")
    time.sleep(0.5)
    FromDate.send_keys(date_start)
    time.sleep(0.5)
    FromDate.send_keys(Keys.ENTER)
    time.sleep(1)

    # Get value to save csv
    data = get_his_dict(driver=driver, ID=ID)
    # Creating DataFrame
    df = pd.DataFrame(data)
    # Saving DataFrame to CSV
    df.to_csv(f"{date.today()}_{ID}.csv", encoding='utf-8', index=False)


def bot_get_item(driver, ID, date_start=None):
    
    # Check banner
    time.sleep(5)
    if check_banner_block(driver):
        time.sleep(30)
        print('Time out banner!')

    try:
        # Find column has ID you want
        all_id = driver.find_elements(By.CSS_SELECTOR, 'div.ag-row-odd.ag-row-no-focus.ag-row.ag-row-level-0.ag-row-position-absolute')
        # Logic click with your ID
        for i in range(len(all_id)):
            xpath_main = '//*[@id="main-wrapper"]/div[1]/section[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]'
            xpath = xpath_main + f"/div[1]/div[{i+1}]"
            css_row_id = driver.find_element(By.XPATH, xpath)
            if css_row_id.get_attribute('row-id') == ID:
                css_row_id.click()
                time.sleep(1)
                break
            
        if date_start:
            crawl_history(driver=driver, ID=ID, date_start=date_start)

    except Exception as e:
        # Print the error message
        print(f"An error occurred: {e}")


if __name__ == '__main__':

    driver = uc.Chrome(headless=False, use_subprocess=True)
    
    ID_list = ["VHM"]
    date_start = "01/01/2000"

    for ID in ID_list:
        driver.get(url)
        bot_get_item(driver=driver, ID=ID, date_start=date_start)