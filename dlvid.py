from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time 

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

chromeOptions = Options()  
#chromeOptions.add_argument("--headless")  
#chromeOptions.add_argument(f'user-agent={user_agent}')
chromeOptions.add_argument("--mute-audio")

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome("/Users/QuanhaoLi/Desktop/dlvid/chromedriver", chrome_options=chromeOptions, desired_capabilities=capa)

wait = WebDriverWait(driver, 20)
driver.get("http://kissasian.es/")

wait.until(EC.presence_of_element_located((By.ID, 'onesignal-popover-cancel-button')))

driver.execute_script("window.stop();")

#time.sleep(6)

print("What would you like to search?")
search_option = input()

driver.find_element_by_xpath("//button[@id='onesignal-popover-cancel-button']").click()
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])

#driver.maximize_window()
#driver.implicitly_wait(5)

#driver.find_element_by_name("search").send_keys(str(search_option))
search = driver.find_element_by_xpath("//input[@id='keyword']")
search.send_keys(str(search_option))
time.sleep(3)
# Break here if fails

html_list = driver.find_element_by_xpath("//div[@id='result_box']")
items = driver.find_elements_by_xpath("//a[@class='item_search_link']")

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
        comp_title = driver.find_element_by_xpath("//a[@class='bigChar']").text
        ep_num = '%03d' % int(val[0])
        titl = 'Watch ' + comp_title + ' Episode ' + ep_num + ' online in high quality'
        first_ep = driver.find_element_by_xpath("//a[@title='%s']" %titl)
        driver.execute_script("arguments[0].click();", first_ep)
        driver.implicitly_wait(20)

        driver.find_element_by_link_text("Download").click()
        
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        cur_ep = val[0] + 1
        while (cur_ep < val[1]) :
            driver.execute_script("window.history.go(-1)")
            nm = "Episode " + '%03d' % int(cur_ep)
            driver.find_element_by_xpath("//*[@title='%s']" %nm).click()
            driver.implicitly_wait(20)

            driver.find_element_by_link_text("Download").click()
        
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

            cur_ep = val[0] + 1
    
    print("Is there any other drama you would like to download?")
    break()


       

'''
html_list = driver.find_element_by_xpath("//div[@class='blockbody list_film']")
items = html_list.find_elements_by_class_name("name")

dicty = {}

print("Which drama/movie are you referring to:")
for item in items:
    text = item.text
    print ("\t", text)
    dicty[text[:-7].lower()] = text
while(True):
    choice = input()
    if str(choice).lower() in dicty:
        drama = html_list.find_element_by_link_text(dicty[choice])
        driver.execute_script("arguments[0].click();", drama)
        driver.find_element_by_xpath("//a[@class='watch_button now']").click()
        val = input("What episodes would you like to download?\nPlease input as a single number or as two numbers separated by a -\n")
        if ("-" in val):
            val = val.split("-")
        else:
            val = [val]
        driver.implicitly_wait(20)
        #ep = driver.find_elements_by_class_name("episode_list")
        #print(ep)
        for i in range(0, len(val)):
            ep_num = val[i]
            driver.implicitly_wait(20)

            # Getting Episode
            episodes = driver.find_element_by_xpath("//*[@title='Watch " + choice.title() + " Episode " + val[i] + " - Extend-1']")
            driver.execute_script("arguments[0].click();", episodes)
            dlbttn = driver.find_element_by_xpath("//div[@id='download_btn']")
            driver.execute_script("arguments[0].click();", dlbttn)

            # Getting download link
            driver.switch_to.window(driver.window_handles[1])
            dlbttn2 = driver.find_element_by_xpath("//a[@id='btnDl']")
            driver.execute_script("arguments[0].click();", dlbttn2)

            # Download
            driver.implicitly_wait(20)
            fDlBttn = driver.find_element_by_xpath("//a[@class='main-button dlbutton']")
            driver.execute_script("arguments[0].click();", fDlBttn)

            driver.get_screenshot_as_file('img' + str(i) + '.png') 

        driver.get_screenshot_as_file('img.png') 
        break
    elif str(choice).lower()=="quit":
        break
    else:
        print("The choice you entered was no valid. Please try again or enter quit to quit.")
'''
driver.quit()