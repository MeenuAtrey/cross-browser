import time
import pytest
import os
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators
from Utils.MiniMap_Util import MiniMap
from pageObjects.LoginPage import Login
from pageObjects.BasePage import Summary


class TestOperator:
    logger = LogGen.log_gen()

    @pytest.mark.regression
    def test_operator_page_and_tabs(self, setup):
        try:
            self.logger.info(
                "***************** Test Operator page load with search and load Op tab pages *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.execute_search_and_click_link("OP:", "Operator", locators.First_link_in_search_results)
            self.summary.check_elem_present("Operator page header", locators.header_Operator)
            self.summary.check_elem_present("Operator Entity Id", locators.Entity_Id_value)
            time.sleep(2)
            MiniMap.CheckMapHideButton(driver)
            MiniMap.CheckMapResizeButtons(driver)
            self.logger.info("***************** Operator Page > Info Tab Test Passed *****************")
            self.summary.operator_page_edit()
            time.sleep(2)
            self.summary.delete_op_feature_override()
            self.summary.delete_op_feature_override()
            self.logger.info("***************** Operator Page Edit and delete feature Test Passed *****************")
            self.summary.click_link_and_assert_elements("Op > Operator Journey Counts tab",
                                                    locators.Operator_Operator_Journey_Counts_Tab,
                                                    "Gantt Chart",
                                                    locators.Gantt_chart_cell,
                                                    "Update chart button",
                                                    locators.Gantt_Update_Charts_button)
            self.logger.info("***************** Operator Page > Operator Journey Counts tab Test Passed *****************")
            self.summary.click_link_and_assert_elements("Op > Line Journey Counts tab",
                                                    locators.Operator_Line_Journey_Counts_Tab,
                                                    "Gantt Chart",
                                                    locators.Gantt_chart_cell,
                                                    "Update chart button",
                                                    locators.Gantt_Update_Charts_button)
            self.logger.info("***************** Operator Page > Line Journey Counts Tab Test Passed *****************")
            driver.quit()
            time.sleep(4)
        except Exception:
            self.driver.quit()
            time.sleep(4)
