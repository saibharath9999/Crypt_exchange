from selenium import webdriver
import unittest, sys, time, pickle, os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Hex(unittest.TestCase):

    # --> Setup Which Runs Before Every Testcase.

    def setUp(self):
        cd = os.environ.get("DRIVERPATH", "/Users/marellasaibharath/Downloads/chromedriver")
        self.driver = webdriver.Chrome(cd)
        self.base_url = "http://141.73.130.36:7770"
        self.driver.set_window_size(1440, 1024)
        self.driver.maximize_window()
        if not os.path.exists("./Cookies.pkl"):
            driver = self.driver
            driver.get(self.base_url + "/login")
            WebDriverWait(driver,100).until(EC.presence_of_element_located((By.NAME,'email')))
            driver.find_element_by_name("email").send_keys("user@mail.com")
            driver.find_element_by_name("password").send_keys("@pswd")
            driver.find_element_by_class_name('elemXBoxInnButton').click()
            time.sleep(18)
            driver.find_element_by_class_name('elemXBoxInnButton').click()
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, 'elemX-MarketLabel')))
            with open("Cookies.pkl","wb") as Cookies:
                pickle.dump(driver.get_cookies(),Cookies)

    # --> Handling Cookies.

    def handle_Cookies(self):
        driver = self.driver
        with open("Cookies.pkl","rb") as Cookies:
            cookie = pickle.load(Cookies)
            for ck in  cookie:
                driver.add_cookie(ck)



    def test_buy(self):
        driver = self.driver
        driver.get(self.base_url + "/trade")
        self.handle_Cookies()
        driver.get(self.base_url + "/trade")
        for i in range(3):
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'price')))
            driver.find_element_by_class_name('buyPrice').send_keys("10")
            driver.find_element_by_class_name('buyAmount').send_keys("20")
            time.sleep(1)
            driver.find_element_by_class_name('buy').click()
            driver.find_element_by_xpath('//*[@id="elemXShellInnTradingDesk"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]').click()
            time.sleep(1)
            driver.switch_to.alert.accept()



    def test_sell(self):
        driver = self.driver
        driver.get(self.base_url + "/trade")
        self.handle_Cookies()
        driver.get(self.base_url + "/trade")
        for i in range(3):
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.NAME, 'price')))
            driver.find_element_by_class_name('sellPrice').send_keys("10")
            driver.find_element_by_class_name('sellAmount').send_keys("20")
            time.sleep(1)
            driver.find_element_by_class_name('sell').click()
            driver.find_element_by_xpath('//*[@id="elemXShellInnTradingDesk"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]').click()
            time.sleep(1)
            driver.switch_to.alert.accept()

    def tearDown(self):
        self.driver.quit()

    if __name__ == "__main__":
        unittest.main()

