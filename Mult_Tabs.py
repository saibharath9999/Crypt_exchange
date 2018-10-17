from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os ,time
cd = os.environ.get("DRIVERPATH", "/Users/marellasaibharath/Downloads/chromedriver")
driver = webdriver.Chrome(cd)
driver.get('http:/reddit.com')
window_before = driver.window_handles[0]
driver.execute_script('''window.open("about:blank", "_blank");''')
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)
time.sleep(3)
driver.get('http:/fb.com')
driver.switch_to.window(window_before)
time.sleep(10)
