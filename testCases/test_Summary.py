import pytest
import time
import os
from Utils.customLogger import LogGen
from Utils.selenium_locators import locators
from Utils.MiniMap_Util import MiniMap
from pageObjects.LoginPage import Login
from pageObjects.BasePage import Summary


class TestSummary:
    logger = LogGen.log_gen()

    # @pytest.mark.skip(reason="Skipping for demo")
    @pytest.mark.regression
    def test_ito_logo_and_menu_items_navigation(self, setup):
        try:
            self.logger.info("***************** Test Summary Page *****************")
            self.logger.info("***************** Test presence of Ito Logo in left menu *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.check_Ito_Logo()
            self.logger.info("***************** Ito Logo on left menu asserted *****************")
            self.logger.info(
                "***************** Beginning to test side menu navigation and assert page elements ******************")
            self.summary.locate_page_element_by_xpath("Summary table", locators.Table)
            self.summary.click_side_menu_element(
                "Dataset Info", locators.menu_Dataset_Info_xpath, "DATASET INFO header",
                locators.dataset_info_header, "Databases Table", locators.Table)
            self.summary.locate_page_element_by_xpath("Source Files", locators.dataset_info_Source_Files)
            self.summary.click_side_menu_element(
                "Situations", locators.menu_Situations_xpath, "Situations page header", locators.situations_header)
            self.summary.click_side_menu_element(
                "Map", locators.menu_Map_xpath, "Mapbox logo", locators.mapbox_logo)
            self.summary.check_side_menu_element_present("Warnings", locators.menu_Warnings_xpath)
            self.summary.click_element("Warnings expand button", locators.menu_Warnings_expand_button_xpath)
            self.summary.click_side_menu_element(
                "Anomalies", locators.menu_Anomalies_xpath, "Anomalies header", locators.header_anomalies)
            self.summary.click_element("Interventions expand button",
                                       locators.menu_Interventions_expand_button_xpath)
            self.summary.click_side_menu_element(
                "Current Interventions", locators.menu_Current_Interventions_xpath,
                "Current Interventions header", locators.header_current_interventions)
            self.summary.click_side_menu_element(
                "Mass Interventions", locators.menu_Mass_Interventions_xpath,
                "Mass Interventions header", locators.header_mass_interventions)
            self.summary.click_side_menu_element(
                "Rule Interventions", locators.menu_Rule_Interventions_xpath,
                "Rule Interventions header", locators.header_rule_interventions)
            self.summary.click_side_menu_element(
                "Warning Descriptions", locators.menu_Warning_Descriptions_xpath, "Warning Descriptions header",
                locators.header_warning_descriptions, "Bezier opposite definition",
                locators.Warning_Definitions_Bezier_opposite)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    def test_menu_collapse_expand(self, setup):
        try:
            self.logger.info("***************** Test Menu Expand Collapse function *****************")
            self.driver = setup
            self.login = Login(setup)
            time.sleep(3)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.click_element("Side menu collapse button", locators.menu_collapse_button_xpath)
            self.summary.check_elem_hidden("Dataset Info", locators.menu_Dataset_Info_xpath)
            self.summary.check_elem_hidden("Interventions", locators.menu_Interventions_xpath)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(4)
        except Exception:
            self.driver.quit()
            time.sleep(4)

    @pytest.mark.regression
    def test_menu_items_hidden(self, setup):
        try:
            self.logger.info("***************** Test Menu Items hidden for TfWM *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            time.sleep(2)
            self.summary.check_side_menu_element_hidden("Service Links", locators.menu_Service_Links_xpath)
            self.summary.check_side_menu_element_hidden("Ito Objects", locators.menu_Service_Links_xpath)
            self.summary.check_side_menu_element_hidden("Quality Dimensions", locators.menu_Service_Links_xpath)
            self.summary.check_side_menu_element_hidden("Intervention Map Tool", locators.menu_Service_Links_xpath)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    def test_footer_link_Glossary(self, setup):
        try:
            self.logger.info("***************** Test Footer Link Glossary *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.click_link_and_assert_elements("Glossary footer Link", locators.link_Glossary_xpath,
                                                        "Glossary header", locators.Glossary_header,
                                                        "Journey Association link on Glossary",
                                                        locators.Glossary_Journey_Association_link)
            self.summary.click_link_and_assert_elements("Journey Association link on Glossary",
                                                        locators.Glossary_Journey_Association_link,
                                                        "Journey Association table header on glossary",
                                                        locators.Glossary_Journey_Association_table_header)
            self.summary.click_element("Scroll to Top button", locators.Scroll_to_top_button)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    def test_footer_link_Licences(self, setup):
        try:
            self.logger.info("***************** Test Footer Link Licences *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.click_link_and_assert_elements("Licences footer Link", locators.link_Licences_xpath,
                                                        "Licences header", locators.Licences_header,
                                                        "MIT Licences paragraph",
                                                        locators.Licences_MIT_Licences_text)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    # @pytest.mark.skip(reason="Skipping from CI run")
    def test_footer_link_Privacy_Policy(self, setup):
        try:
            self.logger.info("***************** Test Footer Link Privacy Policy *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            main_window = driver.current_window_handle
            self.summary.click_element("Privacy Link in footer", locators.link_Privacy_Policy_xpath)
            time.sleep(10)
            privacy_policy_tab = driver.window_handles[1]
            driver.switch_to.window(privacy_policy_tab)
            time.sleep(8)
            self.summary.check_elem_present("Privacy Policy header", locators.privacy_policy_header)
            driver.close()
            driver.switch_to.window(main_window)
            driver.switch_to.default_content()
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(6)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    def test_feature_page_launch_with_search(self, setup):
        try:
            self.logger.info("***************** Test Feature page load with search *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.execute_search_and_click_link("LI:", "Line", locators.First_link_in_search_results)
            self.summary.check_elem_present("Line page header", locators.header_Line)
            self.summary.check_elem_present("Line Entity Id", locators.Entity_Id_value)
            time.sleep(2)
            MiniMap.CheckMapHideButton(driver)
            MiniMap.CheckMapResizeButtons(driver)
            self.summary.execute_search_and_click_link("St:", "Stop", locators.First_link_in_search_results)
            self.summary.check_elem_present("Stop page header", locators.header_Stop)
            self.summary.check_elem_present("Stop Entity Id", locators.Entity_Id_value)
            time.sleep(4)
            MiniMap.CheckMapHideButton(driver)
            MiniMap.CheckMapResizeButtons(driver)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)

    @pytest.mark.regression
    def test_individual_warning_navigating_from_summary(self, setup):
        try:
            self.logger.info("***************** Test Feature page load with search *****************")
            self.driver = setup
            self.login = Login(setup)
            driver = self.login.do_login_and_load_dataset()
            self.summary = Summary(driver)
            self.summary.click_element("Summary > Warnings tab", locators.Summary_Warnings_xpath)
            time.sleep(2)
            self.summary.click_element("West Midlands Journeys link", locators.Warnings_West_Midlands_Journeys)
            self.summary.click_link_and_assert_elements("West Midlands Bezier Direction Warnings",
                                                        locators.Warnings_West_Midlands_Journeys_Bezier_Direction,
                                                        "West Midlands Warnings page header",
                                                        locators.West_Midlands_Warnings_header,
                                                        "Results for Bezier direction banner",
                                                        locators.Warnings_Results_for_Bezier_direction_banner)
            time.sleep(3)
            MiniMap.CheckPresenceOfMap(driver)
            self.logger.info("***************** Test Passed *****************")
            driver.quit()
            time.sleep(5)
        except Exception:
            self.driver.quit()
            time.sleep(5)
