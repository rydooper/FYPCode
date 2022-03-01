from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


def configFirefoxDriver():
    firefoxOptions = FirefoxOptions()
    firefoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(executable_path="./geckodriver.exe", options=firefoxOptions)
    return driver


def configChromeDriver():
    chromeOptions = ChromeOptions()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="C:\\Selenium\\chromedriver.exe", options = chromeOptions)
    return driver
