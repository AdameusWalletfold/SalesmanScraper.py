#  Adam Knott Copyright (c) 2023

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

s = Service("C:/ProgramFiles/Google/Chrome/Application/chromedriver.exe")

# Webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=s, options=options)

# User input for Cars.com Search form
stockInput = input("Please enter a number \n0: New & Used Cars \n1: New & Certified Cars \n2: New Cars \n3: Used "
                   "Cars \n4: Certified Cars\n")
if stockInput not in ["0", "1", "2", "3", "4"]:
    stockInput = input('Invalid input. Please choose an option from numbers 1-4: ')

zipInput = int(input('Please enter the 5-digit zip code: '))
makeInput = input('Please enter a make (leave blank for all): ')
distanceInput = input('Please enter the farthest distance(in miles) you are willing to drive: ')
priceInput = input('Please enter a maximum price: ')

# Area to validate user input


# Chromedriver urls
url = "https://www.cars.com"
url2 = "https://www.cars.com/shopping/results/?stock_type=all&makes%5B%5D=&models%5B%5D=&list_price_max=40000" \
       "&maximum_distance=30&zip=27615"

# Calling url
driver.get(url)

# Not a chromedriver option but maximizes window
driver.maximize_window()

# Select a stock type for search query
stock = driver.find_element(By.NAME, "stock_type")
Select(stock).select_by_index(stockInput)

# Delete default zip code and enter current zip code
zip_code = driver.find_element(By.XPATH, "//input[@aria-label='Enter a Zip Code']")
zip_code.send_keys(Keys.BACKSPACE * 5)
zip_code.send_keys(zipInput)

# Select dropdown of makes and select "All makes"
make = driver.find_element(By.ID, "makes")
Select(make).select_by_value(makeInput)

# Select dropdown of maximum distance user is willing to drive to purchase car
distance = driver.find_element(By.ID, "make-model-maximum-distance")
Select(distance).select_by_value(distanceInput)

# Select dropdown of maximum price user is willing to pay for car
price = driver.find_element(By.ID, "make-model-max-price")
Select(price).select_by_value(priceInput)

# Clicking the button to submit form and continue to result page
driver.find_element(By.CLASS_NAME, "sds-button").click()

# Create empty list to store all results
carList = []

# Find the "Next" button element

while True:
    try:
    # Find all car listings on the current page
        next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next page']")

        cars = driver.find_elements(By.XPATH, '//div[@class="vehicle-card   "]')

        for car in cars:
        # Extract information from each car listing
            try:
                title = car.find_element(By.XPATH, './/h2[@class="title"]').text
            except:
                title = None
            try:
                price = car.find_element(By.XPATH, './/span[@class="primary-price"]').text
            except:
                price = None
            try:
                condition = car.find_element(By.XPATH, './/p[@class="stock-type"]').text
            except:
                condition = None
            try:
                mileage = car.find_element(By.XPATH, './/div[@class="mileage"]').text
            except:
                mileage = None
            try:
                miles_from = car.find_element(By.XPATH, './/div[@class="miles-from "]').text
            except:
                miles_from = None

        # Append the extracted information to the carList
            carList.append({'Title': title,
                            'Price': price,
                            'Condition': condition,
                            'Mileage': mileage,
                            'Miles from': miles_from})

    # Click the "Next" button to go to the next page
        next_btn.click()

    # Wait for the next page to load
        WebDriverWait(driver, 20).until(EC.url_changes(url2))

    except StaleElementReferenceException:
        next_btn = driver.find_element(By.XPATH, "//a[@aria-label='Next page']")
        continue

# Create pandas dataframe from the list of all results
    carList_df = pd.DataFrame(carList)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_rows', None)
    print(carList_df)

