import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators
from Utils.Config import Config


class Login:

    username = Config.username
    password = Config.password
    logger = LogGen.log_gen()

    def __init__(self, driver):
        self.driver = driver
        time.sleep(12)

    def setUserName(self, username):
        WebDriverWait(self.driver, 180).until(
            ec.visibility_of_element_located((By.XPATH, locators.textbox_email_xpath)))
        time.sleep(6)
        self.driver.find_element(By.XPATH, locators.textbox_email_xpath).clear()
        self.driver.find_element(By.XPATH, locators.textbox_email_xpath).send_keys(username)

    def setPassword(self, password):
        WebDriverWait(self.driver, 60).until(
            ec.visibility_of_element_located((By.XPATH, locators.textbox_password_xpath)))
        self.driver.find_element(By.XPATH, locators.textbox_password_xpath).clear()
        self.driver.find_element(By.XPATH, locators.textbox_password_xpath).send_keys(password)

    def clickSignIn(self):
        WebDriverWait(self.driver, 90).until(
            ec.visibility_of_element_located((By.XPATH, locators.button_sign_in_xpath)))
        self.driver.find_element(By.XPATH, locators.button_sign_in_xpath).click()
        time.sleep(14)
        WebDriverWait(self.driver, 120).until(
            ec.visibility_of_element_located((By.XPATH, locators.button_dataset_selection_Ok_xpath)))

    def clickDatasetOk(self):
        WebDriverWait(self.driver, 120).until(
            ec.visibility_of_element_located((By.XPATH, locators.button_dataset_selection_Ok_xpath)))
        self.logger.info("***************** Explicit wait resolved for dataset OK button *****************")
        self.driver.find_element(By.XPATH, locators.button_dataset_selection_Ok_xpath).click()
        time.sleep(8)
        self.logger.info("***************** Dataset selector Ok button clicked *****************")
        if self.getHeader() == "Dataset Comparison":
            self.logger.info("***************** TfWM Dataset loaded *****************")

    def clickSignOut(self):
        WebDriverWait(self.driver, 120).until(
            ec.visibility_of_element_located((By.XPATH, locators.button_Logged_in_user_xpath)))
        self.driver.find_element(By.XPATH, locators.button_Logged_in_user_xpath).click()
        self.driver.wait(3)
        self.driver.find_element(By.XPATH, locators.button_sign_out_xpath).click()

    def getHeader(self):
        try:
            header = self.driver.find_element(By.ID, locators.header_dataset_comparison_id).text
            return header
        except Exception as e:
            WebDriverWait(self.driver, 480).until(
                    ec.invisibility_of_element_located((By.XPATH, locators.banner_Dataset_loading_xpath)))
            time.sleep(3)
            header = self.driver.find_element(By.ID, locators.header_dataset_comparison_id).text
            return header

    def do_login(self):
        self.setUserName(username=self.username)
        self.setPassword(password=self.password)
        self.clickSignIn()
        self.driver.maximize_window()
        time.sleep(5)
        if self.driver:
            self.logger.info("***************** Sign In successful *****************")
            return self.driver
        else:
            self.logger.info("***************** Sign In Failed *****************")
            return None

    def do_login_and_load_dataset(self):
        self.driver = self.do_login()
        time.sleep(5)
        self.clickDatasetOk()
        time.sleep(3)
        return self.driver

    def check_navigation_side_bar(self):
        try:
            self.driver.find_element(By.XPATH, locators.side_nav_bar_element_xpath)
            self.logger.error("<br />***************** Side Nav bar enabled without dataset selection *****************")
            assert False
        except NoSuchElementException:
            # This exception is expected, Nav bar won't be present without selecting dataset
            self.logger.info("***************** Side menu asserted as disabled when no dataset loaded *****************")
            time.sleep(1)
            pass

