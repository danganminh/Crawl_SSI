import time
import pandas as pd
import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
from datetime import date

from functions.processing_his_soup import get_his_dict

global url_home 
url_home = 'https://iboard.ssi.com.vn/'


def crawl_history(driver, ID, date_start):

    # Click to history page
    statistics_button_locator = (By.XPATH, '//*[@id="stock-detail-tab"]/ul/li[7]/a')
    statistics_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(statistics_button_locator))
    statistics_button.click()

    # Fill value date to FromDate
    FromDate = driver.find_elements(By.XPATH, '//*[@id="fromDate"]')[-1]
    print(FromDate)
    FromDate.send_keys(Keys.CONTROL,"a")
    time.sleep(0.5)
    FromDate.send_keys(date_start)
    time.sleep(0.5)
    FromDate.send_keys(Keys.ENTER)

    # Get value to save csv
    data = get_his_dict(driver=driver, ID=ID)
    # Creating DataFrame
    df = pd.DataFrame(data)
    # Saving DataFrame to CSV
    df.to_csv(f"{date.today()}_{ID}.csv", encoding='utf-8', index=False)


def check_banner_block(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, 'img.w-full.object-contain')
    if elements:
        print('Waiting banner!')
        return True
    return False


def bot_get_item(driver, date_start=None):

    try:
        # Get home page
        driver.get(url_home)

        # Check banner
        time.sleep(5)
        if check_banner_block(driver):
            time.sleep(30)
            print('Time out banner!')

        # Find column has ID you want
        all_id = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ag-row-odd.ag-row-no-focus.ag-row.ag-row-level-0.ag-row-position-absolute')))
        
        # Logic click with your ID
        for i in range(len(all_id)):
            xpath_main = '//*[@id="main-wrapper"]/div[1]/section[2]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[3]'
            xpath = xpath_main + f"/div[1]/div[{i+1}]"
            css_row_id = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            css_row_id.click()
            
            # Wait load detail page
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="stock-detail-tab"]/div/div/div[3]/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div/div/div[8]/div[1]')))
            
            if date_start:
                ID = css_row_id.get_attribute('row-id')
                print(ID)
                crawl_history(driver=driver, ID=ID, date_start=date_start)
            
            # Get Home page again
            driver.get(url_home)
            # Wait ID again
            WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.ag-row-odd.ag-row-no-focus.ag-row.ag-row-level-0.ag-row-position-absolute')))

    except Exception as e:
        # Print the error message
        print(f"No Symbol to Crawl: {e}")


if __name__ == '__main__':

    driver = uc.Chrome(headless=False, use_subprocess=True, version_main=123)
    
    date_start = "01/01/2020"
    bot_get_item(driver=driver, date_start=date_start)