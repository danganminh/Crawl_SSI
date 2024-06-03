from dateutil.parser import parse
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_demand_supply(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    demands = []
    supplys = []
    history = soup.find_all('div', class_="flex p-2")
    for value in history:
        demand = value.find('div', class_='header-statistic-item justify-end text-right pr-3').get_text().replace(',', '')
        supply = value.find('div', class_='header-statistic-item justify-center text-right').get_text().replace(',', '')
        demands.append(demand)
        supplys.append(supply)
    return demands, supplys


def get_value_price(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    VND = []
    dd_mm_yyyy = []
    history = soup.find_all('div', class_="flex p-2")
    for value in history:
        html_value = value.find_all("div", class_="header-statistic-item justify-center text-center")
        time_elem = html_value[0].get_text()
        money_elem = html_value[2].get_text()
        dd_mm_yyyy.append(time_elem)
        VND.append(money_elem)
    return dd_mm_yyyy, VND


def click_demand_supply(driver):
    try:
        page_ds = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[12]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/button[3]/div')))
        page_ds.click()
    except TimeoutException:
        print("None Demand and Supply page !!")


def click_history(driver):
    try:
        page_hist = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[12]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[1]/button[1]/div')))
        page_hist.click()
    except TimeoutException:
        print("None History page !!")
    

def click_next_page(driver):
    try:
        next_page = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="page-item"][@rel="next"]')))
        next_page.click()
        return True
    except TimeoutException:
        return False


def try_convert(data, dtype):
    result = []
    for val in data:
        try:
            if dtype == 'date':
                val = parse(val).date()
            else:
                val = val.astype(dtype)
        except:
            val = val
        finally:
            result.append(val)
    return result


def get_his_dict(driver, ID):

    value_prices = []
    value_datetimes = []
    value_demands = []
    value_supplys = []

    while True:
        click_history(driver)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="headlessui-tabs-panel-14"]/div/div[1]/div/div[2]/div[1]/div[1]')))
        
        # Get values Price and Date
        datetimes, prices = get_value_price(driver)
        value_prices.extend(prices)
        value_datetimes.extend(datetimes)
        
        # Get values of Demand and Supply
        click_demand_supply(driver)
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="headlessui-tabs-panel-16"]/div/div[1]/div/div[2]/div[1]/div[1]')))
        
        demands, supplys = get_demand_supply(driver)
        value_demands.extend(demands)
        value_supplys.extend(supplys)

        for date, price, demand, supply in zip(value_datetimes, value_prices, value_demands, value_supplys):
            print(ID, date, price, demand, supply)
        
        if not click_next_page(driver):
            break

    return {
        "date": try_convert(value_datetimes, 'date'),
        "VND": try_convert(value_prices, 'float32'),
        "demand": try_convert(value_demands, 'int32'),
        'supply': try_convert(value_supplys, 'int32')
    }
