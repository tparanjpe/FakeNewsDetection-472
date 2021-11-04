from selenium import webdriver
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe" 
driver = webdriver.Chrome("C:\\Users\\tarap\\Dropbox\\My PC (LAPTOP-EFB1H1KE)\\Desktop\\CSE472\\project2\\chromedriver.exe",  options=chromeOptions)
driver.get('https://www.reddit.com/r/ASU/')