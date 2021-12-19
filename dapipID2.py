import pandas #
from bs4 import BeautifulSoup #
from selenium import webdriver #
from selenium.webdriver.chrome.options import Options #
import time
from concurrent.futures import ThreadPoolExecutor #



newList = pandas.read_csv(r'SClist.csv')
schoolList = newList["Institution Name"]
idList = []
metaList = []
accreditorList = []
acceptedStates = ['MD', 'PA', 'VA', 'WV', 'DC']
badSchools = []

def cleanString(string):
    bad_chars = ['\xd7', '\n', '\x99m', "\xf0", '                          ', '  '] 
    for i in bad_chars : 
        string = string.replace(i, '') 
    return string

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
def scrape(school):
    chromeOptions = Options()
    #chromeOptions.add_argument('--headless')
    driver = webdriver.Chrome(options=chromeOptions)
    url = 'https://ope.ed.gov/dapip/#/home'
    driver.get(url)
    driver.maximize_window()
    time.sleep(4)
    driver.find_element_by_xpath('//input[@id="searchTerm"]').send_keys(school)
    driver.find_element_by_xpath('//button[@id="searchBtn"]').click()
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for data in soup.find_all('td'):
        if data.contents[0] == "Institution":
            text=cleanString(data.parent.find('a').contents[0])
            if text in school:
                #go back to selenium
                locationNameList = driver.find_elements_by_xpath('//a[@class="location-name"]')
                for locationName in locationNameList:
                    time.sleep(2)
                    if text in locationName.get_attribute("innerHTML"):
                        locationName.click()
                        time.sleep(4)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        factList = []
                        for child in soup.find('div', 'institution-information').contents:
                            if "top-row" in str(child):
                                for grandchild in child.contents:
                                    text2 = grandchild.string
                                    if(text2 != None):
                                        text2 = cleanString(grandchild.string)
                                        if(len(text2) != 0):
                                            factList.append(text2)
                            if "bottom-row" in str(child):
                                for grandchild in child.contents:
                                    if(grandchild != None):
                                        dapipId = str(grandchild)[str(grandchild).find("DAPIP ID: ") + 10:str(grandchild).find("DAPIP ID: ") + 16]
                                        if(isNum(cleanString(dapipId))):
                                            idList.append(cleanString(dapipId))
                            #can u also search for the accreditor and add it to the thing
                        metaList.append(factList)
                        if(factList[-1] not in acceptedStates):
                            badSchools.append(school)
                        table = soup.find('institutional-accr-tables')
                        tempAccList = []
                        for line in table.descendants:
                            if "<" not in line:
                                if line.string != None:
                                    if "Accreditor" not in line.string:
                                        if "Accredited" not in line.string:
                                            if "(" and "/" not in line.string:
                                                if "Next Review Date" not in line.string:
                                                    if "Preaccredited" not in line.string:
                                                        if any(c.isalpha() for c in line.string):
                                                            if line.string not in tempAccList:
                                                                    tempAccList.append(line.string)

                        tempAccList = [cleanString(x) for x in tempAccList]

                        accreditorList.append(tempAccList)
                        print("Finished " + school)
                        driver.close()

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        for school in schoolList:
            executor.submit(scrape, school)

results = pandas.DataFrame(list(zip(schoolList, idList, metaList, accreditorList)), columns = ["Institution", "DAPIP ID", "Metadata", "Accreditor(s)"])
results.to_csv(r'dapip2results.csv', index=False, header=True)

print("DONE!! :D")
    

