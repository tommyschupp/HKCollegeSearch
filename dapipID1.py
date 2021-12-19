import pandas
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#maryland, DC, Virginia, West Virginia, Pennsylvania 
collegeList = []
addressList = []
stateFinalList = []
i = 0
def scrape():
    chromeOptions = Options()
    driver = webdriver.Chrome(options=chromeOptions)
    url = 'https://ope.ed.gov/dapip/#/search'
    driver.get(url)
    driver.maximize_window()
    time.sleep(4)
    driver.find_element_by_xpath('//input[@id="state"]').click()
    stateList = driver.find_elements_by_xpath('//li[@value=0]')
    for state in stateList:
        if '<div _ngcontent-c8="">Maryland</div>' in state.get_attribute("innerHTML"):
            state.click()
        if '<div _ngcontent-c8="">District of Columbia</div>' in state.get_attribute("innerHTML"):
            state.click()
        if '<div _ngcontent-c8="">West Virginia</div>' in state.get_attribute("innerHTML"):
            state.click()
        if '<div _ngcontent-c8="">Virginia</div>' in state.get_attribute("innerHTML"):
            state.click()   
        if '<div _ngcontent-c8="">Pennsylvania</div>' in state.get_attribute("innerHTML"):
            state.click()
    driver.find_element_by_xpath('//button[@id="search"]').click()
    time.sleep(4)
    for i in range(500):
        soup = BeautifulSoup(driver.page_source,'html.parser')
        #this soup isnt resetting? or something? idk 
        for data in soup.find_all('td'):
            if data.contents[0] == "Institution":
                text=data.parent.find('a').contents[0]
                bad_chars = ['\xd7', '\n', '\x99m', "\xf0", '                          '] 
                for i in bad_chars : 
                    text = text.replace(i, '') 
                collegeList.append(text)

                text = data.parent.find_all('td')[2].string
                bad_chars = ['\xd7', '\n', '\x99m', "\xf0"] 
                for i in bad_chars : 
                    text = text.replace(i, '') 
                addressList.append(text)

                text = data.parent.find_all('td')[4].string
                bad_chars = ['\xd7', '\n', '\x99m', "\xf0"] 
                for i in bad_chars : 
                    text = text.replace(i, '') 
                stateFinalList.append(text)
        
        try: 
            driver.find_element_by_xpath('//i[@class="fa fa-angle-double-right"]').click()
        except:
            time.sleep(2)
        if("York College of Pennsylvania" in collegeList):
            print("doneski")
            break
        

scrape()

results = pandas.DataFrame(list(zip(collegeList, addressList, stateFinalList)), columns=["Institution", "Address", "State"])
results.to_csv(r'C:\Users\tommy\Desktop\Programming\HK\old\completeList.csv', index=False, header=True)
