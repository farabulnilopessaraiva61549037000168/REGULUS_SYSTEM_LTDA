# seo_manager/wix_api_integration.py

import requests

class WixSEOManager:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.wix.com"

    def update_meta_description(self, site_id, description):
        endpoint = f"{self.base_url}/sites/{site_id}/seo"
        payload = {
            "metaDescription": description
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.patch(endpoint, json=payload, headers=headers)
        return response.json()

    def connect_search_console(self, site_id):
        endpoint = f"{self.base_url}/sites/{site_id}/connect-google-search-console"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(endpoint, headers=headers)
        return response.json() 

