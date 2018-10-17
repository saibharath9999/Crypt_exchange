from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time,os,pickle,random

def setup_module(module):
    global driver
    global base_url
    cd = os.environ.get("DRIVERPATH", "/Users/marellasaibharath/Downloads/chromedriver")
    driver = webdriver.Chrome(cd)
    base_url = "http://142.14.114.27:7770"
    driver.set_window_size(1440, 1024)
    driver.maximize_window()
    if not os.path.exists("./Cookies.pkl"):
        driver = driver
        driver.get(base_url + "/login")
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.NAME,'email')))
        driver.find_element_by_name("email").send_keys("user@mail.com")
        driver.find_element_by_name("password").send_keys("@pswd")
        driver.find_element_by_class_name('elemqXBoxInnButton').click()
        time.sleep(12)
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'elemqX-MarketLabel')))
        with open("Cookies.pkl","wb") as Cookies:
            pickle.dump(driver.get_cookies(),Cookies)


# --> Handling Cookies.

def handle_Cookies():
    with open("Cookies.pkl","rb") as Cookies:
        cookie = pickle.load(Cookies)
        for ck in  cookie:
            driver.add_cookie(ck)

def amnt_Gen(n):
    b = random.uniform(2, n-2)
    a = random.uniform(1, b - 1)
    c = random.uniform(b + 1, 9)
    d = b-a
    e = c-b
    f = n-c
    return [float("{0:.2f}".format(a)),float("{0:.2f}".format(d)),float("{0:.2f}".format(e)),float("{0:.2f}".format(f))]

def test_buy():
    driver.get(base_url + "/trade")
    handle_Cookies()
    driver.get(base_url + "/trade")
    time.sleep(1)
    values = amnt_Gen(12)
    last_price = "0.034114"
    for i in values:
        #last_price = driver.find_element_by_xpath('//*[@id="elemqXShellInnTradingDesk"]/div/div[2]/section/section[1]/section[1]/div/div[2]/div[2]/div[1]').text

        last_price = float(last_price)
        driver.find_element_by_class_name('buyPrice').clear()
        last_price += 0.00011
        driver.find_element_by_class_name('buyPrice').send_keys(str(last_price))
        driver.find_element_by_class_name('buyAmount').send_keys(str(i))
        driver.find_element_by_class_name('buy').click()
        driver.find_element_by_class_name('elemqxXOdConfBox-Accept').click()
        time.sleep(1)
        driver.find_element_by_id('closeOrderPlaced').click()
        time.sleep(2)

def test_sell():
    driver.get(base_url + "/trade")
    handle_Cookies()
    driver.get(base_url + "/trade")
    time.sleep(1)
    values = amnt_Gen(15)
    last_price = "0.056185"
    for i in values:
        #last_price = driver.find_element_by_xpath('//*[@id="elemqXShellInnTradingDesk"]/div/div[2]/section/section[1]/section[1]/div/div[2]/div[2]/div[1]').text

        last_price = float(last_price)
        driver.find_element_by_class_name('sellPrice').clear()
        last_price += 0.00024
        driver.find_element_by_class_name('sellPrice').send_keys(str(last_price))
        driver.find_element_by_class_name('sellAmount').send_keys(str(i))
        driver.find_element_by_class_name('sell').click()
        driver.find_element_by_class_name('elemqxXOdConfBox-Accept').click()
        time.sleep(1)
        driver.find_element_by_id('closeOrderPlaced').click()
        time.sleep(2)


def teardown_module(module):
    driver.quit()



