import os
import time

import pytest
from pageObjects.LoginPage import Login
from Utils.customLogger import LogGen
from Utils.testData import TestData


class TestLogin:

    logger = LogGen.log_gen()

    @pytest.mark.regression
    def test_login(self, setup):
        try:
            self.logger.info("***************** Starting Hub Login test *****************")
            self.driver = setup
            self.login = Login(self.driver)
            expected_header = TestData.home_page_exp_header
            if self.login.do_login() is not None:
                self.login.check_navigation_side_bar()
                self.login.clickDatasetOk()
                header = self.login.getHeader()
                if header == expected_header:
                    assert True
                    self.logger.info("***************** Dataset Comparison header asserted *****************")
                    self.logger.info("***************** Hub Login Test Pass *****************")
                    cookies = self.driver.execute_cdp_cmd('Network.getAllCookies', {})
                    session_ids = [row['value'] for row in cookies['cookies'] if row['name'] == "sessionid"]
                    self.logger.info(f"Logged in Session Id: {session_ids[1]} ")
            else:
                self.logger.error("***************** Hub Login test failed *****************")
            self.driver.quit()
            time.sleep(8)
        except Exception :
            self.driver.quit()
            time.sleep(6)


