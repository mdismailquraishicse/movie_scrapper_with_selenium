# Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
# This function fetches cast names
def get_cast(driver,xpath):
    cast = driver.find_element(By.XPATH, xpath)
    dummy = cast.find_elements(By.TAG_NAME,'th')
    index = [j for j,i in enumerate(dummy) if i.text == 'Starring'][0]
    cast = tuple(cast.find_elements(By.TAG_NAME,'td')[index].text.split('\n')[:2])
    return cast
# This function fetches box-office
def get_income(driver, xpath):
    income =''
    try:
        income = driver.find_element(By.XPATH, xpath)
        dummy = income.find_elements(By.TAG_NAME,'th')
        index = [j for j,i in enumerate(dummy) if i.text == 'Box office'][0]
        income = tuple(income.find_elements(By.TAG_NAME,'td')[index].text.split('\n'))
    except:
        income ='un-available'
    return income
# This function fetches all the details like cast, income, description etc.
def get_movieDetails(url):
    # Required links (internal links only)
    cast_path = "/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table/tbody"
    title = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/table[1]/tbody/tr[1]/th'
    review = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[24]'
    description = '/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/p[2]'

    # Make driver and load page
    my_browser = webdriver.Chrome()
    my_browser.get(url)

    # Get title, cast, box-office, reviews, description
    title = my_browser.find_element(By.XPATH,title).text
    cast = get_cast(my_browser , xpath=cast_path)
    income = get_income(my_browser, cast_path)
    try:
        review = my_browser.find_element(By.XPATH, review).text.split('.')[0].split()[-1]
    except:
        review = 'un-available'
    description = my_browser.find_element(By.XPATH,description).text
    # Assign the results inside result
    result = (title, cast, description, income, review)
    return result
    
# Name of the movies
titles = ['Ek_Tha_Tiger',"The_Curious_Case_of_Benjamin_Button_(film)",
          "Eega", "Inception", "Munjya_(film)", "Manjummel_Boys",
          "The_Boys_(TV_series)",
          "KGF:_Chapter_2", "Baahubali:_The_Beginning",
          "Fifty_Shades_of_Grey_(film)"]
# Initialize list so that result can be appended.
names = []
cast = []
income = []
review = []
description = []
# Get details of all the movies
for title in titles:
    results = get_movieDetails(f"https://en.wikipedia.org/wiki/{title}")
    names.append(results[0])
    cast.append(results[1])
    income.append(results[3])
    review.append(results[4])
    description.append(results[2])
# Make data frame assign respective values
df = pd.DataFrame()
df['name'] = names
df['description'] = description
df['cast'] = cast
df['income'] = income
df['review'] = review
# Save the df into excel format
df.to_excel('output.xlsx', index=False)