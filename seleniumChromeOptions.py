import chromedriver_install as cdi
from selenium import webdriver

path = cdi.install(file_directory='c:\\data\\chromedriver\\', verbose=True, chmod=True, overwrite=False, version=None)
print('Installed chromedriver to path: %s' % path)
driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")

