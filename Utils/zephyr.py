from requests import Session, Request
from Utils import zephyr_settings


class Zephyr:
    url = 'https://api.zephyrscale.smartbear.com/v2'
    cache = {}

    def __init__(self, token: str) -> None:
        self.session = Session()
        self.session.headers = {'Authorization': f'Bearer {token}'}

    def reset_cache(self) -> None:
        self.cache = {}

    def get(self, endpoint: str, params: dict = {}, full_url: bool = False) -> dict:
        if params:
            endpoint += '?' + '&'.join(f'{k}={v}' for k, v in params.items())
        if endpoint not in self.cache:
            self.cache[endpoint] = self.session.get(endpoint if full_url else f'{self.url}/{endpoint}').json()
        return self.cache[endpoint]

    def post(self, endpoint: str, data: dict) -> dict:
        return self.session.post(f'{self.url}/{endpoint}', json=data).json()

    def put(self, endpoint: str, data: dict) -> Request:
        return self.session.put(f'{self.url}/{endpoint}', json=data)

    def create_folder(self, project_key: str, name: str, type: str = 'TEST_CYCLE') -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/createFolder"""
        return self.post('folders', {'projectKey': project_key, 'folderType': type, 'name': name})

    def get_folders(self, project_key: str, type: str = 'TEST_CYCLE') -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/listFolders"""
        return self.get('folders', {'projectKey': project_key, 'folderType': type})['values']

    def get_folder(self, project_key: str, name: str, type: str = 'TEST_CYCLE') -> dict:
        """Returns the folder that matches the name, not the API call for getfolder"""
        return next((f for f in self.get_folders(project_key, type=type) if f['name'] == name), None)

    def get_testcase_folders(self, project_key: str, max_results: int = 2000) -> dict:
        """https://api.zephyrscale.smartbear.com/v2/folders"""
        params = {'maxResults': max_results}
        if project_key:
            params['projectKey'] = project_key
        return self.get('folders', params)['values']

    def get_tests(self, project_key: str = None, max_results: int = 2000) -> list:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/listTestCases"""
        params = {'maxResults': max_results}
        if project_key:
            params['projectKey'] = project_key

        return self.get('testcases', params)['values']

    def get_cycles(self, project_key: str, folder_id: str = None, max_results: int = 1000) -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/listTestCycles"""
        params = {'projectKey': project_key, 'maxResults': max_results}
        if folder_id:
            params['folderId'] = folder_id

        return self.get('testcycles', params=params)

    def get_cycle(self, project_key: str, name: str, folder_id: str = None) -> dict:
        """Returns the cycle that matches the name, not the API call for getcycle"""
        return next((c for c in self.get_cycles(project_key, folder_id=folder_id)['values'] if c['name'].lower().endswith(name.lower())), None)

    def get_cycle_by_id(self, cycle_id: int) -> dict:
        """Returns the specific test cycle details for the given ID.

        https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/getTestCycle
        """
        return self.get(f"testcycles/{cycle_id}")

    def create_cycle(self, project_key: str, name: str, folder_id: str = None) -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/createTestCycle"""
        data = {'projectKey': project_key, 'name': name}
        if folder_id:
            data['folderId'] = folder_id

        return self.post('testcycles', data=data)

    def create_execution(self, project_key: str, test_key: str, cycle_key: str, status_name: str, comment, **kwargs) -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/createTestExecution
           Valid Kwargs: comment, environment, elapsed, executed_by, assignTo
        """
        data = {'projectKey': project_key, 'testCaseKey': test_key,
                'testCycleKey': cycle_key, 'statusName': status_name,
                'comment': comment}
        for key, value in kwargs.items():
            if key == "comment":
                data['comment'] = value
            elif key == "environment":
                data['environmentName'] = value
            elif key == "elapsed":
                data['executionTime'] = value
            elif key == "executed_by":
                data['executedById'] = value
            data['assignedToId'] = zephyr_settings.User_Id
        return self.post('testexecutions', data)

    def get_executions(self, project_key: str, cycle_key: str = None, testcase_key: str = None, max_results: int = 1000) -> list:
        params = {'projectKey': project_key,
                  'maxResults': max_results}

        if cycle_key:
            params['testCycle'] = cycle_key
        if testcase_key:
            params['testCase'] = testcase_key

        return self.get('testexecutions', params=params)['values']

    def update_case(self, case: dict) -> Request:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/updateTestCase"""
        return self.put(f'testcases/{case["key"]}', case)

    def get_automated_tests(self, project_key: str) -> dict:
        """Gets all tests for a project and returns those with an automation name"""
        return {x['customFields']['Automation Name']: x for x in self.get_tests(project_key)
                if x['customFields']['Automation Name']}

    def create_test_script(self) -> dict:
        """https://support.smartbear.com/zephyr-scale-cloud/api-docs/#operation/createTestCaseTestScript"""
        raise NotImplementedError

    def get_cycles_for_automatated_test(self, project_key, automated_test_name):
        """Return the cycle IDs for the given automation method name. Project key e.g. 'BODP' """
        cycles = []
        testcase = self.get_automated_tests(project_key).get(automated_test_name, None)
        try:
            params = {
                "projectKey": project_key,
                "testCase":testcase['key']
                    }
        except TypeError:
            return None
        execs = self.get('testexecutions',params)
        for execution in execs['values']:
            tc_execution = execution['testCase']['id']
            if testcase['id'] == tc_execution:
                cycle_id = execution['testCycle']['id']
                if cycle_id not in cycles:
                    cycles.append(cycle_id)
        return cycles

