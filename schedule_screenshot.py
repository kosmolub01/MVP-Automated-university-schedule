"""
===============================================================================

Filename: schedule_screenshot.py

Description:
Script finds up-to-date schedule for given group, takes screenshot 
and saves it in given location.

Input parameters:
    - group name
    - location to save screenshot
    - location with up-to-date browser driver

Output:
    - 0 - successful completion
    - -1 - something went wrong when selecting week
    - error info. string - error

If there is more than one match to provided group, 
program selects the first result listed on a webpage

===============================================================================

"""
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from datetime import date
import sys

# Debug purposes
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":

    # Setup webdriver
    try:
        s = Service(sys.argv[3])
        op = webdriver.EdgeOptions()

        op.add_argument('headless')

        driver = webdriver.Edge(service=s, options=op)
        driver.set_window_size(2160, 1280)
        driver.maximize_window()

        # Get the webpage
        try:
            driver.get("https://plan.polsl.pl/")

            # Selection of a group
            try:
                driver.switch_to.frame("page_content")

                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/" + 
                "table[2]/tbody/tr[1]/td/form/center/input")))
                element.send_keys(sys.argv[1])

                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                "/html/body/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/" +
                "table[2]/tbody/tr[3]/td/center/input")))
                element.click()

                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                "/html/body/table/tbody/tr/td/div/div/a")))
                element.click()

                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                "/html/body/div[4]/div[2]/div[4]/select")))
                element = Select(element)

                # Selection of a week
                try:
                    current_day = date.today().day
                    current_month = date.today().month

                    weeks = element.options[1:]

                    for week in weeks:

                        if(int(week.text[3:5]) == current_month and int(week.text[0:2]) <= current_day and 
                        int(week.text[6:8]) >= current_day):
                            week.click()
                            break
                    
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, 
                    "/html/body/div[4]/div[2]/input")))
                    element.click()
                    

                    # Getting the screenshot and saving it
                    try:             
                        driver.save_screenshot(sys.argv[2])

                        print(0)
                    
                        # Quit the driver instance
                        driver.quit()
                    except:
                        print("Something went wrong when getting the screenshot")   
                except:
                    # Something went wrong when selecting week
                    print(-1)    
            except:
                print("Something went wrong when selecting group")
        except:
            print("Something went wrong when getting the schedule webpage")
    except:
        print("Something went wrong when setting up the webdriver")