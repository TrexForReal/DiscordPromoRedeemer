import requests
from SourceCode.Modules.config_scr import *

def Obtain_Cookies() -> dict:
        cookies = {}
        try:
            response = requests.get("https://discord.com")
            for cookie in response.cookies:
                if cookie.name.startswith("__") and cookie.name.endswith("uid"):
                    cookies[cookie.name] = cookie.value
            return cookies
        except Exception as e:
            return {}