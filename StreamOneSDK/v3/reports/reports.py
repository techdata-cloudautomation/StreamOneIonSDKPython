import requests
from typing import Dict, List, Optional, Union
from ...exceptions import StreamOneSDKException, BadRequestError, AuthenticationError, AuthorizationError, NotFoundError, ServerError
import datetime
import csv
from requests import Response


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
        headers = self._get_headers()
        params = {"module": module}

        response = requests.get(
            f"{self.base_url}/api/v3/accounts/{self.account_id}/reports",
            headers=headers,
            params=params
        )
        return self._handle_response(response)

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

    def get_report_data_csv(self, report_id: str, report_module: str, category: str, start_date: str = None, end_date: str = None, relative_date_range: str = "MONTH_TO_DATE", path="") -> requests.Response:
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
            "date_range_option": {"select_date_range": relative_date_range}
        } if relative_date_range else {
            "date_range_option": {"fixed_date_range": {
                "start_date": start_date,
                "end_date": end_date
            }}
        }

        payload = {
            "report_id": report_id,
            "report_module": report_module,
            "category": category,
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
