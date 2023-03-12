import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

chrome_driver_path = "C:\\Users\\Shaharabanu's\\Application\\chromedriver.exe"
services = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=services)

# Creating a new output csv file
with open("output.csv", 'w') as new_file:
    csvwriter = csv.writer(new_file)
    fields = ['Posting', 'Est. Value Notes', 'Description', 'Closing Date']
    csvwriter.writerow(fields)

driver.maximize_window()
driver.get("https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787")

# Clicking the first posting after loading
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[3]/div[6]/div/div/div/div[3]/div/table/tbody/tr[1]/td[2]/a")))
posting = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[2]/div/div[3]/div[6]/div/div/div/div[3]/div/table/tbody/tr[1]/td[2]/a")
posting.click()

# We need the first 10 postings
for i in range(10):
    time.sleep()
    # Posting
    posting_name = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[2]/div[2]/h1").text
    print(f"Posting: {posting_name}")

    # Est. Value Notes
    est_value = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[1]").text
    est_value_notes = ""
    if est_value == "Est. Value Notes:":
        est_value_notes = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[2]/div/table/tbody/tr[3]/td[2]").text
        print(f"Est value notes:{est_value_notes}")

    # Closing Date
    closing = driver.find_element(by=By.XPATH,
                                    value="/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[1]").text
    closing_date = ""
    if closing == "Closing Date:":
        closing_date = driver.find_element(by=By.XPATH,
                                              value="/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[2]/div/table/tbody/tr[1]/td[2]").text
        print(f"Closing Date: {closing_date}")

    # Description
    description = ""
    for i in range(1, 5):
        desc = driver.find_element(by=By.XPATH,
                                    value=f"/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[3]/div/table/tbody/tr[{i}]/td[1]").text
        if desc == "Description:":
            description = driver.find_element(by=By.XPATH,
                                              value=f"/html/body/div[2]/div[2]/div[2]/div/div[4]/div[1]/div[4]/div[2]/div/div/div[3]/div/table/tbody/tr[{i}]/td[2]").text
            print(f"Description:{description}")
            break

    with open("output.csv", 'a') as new_file:
        csvwriter = csv.writer(new_file)
        datarows = [
            [posting_name, est_value_notes, description, closing_date],
            ]
        csvwriter.writerows(datarows)

    # Click next to go to next posting
    next_button = driver.find_element(by=By.ID, value="id_prevnext_next")
    next_button.click()

