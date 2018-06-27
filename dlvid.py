#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time 
import dl as down
import sys

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

chromeOptions = Options()  
chromeOptions.add_argument("--headless")  
chromeOptions.add_argument(f'user-agent={user_agent}')
chromeOptions.add_argument("--mute-audio")

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome("/Users/QuanhaoLi/Desktop/dlvid/chromedriver", chrome_options=chromeOptions, desired_capabilities=capa)

wait = WebDriverWait(driver, 20)
driver.get("http://kissasian.es/")

#wait.until(EC.presence_of_element_located((By.ID, 'onesignal-popover-cancel-button')))

#driver.execute_script("window.stop();")

#print("What would you like to search?")
#search_option = input()
search_option = ""

for arg in sys.argv:
    if str(arg) != "./d.py" :
        search_option = search_option + str(arg) + " "

#driver.find_element_by_xpath("//button[@id='onesignal-popover-cancel-button']").click()
#driver.switch_to.window(driver.window_handles[1])
#driver.close()
#driver.switch_to.window(driver.window_handles[0])

#driver.maximize_window()
#driver.implicitly_wait(5)

#driver.find_element_by_name("search").send_keys(str(search_option))
driver.implicitly_wait(20)
search = driver.find_element_by_xpath("//input[@id='keyword']")
search.send_keys(str(search_option))
time.sleep(3)

time.sleep(1)
html_list = driver.find_element_by_xpath("//div[@id='result_box']")
items = driver.find_elements_by_xpath("//a[@class='item_search_link']")

# Break here if fails
if len(items) < 1:
    print ("No matching drama was found.")
    driver.quit()
    sys.exit()


dicty = {}

print("Which drama/movie are you referring to:")
for item in items:
    text = item.text
    print ("\t", text)
    dicty[text.lower()] = text

while(True):
    choice = input()
    if str(choice).lower() in dicty:
        drama = html_list.find_element_by_link_text(dicty[choice])
        driver.execute_script("arguments[0].click();", drama)
        val = input("What episodes would you like to download?\nPlease input as a single number or as two numbers separated by a -\n")
        if ("-" in val):
            val = val.split("-")
        else:
            val = [val]
        driver.implicitly_wait(20)
        comp_title = driver.find_element_by_xpath("//a[@class='bigChar']").text
        ep_num = '%03d' % int(val[0])
        titl = 'Watch ' + comp_title + ' Episode ' + ep_num + ' online in high quality'
        first_ep = driver.find_element_by_xpath("//a[@title='%s']" %titl)
        driver.execute_script("arguments[0].click();", first_ep)
        '''
        wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
        driver.execute_script("window.stop();")
        '''
        driver.implicitly_wait(20)
        dl = driver.find_element_by_link_text("Download")
        driver.execute_script("arguments[0].click();", dl)
        driver.switch_to.window(driver.window_handles[1])

        file_name = 'Episode_' + ep_num + '.mp4'
        down.download(driver.current_url, file_name)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
        cur_ep = int(val[0]) + 1

        while (cur_ep <= int(val[1])) :

            next_btn = driver.find_element_by_xpath("//a[@class='nexxt']")
            driver.execute_script("arguments[0].click();", next_btn)

            driver.implicitly_wait(20)

            dl = driver.find_element_by_link_text("Download")
            driver.execute_script("arguments[0].click();", dl)
            driver.switch_to.window(driver.window_handles[1])

            ep_num = '%03d' % cur_ep
            file_name = 'Episode_' + ep_num + '.mp4'
            down.download(driver.current_url, file_name)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            cur_ep = cur_ep + 1
    elif choice.lower == "quit" :
        break
    else:
        ("You did not select a valid drama. Please try again or enter quit to exit")

driver.quit()