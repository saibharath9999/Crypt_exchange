from selenium import webdriver
import time, pickle, os.path, random,pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.common.exceptions import TimeoutException

fake = Faker()
# --> Setup Which Runs Before Every Testcase.

def setup_module(module):
    global driver
    global base_url
    cd = os.environ.get("DRIVERPATH", "/Users/marellasaibharath/Downloads/chromedriver")
    driver = webdriver.Chrome(cd)
    base_url = "http://147.25.130.12:7770"
    driver.set_window_size(1440, 1024)
    driver.maximize_window()
    if not os.path.exists("./Cookies.pkl"):
        driver = driver
        driver.get(base_url + "/login")
        WebDriverWait(driver,100).until(EC.presence_of_element_located((By.NAME,'email')))
        driver.find_element_by_name("email").send_keys("user@mail.co")
        driver.find_element_by_name("password").send_keys("@pswd")
        driver.find_element_by_class_name('elemXBoxInnButton').click()
        time.sleep(12)
        #driver.find_element_by_class_name('elemXBoxInnButton').click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'elemX-MarketLabel')))
        with open("Cookies.pkl","wb") as Cookies:
            pickle.dump(driver.get_cookies(),Cookies)

# --> Handling Cookies.

def handle_Cookies():
    with open("Cookies.pkl","rb") as Cookies:
        cookie = pickle.load(Cookies)
        for ck in  cookie:
            driver.add_cookie(ck)

def choose_Cur(cur_pair = None):
    base_cur = random.choice(['elemX-BTC','elemX-ETH','elemX-HEX','elemX-USDT'])
    if base_cur == 'elemX-BTC':
        cur_pair = random.choice(['elemXTab-ETH/BTC','elemXTab-HEX/BTC','elemXTab-BCH/BTC','elemXTab-DASH/BTC'])
    elif base_cur == 'elemX-ETH':
        cur_pair = random.choice(['elemXTab-HEX/ETH','elemXTab-DASH/ETH','elemXTab-BCH/ETH'])
    elif base_cur == 'elemX-HEX':
        cur_pair = random.choice(['elemXTab-DASH/HEX'])
    return base_cur,cur_pair

base_Cur,cur_Pair = choose_Cur()

@pytest.mark.skip()
def test_buy():
    driver.get(base_url + "/trade")
    handle_Cookies()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'price')))
    driver.find_element_by_class_name('elemXDeskTabAddPair').click()
    driver.find_element_by_class_name('{}'.format(base_Cur)).click()
    time.sleep(1)
    driver.find_element_by_id('{}'.format(cur_Pair)).click()
    driver.find_element_by_class_name('buyPrice').send_keys("20")
    driver.find_element_by_class_name('buyAmount').send_keys("10")
    time.sleep(1)
    driver.find_element_by_class_name('buy').click()
    driver.find_element_by_xpath('//*[@id="elemXShellInnTradingDesk"]/div/div[8]/div/div/div/div[2]/div[3]/div[1]').click()
    time.sleep(1)
    driver.switch_to.alert.accept()
@pytest.mark.skip()
def test_sell():
    driver.get(base_url + "/trade")
    handle_Cookies()
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'price')))
    driver.find_element_by_class_name('elemXDeskTabAddPair').click()
    driver.find_element_by_class_name('{}'.format(base_Cur)).click()
    time.sleep(1)
    driver.find_element_by_id('{}'.format(cur_Pair)).click()
    driver.find_element_by_class_name('sellPrice').send_keys("20")
    driver.find_element_by_class_name('sellAmount').send_keys("10")
    time.sleep(1)
    driver.find_element_by_class_name('sell').click()
    driver.find_element_by_xpath('//*[@id="elemXShellInnTradingDesk"]/div/div[3]/div/div/div/div[0]/div[3]/div[1]').click()
    time.sleep(1)
    driver.switch_to.alert.accept()

@pytest.mark.skip()
def test_Register():
    driver.get(base_url + "/register")
    WebDriverWait(driver,100).until(EC.presence_of_element_located((By.NAME,'email')))
    driver.find_element_by_name('email').send_keys(fake.email())
    driver.find_element_by_name('name').send_keys(fake.name())
    driver.find_element_by_name('username').send_keys(fake.user_name())
    driver.find_element_by_name('password').send_keys(fake.password())
    time.sleep(30)
    driver.find_element_by_class_name('elemXBoxInnButton').click()

@pytest.mark.skip()
def test_Trade():
    driver.get(base_url + "/trade")
    handle_Cookies()
    driver.get(base_url + "/trade")
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'price')))
    time.sleep(1)
    last_price = float(driver.find_element_by_class_name('elemXTDBookCurrent').text)
    buy_val = 1.59
    sel_val = 0.98
    for _ in range(1,5):
        driver.find_element_by_class_name("buyPrice").clear()
        driver.find_element_by_class_name("buyPrice").send_keys(str(last_price))
        driver.find_element_by_name('amount').send_keys(str(buy_val))
        driver.find_element_by_class_name('buy').click()
        time.sleep(1)
        driver.find_element_by_class_name('elemxXOdConfBox-Accept').click()
        time.sleep(2)
        driver.find_element_by_class_name('elemXErrorModalDismiss').click()
        last_price += 0.00011
        sel_val += 0.90
        driver.find_element_by_class_name("sellPrice").clear()
        driver.find_element_by_class_name("sellPrice").send_keys(str(last_price))
        driver.find_element_by_class_name('sellAmount').send_keys(str(sel_val))
        driver.find_element_by_class_name('sell').click()
        time.sleep(1)
        driver.find_element_by_class_name('elemxXOdConfBox-Accept').click()
        time.sleep(2)
        driver.find_element_by_class_name('elemXErrorModalDismiss').click()
        last_price += 0.00024
        buy_val += 0.004
        time.sleep(1)
    time.sleep(5)




def teardown_module(module):
    driver.quit()
