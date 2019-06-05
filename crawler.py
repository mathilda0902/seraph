import time, re, json
import selenium.webdriver
from selenium.webdriver.common.keys import Keys


def get_company(company_string):
    """
    Returns the company name from each user profile summary. 
    company_string: for each user profile summary, a broken down list of words in the summary.
    """
    for index, word in enumerate(company_string):
        if word in ['Founder', 'Co-founder', 'CEO', 'founder'] :
            company = ' '.join(company_string[index:])
            
            if '.' in company:
                stop_pos = [m.start(0) for m in re.finditer(r'\.', company)][0]
            else:
                stop_pos = len(company)  
            
            return company[:stop_pos]


def get_name_company(query_list):
    """
    Returns a dictionary that matches founder names with their companies.
    query_list: a list of user profile strings.
    """
    sample_db = {}
    for name in query_list:
        name_com = name.replace('\n', ' ').split(', ')
        if len(name_com) > 1:
            sample_db[name_com[0]] = get_company(name_com[1].split(" "))
    return sample_db


if __name__ == '__main__':
    # initiate a chromedriver session
    driver = selenium.webdriver.Chrome('/Users/vicky/Dev/chromedriver')
    driver.get("https://www.quora.com/search?q=founder&type=profile")
    print(driver.window_handles)

    # automate the scroll down action to handle infinite scroll
    for i in range(1, 100):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)

    # find QueryResultsList which contains all profile summaries
    element = driver.find_elements_by_class_name("QueryResultsList")
    query_list = element[0].text.split("Profile:")
    get_name_company(query_list)

    