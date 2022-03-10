import chromedriver_install as cdi
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

path = cdi.install(file_directory='c:\\data\\chromedriver\\', verbose=True, chmod=True, overwrite=False, version=None)
print('Installed chromedriver to path: %s' % path)
chromeOptions = ChromeOptions()
chromeOptions.add_argument("--headless")
driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")
