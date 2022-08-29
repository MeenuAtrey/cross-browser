from selenium.webdriver.support.ui import WebDriverWait
from Utils.selenium_locators import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Utils.zephyr import Zephyr
from Utils import zephyr_settings
from Utils.customLogger import LogGen
import time


class MiniMap:
    zephyr = Zephyr(zephyr_settings.ZEPHYR_TOKEN)
    logger = LogGen.log_gen()

    @staticmethod
    def CheckPresenceOfMap(driver, testcase_key=None):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, locators.Mini_Map_mapbox)))
            MiniMap.logger.info("*************** Mini Map asserted *******************")
        except Exception as e:
            if testcase_key:
                MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                zephyr_settings.cycle_key, "Fail",
                                                "MiniMap Error")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** Exception in identifying Mini Map on page ***************")
            assert False

    @staticmethod
    def CheckPresenceOfMapButtons(driver, testcase_key=None):
        try:
            driver.find_element(By.XPATH, locators.Mini_Map_Resize_plus_button).is_enabled()
            driver.find_element(By.XPATH, locators.Mini_Map_Resize_minus_button).is_enabled()
            driver.find_element(By.XPATH, locators.Mini_Map_Reset_button).is_enabled()
            driver.find_element(By.XPATH, locators.Mini_Map_Hide_button).is_enabled()
            MiniMap.logger.info("*************** All Map Buttons are Enabled on page ***************")

        except Exception as e:
            if testcase_key:
                MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                zephyr_settings.cycle_key, "Fail",
                                                "Exception in Map Buttons functionality")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** Exception in Map Buttons functionality ***************")
            assert False

    # Check Map Hide/Map Recover button
    @staticmethod
    def CheckMapHideButton(driver, testcase_key=None):
        try:
            driver.find_element(By.XPATH, locators.Mini_Map_Mapbox_Logo)
            driver.find_element(By.XPATH, locators.Mini_Map_Hide_button).click()
            time.sleep(3)
            MiniMap.logger.info("*************** Map Hide button clicked ***************")

        except Exception as e:
            if testcase_key:
                MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                zephyr_settings.cycle_key, "Fail",
                                                "Exception in Map Hide button functionality")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** Exception in Map Hide button functionality ***************")
            assert False

        try:
            driver.assertFalse(driver.find_element(By.XPATH, locators.Mini_Map_Mapbox_Logo))

        except Exception as e:
            # Its Ok we expect this element not to be present on page after Map Hide button click
            MiniMap.logger.info("*************** Map hidden now ***************")

        try:
            driver.find_element(By.XPATH, locators.Mini_Map_Recover_button).click()
            time.sleep(3)
            MiniMap.logger.info("*************** Map recover button clicked ***************")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, locators.Mini_Map_Mapbox_Logo)))
            MiniMap.logger.info("*************** Map displayed on page ***************")

        except Exception as e:
            if testcase_key:
                MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                zephyr_settings.cycle_key, "Fail",
                                                "Exception in Map Hide button functionality")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** Map Hide button re-click - Error ***************")
            assert False

    @staticmethod
    def CheckMapResizeButtons(driver, testcase_key=None):
        try:
            elem = driver.find_element(By.XPATH, locators.Mini_Map_Canvas)
            MiniMap.logger.info("*************** Map Canvas detected ***************")
            time.sleep(1)
            orig_Map_width = elem.size.get('width')
            orig_Map_height = elem.size.get('height')
            try:
                driver.find_element(By.XPATH, locators.Mini_Map_Resize_minus_button).click()
                time.sleep(3)
                map_after_minus = driver.find_element(By.XPATH, locators.Mini_Map_Canvas)
                MiniMap.logger.info("*************** Map Canvas detected after clicking on '-' button ***************")
                map_width_after_minus = map_after_minus.size.get('width')
                map_height_after_minus = map_after_minus.size.get('height')
                try:
                    if map_width_after_minus < orig_Map_width and map_height_after_minus < orig_Map_height:
                        MiniMap.logger.info(
                            "*************** Map size check - success - reduced after clicking on '-' button ***************")
                    else:
                        if testcase_key:
                            MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                            zephyr_settings.cycle_key, "Fail",
                                                            "Map size not reduced after clicking '-' button")
                        MiniMap.logger.info(
                            "*************** Map size not reduced after clicking '-' button ***************")
                except Exception as e:
                    if testcase_key:
                        MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                        zephyr_settings.cycle_key, "Fail",
                                                        "Map size error after clicking '-' button")
                    MiniMap.logger.error("*************** Map size error after clicking '-' button ***************")
                    assert False
            except Exception as e:
                if testcase_key:
                    MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                    zephyr_settings.cycle_key, "Fail",
                                                    "Map '-' button click Error")
                MiniMap.logger.error("*************** Map '-' button click Error ***************")
                assert False
            try:
                driver.find_element(By.XPATH, locators.Mini_Map_Resize_plus_button).click()
                time.sleep(3)
            except Exception as e:
                if testcase_key:
                    MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                    zephyr_settings.cycle_key, "Fail",
                                                    "Error on click Map plus button followed by clicking Map minus button")
                MiniMap.logger.error(
                    " *************** Error on clicking Map plus button after clicking Map minus button ***************")
            try:
                driver.find_element(By.XPATH, locators.Mini_Map_Resize_plus_button).click()
                time.sleep(3)
                map_after_plus = driver.find_element(By.XPATH, locators.Mini_Map_Canvas)
                MiniMap.logger.info("*************** Map Canvas detected after clicking on '+' button ***************")
                map_width_after_minus = map_after_plus.size.get('width')
                map_height_after_minus = map_after_plus.size.get('height')
                try:
                    if map_width_after_minus > orig_Map_width and map_height_after_minus > orig_Map_height:
                        MiniMap.logger.info(
                            "*************** Map size check - success - increased after clicking on '+' button ***************")
                    else:
                        if testcase_key:
                            MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                            zephyr_settings.cycle_key, "Fail",
                                                            "Map size not increased after clicking '+' button")
                        MiniMap.logger.error(
                            "*************** Map size not increased after clicking '+' button ***************")
                except Exception as e:
                    if testcase_key:
                        MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                        zephyr_settings.cycle_key, "Fail",
                                                        "Map size error after clicking '+' button")
                    MiniMap.logger.error("*************** Map size error after clicking '+' button ***************")
                    assert False
            except Exception as e:
                if testcase_key:
                    MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                    zephyr_settings.cycle_key, "Fail",
                                                    "Map '+' button click Error")
                MiniMap.logger.error("*************** Map '+' button click Error ***************")
                assert False
        except Exception as e:
            if testcase_key:
                MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                                zephyr_settings.cycle_key, "Fail",
                                                "Map Coordinates Error")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** Map Coordinates Error ***************")
            assert False

    @staticmethod
    def CheckMapSeeinbutton(cls, driver, testcase_key, locator):
        main_window = driver.current_window_handle

        try:
            time.sleep(2)
            select_map_from = driver.find_element(By.XPATH, locators.Mini_Map_See_in_button)
            select_map_from.click()
            time.sleep(1)
            driver.find_element(By.XPATH, locators.Mini_Map_See_in_Google_Maps_option).click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            MiniMap.logger.info("*************** Google Maps opened successfully ***************")
            driver.close()
            driver.switch_to.window(main_window)
            driver.switch_to.default_content()
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, locator)))
            MiniMap.logger.info(" *************** Back to Ito Edit main window ***************")

        except Exception as e:
            MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                            zephyr_settings.cycle_key, "Fail",
                                            "Map See in Error - Google Maps")
            MiniMap.logger.error(e)
            MiniMap.logger.error("*************** SP - Map See in Error - Google Maps ***************")
            cls.fail()

        try:
            select_map_from.click()
            driver.find_element(By.XPATH, locators.Mini_Map_See_in_ITO_Map_option).click()
            time.sleep(2)
            WebDriverWait(driver, 120).until(
                EC.presence_of_element_located((By.XPATH, locators.Mini_MapSeein_ITOMap_MapBoundary)))
            cls.assertIn("map_browser", driver.current_url)
            MiniMap.logger.info("*************** ITO Map Browser opened successfully ***************")
            driver.back()
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, locator)))
            MiniMap.logger.info("*************** Back to Ito Edit main window ***************")

        except Exception as e:
            MiniMap.zephyr.create_execution(zephyr_settings.project_key, testcase_key,
                                            zephyr_settings.cycle_key, "Fail",
                                            "Map See in Error - ITO Map Browser")
            MiniMap.logger.error(e)
            MiniMap.logger.error(
                "*************** SP - Patterns Tab - Map See in Error - ITO Map Browser ***************")
            cls.fail()
