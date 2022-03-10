from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def chromeDriverSetup():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="C:\\Selenium\\chromedriver.exe", options=options)
    return driver
