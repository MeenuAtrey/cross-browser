import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators
from selenium.webdriver.common.keys import Keys



class Summary:
    logger = LogGen.log_gen()

    def __init__(self, driver):
        self.driver = driver

    def check_Ito_Logo(self):
        try:
            self.driver.find_element(By.XPATH, locators.nav_bar_Ito_Logo_xpath)
            self.logger.info(f"***************** Ito Logo presence asserted *****************")
            assert True
        except NoSuchElementException:
            self.logger.error("***************** Ito Logo assertion failure *****************")
            assert False

    def check_side_menu_element_present(self, menu_elem, menu_element_xpath):
        try:
            self.driver.find_element(By.XPATH, menu_element_xpath)
            self.logger.info(f"***************** {menu_elem} presence asserted *****************")
            assert True
        except NoSuchElementException:
            self.logger.error(f"***************** assertion failure on {menu_elem} presence check *****************")
            assert False

    def click_side_menu_element(self,
                                menu_elem,
                                menu_element_xpath,
                                page_elem1_to_assert,
                                page_elem1_to_assert_xpath,
                                page_elem2_to_assert=None,
                                page_elem2_to_assert_xpath=None,
                                ):
        try:
            self.driver.find_element(By.XPATH, menu_element_xpath).click()
            self.logger.info(f"***************** {menu_elem} clicked *****************")
            WebDriverWait(self.driver, 120).until(
                ec.visibility_of_element_located((By.XPATH, page_elem1_to_assert_xpath)))
            self.logger.info(f"***************** Presence of {page_elem1_to_assert} asserted *****************")
            time.sleep(1)
            assert True
        except NoSuchElementException:
            self.logger.error(
                f"***************** assertion failure on {menu_elem} for {page_elem1_to_assert} check *****************")
            assert False

        if page_elem2_to_assert and page_elem2_to_assert_xpath is not None:
            try:
                WebDriverWait(self.driver, 120).until(
                    ec.visibility_of_element_located((By.XPATH, page_elem2_to_assert_xpath)))
                self.logger.info(f"***************** Presence of {page_elem2_to_assert} asserted *****************")
                time.sleep(3)
                assert True
            except NoSuchElementException:
                self.logger.error(
                    f"***************** assertion failure on {menu_elem} for {page_elem2_to_assert} check *****************")
                assert False

    def check_side_menu_element_hidden(self, menu_elem, menu_element_xpath):
        try:
            self.driver.find_element(By.XPATH, menu_element_xpath)
            self.logger.error(f"************* FAIL - {menu_elem} expected to be hidden found present *****************")
            assert False
        except NoSuchElementException:
            # This exception is expected, Nav bar won't be present without selecting dataset
            self.logger.info(f"***************** {menu_elem} not present for TfWM client as expected *****************")
            pass

    def locate_page_element_by_xpath(self, elem, elem_xpath):
        try:
            self.driver.find_element(By.XPATH, elem_xpath)
            self.logger.info(f"***************** {elem} successfully located *****************")
            assert True
        except NoSuchElementException:
            self.logger.error(f"***************** expected {elem} not located on page *****************")
            assert False

    def click_element(self, elem, elem_xpath):
        try:
            self.driver.find_element(By.XPATH, elem_xpath).click()
            time.sleep(6)
            self.logger.info(f"***************** {elem} clicked *****************")
            assert True
        except NoSuchElementException:
            self.logger.error(f"***************** expected {elem} couldn't be located on page *****************")
            assert False

    def check_elem_present(self, elem, elem_xpath):
        try:
            WebDriverWait(self.driver, 60).until(
                ec.visibility_of_element_located((By.XPATH, elem_xpath)))
            self.logger.info(f"***************** {elem} presence asserted *****************")
            assert True
        except NoSuchElementException:
            self.logger.error(f"***************** assertion failure on {elem} presence check *****************")
            assert False

    def check_elem_hidden(self, elem, elem_xpath):
        try:
            self.driver.find_element(By.XPATH, elem_xpath)
            time.sleep(5)
            self.logger.info(f"***************** {elem} expected to be hidden but found on page *****************")
            assert False
        except NoSuchElementException:
            # This exception is expected
            self.logger.info(f"***************** {elem} hidden as expected *****************")
            pass

    def click_link_and_assert_elements(self,
                                       link,
                                       link_xpath,
                                       page_elem1_to_assert,
                                       page_elem1_to_assert_xpath,
                                       page_elem2_to_assert=None,
                                       page_elem2_to_assert_xpath=None,
                                       ):
        try:
            self.driver.find_element(By.XPATH, link_xpath).click()
            self.logger.info(f"***************** {link} clicked *****************")
            time.sleep(8)
            WebDriverWait(self.driver, 120).until(
                ec.visibility_of_element_located((By.XPATH, page_elem1_to_assert_xpath)))
            self.logger.info(f"***************** Presence of {page_elem1_to_assert} asserted *****************")
            time.sleep(3)
            assert True
        except NoSuchElementException:
            self.logger.error(
                f"***************** assertion failure on {link} for {page_elem1_to_assert} check *****************")
            assert False

        if page_elem2_to_assert and page_elem2_to_assert_xpath is not None:
            try:
                WebDriverWait(self.driver, 120).until(
                    ec.visibility_of_element_located((By.XPATH, page_elem2_to_assert_xpath)))
                self.logger.info(f"***************** Presence of {page_elem2_to_assert} asserted *****************")
                time.sleep(1)
                assert True
            except NoSuchElementException:
                self.logger.error(
                    f"***************** assertion failure on {link} for {page_elem2_to_assert} check *****************")
                assert False

    def execute_search(self, search_string, exp_elem):
        try:
            WebDriverWait(self.driver, 90).until(ec.visibility_of_element_located((By.ID, locators.Header_Search)))
            self.driver.find_element(By.ID, locators.Header_Search).click()
            time.sleep(4)
            self.driver.find_element(By.ID, locators.Header_Search).clear()
            self.driver.find_element(By.ID, locators.Header_Search).send_keys(search_string, Keys.ENTER)
            time.sleep(4)
            WebDriverWait(self.driver, 90).until(ec.visibility_of_element_located((By.XPATH, exp_elem)))
            self.logger.info(f"***************** search executed with search string {search_string} *****************")
            assert True
        except Exception:
            self.logger.error(
                f"***************** search execution for search string {search_string} failed *****************")
            assert False

    def execute_search_and_click_link(self, search_string, exp_elem, exp_elem_xpath):
        try:
            WebDriverWait(self.driver, 60).until(ec.visibility_of_element_located((By.ID, locators.Header_Search)))
            self.driver.find_element(By.ID, locators.Header_Search).click()
            time.sleep(4)
            self.driver.find_element(By.ID, locators.Header_Search).clear()
            self.driver.find_element(By.ID, locators.Header_Search).send_keys(search_string, Keys.ENTER)
            time.sleep(4)
            WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.XPATH, exp_elem_xpath)))
            self.logger.info(f"***************** search executed with search string {search_string} *****************")
            assert True
        except Exception:
            self.logger.error(
                f"***************** search execution for search string {search_string} failed *****************")
            assert False

        try:
            self.driver.find_element(By.XPATH, exp_elem_xpath).click()
            time.sleep(3)
            self.logger.info(f"***************** {exp_elem} link clicked *****************")
        except Exception:
            self.logger.error(
                f"***************** search of {search_string} failed to find expected element {exp_elem}*****************")
            assert False

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
