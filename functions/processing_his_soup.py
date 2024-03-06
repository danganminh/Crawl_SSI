import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_value_price(soup):
    VND = []
    dd_mm_yyyy = []
    history = soup.find_all('div', class_="flex p-2")
    
    for value in history:
        html_value = value.find_all("div", class_="header-statistic-item justify-center text-center")
        time_elem = html_value[0]
        money_elem = html_value[2]
        dd_mm_yyyy.append(time_elem.get_text())
        VND.append(money_elem.get_text())
    
    return dd_mm_yyyy, VND


def click_next_page(driver):
    try:
        next_page = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="page-item"][@rel="next"]')))
        next_page.click()
        return True
    except TimeoutException:
        return False


def get_his_dict(driver):
    value_prices = []
    value_datetimes = []
    
    while True:
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        datetimes, prices = get_value_price(soup)
        value_prices.extend(prices)
        value_datetimes.extend(datetimes)
        
        for date, price in zip(value_datetimes, value_prices):
            print(date, price)
        
        if not click_next_page(driver):
            break
        
            
    return {
        "dd/mm/yyyy": value_datetimes,
        "VND": value_prices
    }
