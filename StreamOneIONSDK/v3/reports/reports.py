import requests
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneIONSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError
import datetime
import csv
from requests import Response
import re


class ReportsV3:
    def __init__(self, base_url: str, access_token: str, account_id: str):
        self.base_url = base_url
        self.access_token = access_token
        self.account_id = account_id

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def list_reports(self, module: Optional[str] = "REPORTS_MODULE_UNSPECIFIED") -> List[Dict]:
        """
        Fetches a list of available reports for the specified module.

        :param module: The module to filter reports by. Defaults to "REPORTS_MODULE_UNSPECIFIED".
        :return: A list of dictionaries containing report metadata.
                """
        headers = self._get_headers()
        params = {"module": module}

        response = requests.get(
            f"{self.base_url}/api/v3/accounts/{self.account_id}/reports",
            headers=headers,
            params=params
        )

        return self._handle_response(response)

    def get_report(self, report_id: str) -> Dict:
        """
        Fetches the details of a specific report by its ID.

        :param report_id: The ID of the report to retrieve.
        :return: A dictionary containing the report details.
        """
        headers = self._get_headers()

        response = requests.get(
            f"{self.base_url}/api/v3/accounts/{self.account_id}/reports/{report_id}",
            headers=headers,
        )
        if response.status_code != 200:
            return self._handle_response(response)
        else:
            return response.json()

    def _handle_response(self, response: requests.Response) -> Union[Dict, List]:
        if response.status_code == 200:
            return response.json().get("reports", [])
        elif response.status_code == 400:
            raise BadRequestError(response.text)
        elif response.status_code == 401:
            raise AuthenticationError(response.text)
        elif response.status_code == 403:
            raise AuthorizationError(response.text)
        elif response.status_code == 404:
            return []
        elif response.status_code >= 500:
            raise ServerError(response.text)
        else:
            response.raise_for_status()

    def _convert_to_csv(self, response: Response, path: str = "report.csv") -> None:
        # Extract the raw text data from the JSON response
        text_data = response.json()["results"]
        path = path if path else "report.csv"

        # Write the raw text data directly to the specified CSV file
        with open(path, mode='w', newline='') as file:
            file.write(text_data)
        return path

    def _create_columns_list(self, columns):
        def camel_to_snake(name):
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

        new_columns = []
        for col in columns:
            new_col = {camel_to_snake(k): v for k, v in col.items()}
            new_columns.append(new_col)
        return new_columns

    def get_report_data_csv(self, report_id: str, start_date: str = None, end_date: str = None, relative_date_range: str = "MONTH_TO_DATE", path="", columns=None) -> requests.Response:
        """
        Fetches the report data in CSV format.

        :param report_id: The ID of the report.
        :param report_module: The module that uses the reports service.
        :param category: The type of report produced.
        :param start_date: The start date for the report data in the format %Y-%m-%dT%H:%M:%SZ (used if relative_date_range is not provided).
        :param end_date: The end date for the report data in the format %Y-%m-%dT%H:%M:%SZ  (used if relative_date_range is not provided).
        :param relative_date_range: A relative date range (e.g.,"UNKNOWN_RELATIVE_DATE_RANGE", "CUSTOM", "TODAY", "MONTH_TO_DATE", "QUARTER_TO_DATE", "YEAR_TO_DATE", "LAST_MONTH", "LAST_QUARTER", "LAST_YEAR", "LATEST_MONTH", "WEEK_TO_DATE", "LAST_WEEK", "TWO_MONTHS_AGO").
        :return: Path to the csv file with the data.
        """

        headers = self._get_headers()
        url = f"{self.base_url}/api/v3/accounts/{self.account_id}/reports/{report_id}/reportDataCsv"
        specs = {
            "date_range_option": {"selected_range": {"relative_date_range": relative_date_range}}
        } if relative_date_range else {
            "date_range_option": {"selected_range": {"fixed_date_range": {
                "start_date": start_date,
                "end_date": end_date
            }}}
        }

        report = self.get_report(report_id)

        specs["selectedColumns"] = report["specs"]["allColumns"]
        payload = {
            "reportId": report_id,
            "report_module": report["reportModule"],
            "category": report["category"],
            "specs": specs,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True
        )
        if response.status_code != 200:
            self._handle_response(response)
        return self._convert_to_csv(response, path)
