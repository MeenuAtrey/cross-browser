import time
import pytest
import os
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators
from Utils.MiniMap_Util import MiniMap
from pageObjects.LoginPage import Login
from pageObjects.BasePage import Summary


class TestLine:
    logger = LogGen.log_gen()

    @pytest.mark.regression
    @pytest.mark.skip("Skip in daily CI pipeline")
    def test_line_page_and_tabs(self, setup):
        try:
            self.logger.info("***************** Test Line page load using search and load tab pages *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.execute_search_and_click_link("LI:", "Line", locators.First_link_in_search_results)
            self.summary.check_elem_present("Line page header", locators.header_Line)
            self.summary.check_elem_present("Line Entity Id", locators.Entity_Id_value)
            time.sleep(3)
            MiniMap.CheckMapHideButton(driver)
            MiniMap.CheckMapResizeButtons(driver)
            self.logger.info("***************** Line Page > Info Tab Test Passed *****************")
            self.summary.click_link_and_assert_elements("Line > Service Pattern Tab",
                                                        locators.Line_Service_Patterns_Tab,
                                                        "Service Pattern header",
                                                        locators.Line_SP_Service_Patterns_header)
            self.logger.info("***************** Line Page > Service Pattern Tab Test Passed *****************")
            self.summary.click_link_and_assert_elements("Line > Anomalies Tab",
                                                        locators.Line_Anomalies_Tab,
                                                        "Journey Count Baseline header",
                                                        locators.Line_Anomalies_Journey_Count_Baseline_header)
            self.logger.info("***************** Line Page > Anomalies Tab Test Passed *****************")
            self.summary.click_link_and_assert_elements("Line > Warnings Tab",
                                                        locators.Line_Warnings_Tab,
                                                        "All button",
                                                        locators.Line_Warnings_All_button)
            self.logger.info("***************** Line Page > Warnings Tab Test Passed *****************")
            self.summary.click_link_and_assert_elements("Line > Interventions Tab",
                                                        locators.Line_Interventions_Tab,
                                                        "Model Objects Logs",
                                                        locators.Line_Interventions_Model_Object_Logs_header)
            self.logger.info("***************** Line Page > Interventions Tab Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            driver.quit()
            time.sleep(3)
