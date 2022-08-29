import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators


class FeaturePage:
    logger = LogGen.log_gen()

    def __init__(self, driver):
        self.driver = driver

    def operator_page_edit(self):
        try:
            self.driver.find_element(By.XPATH, locators.Edit_button).click()
            time.sleep(5)
            try:
                self.driver.find_element(By.XPATH, locators.Text_Colour_Select_Tab).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, locators.Text_Colour_Scroll).click()
                self.driver.find_element(By.XPATH, locators.Text_Colour_Select_Enter).click()
                time.sleep(3)
                self.logger.info("*************** Text Colour selected ***************")

            except Exception as e:

                self.logger.error(e)
                self.logger.error("*************** Error while selecting Text Colour field ***************")
                assert False

            try:
                self.driver.find_element(By.XPATH, locators.Op_Colour_Select_Tab).click()
                time.sleep(3)
                self.driver.find_element(By.XPATH, locators.Op_Colour_Scroll).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, locators.Op_Colour_Select_Enter).click()
                time.sleep(5)
                self.logger.info("*************** Colour selected ***************")
            except Exception as e:
                self.logger.error(e)
                self.logger.error("*************** Error while selecting Colour field ***************")
                assert False

            try:
                self.driver.find_element(By.XPATH, locators.Scroll_to_top_button).click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, locators.Save_button).click()
                time.sleep(4)
                self.logger.info("*************** Save button clicked ***************")
                self.driver.find_element(By.XPATH, locators.SaveSuccessPopUp).is_displayed()
                self.logger.info("*************** Changes Saved successfully ***************")
                time.sleep(14)
                WebDriverWait(self.driver, 120).until(
                    ec.presence_of_element_located((By.XPATH, locators.Entity_Id_value)))
            except Exception as e:
                self.logger.error(e)
                self.logger.error("*************** Exception in clicking Save button ***************")
                assert False
        except Exception as e:
            self.logger.error(e)
            self.logger.error("*************** Exception in clicking Edit button ***************")
            assert False

    def delete_op_feature_override(self):
        try:
            self.driver.find_element(By.XPATH, locators.Op_Colour_DeleteBin).click()
            time.sleep(1)
            self.driver.find_element(By.XPATH, locators.DeleteSuccessPopUp).is_displayed()
            self.logger.info("*************** Feature override deleted ***************")
            time.sleep(2)
        except Exception as e:
            self.logger.error(e)
            self.logger.error("*************** Exception in deleting feature override ***************")
            assert False
