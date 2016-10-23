'''
Giving selenium a test drive.
'''
import os

from selenium import webdriver

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

url = "http://bairwmp.org/projects/20-acres-x-2020-turf-replacement-project"
browser.get(url)
innerHTML = browser.get_attribute("innerHTML")
