import os
import requests
import logging


class Analitycs:
    TARGET_URL = 'https://www.google-analytics.com/mp/collect'
    SHARE_URL = os.environ['SHARE_URL']

    @staticmethod
    def send_analytics(user_id, lang_code, action_name):
        params = {
            "client_id": str(user_id),
            "user_id": str(user_id),
            "events": [
                {
                    "name": action_name,
                    "params": {
                        "language": lang_code,
                        "engagement_time_msec": "1"
                    }
                }
            ]
        }

        try:
            requests.post(
                f'{Analitycs.TARGET_URL}?measurement_id={os.environ["MEASUREMENT_ID"]}&api_secret={os.environ["API_SECRET"]}',
                json=params)
        except requests.exceptions.RequestException as ex:
            logging.error(ex)
