import tls_client
from SourceCode.Modules.logger import *
from SourceCode.main.fingerprints import fps
import random
from SourceCode.main.cookie_scraper import Obtain_Cookies
from SourceCode.Modules.config_scr import *
import time
import uuid

success = 0
counter = {}


class Redeemer:
    def __init__(self, vcc, promo, token):
        self.start = time.time()
        ja3_properties = random.choice(fps)
        counter_json = {token: 0}
        self.max_tries = 3
        self.promo = promo
        self.vcc = vcc
        counter.update(counter_json)
        self.chrome = "126"
        ja3 = ja3_properties["ja3"]
        self.client = tls_client.Session(
            client_identifier="chrome_126", random_tls_extension_order=True,
            ja3_string=ja3
        )
        if parseConfig()["ProxySetting"]["UseProxy"]:
            self.client.proxies = {
                "http": f"http://" + parseConfig()["ProxySetting"]["Proxy"],
                "https": f"http://" + parseConfig()["ProxySetting"]["Proxy"],
            }
        else:
            self.client.proxies = None
        self.ua = ja3_properties["user-agent"]
        self.full_token = token
        self.token = token if not "@" in token else token.split(":")[2]
        self.xprop = ja3_properties["x-super-properties"]
        self.sleep_after = parseConfig()["Redeeming"]["SleepAfterRedeem"]
        self.SleepAfterXAmountOfRedeems = parseConfig()["Redeeming"][
            "SleepAfterXAmountOfRedeems"
        ]
        self.SleepAfterXAmountOfRedeemsDelay = parseConfig()["Redeeming"][
            "SleepAfterXAmountOfRedeemsDelay"
        ]

    def Watermark(self):

        config = parseConfig()
        wcfg = config["Watermarking"]
        wc = 0
        if wcfg["Use"] == True:
            headers = {
                "accept": "*/*",
                "accept-language": "en-US,en;q=0.9",
                "authorization": self.token,
                "content-type": "application/json",
                "origin": "https://discord.com",
                "priority": "u=1, i",
                "referer": "https://discord.com/channels/@me",
                "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not;A=Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": self.ua,
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-discord-timezone": "Asia/Katmandu",
                "x-super-properties": self.xprop,
            }
            json_data = {
                "bio": wcfg["BIO"],
            }
            response = self.client.patch(
                "https://discord.com/api/v9/users/@me/profile",
                cookies=Obtain_Cookies(),
                headers=headers,
                json=json_data,
            )
            if response.status_code == 200:
                wc += 1
            else:
                pass
            json_data = {
                "global_name": wcfg["GlobalName"],
            }
            response = self.client.patch(
                "https://discord.com/api/v9/users/@me",
                cookies=Obtain_Cookies(),
                headers=headers,
                json=json_data,
            )
            if response.status_code == 200:
                wc += 1
            else:
                pass
            json_data = {
                "pronouns": wcfg["Pronouns"],
            }
            response = self.client.patch(
                "https://discord.com/api/v9/users/@me/profile",
                cookies=Obtain_Cookies(),
                headers=headers,
                json=json_data,
            )
            if response.status_code == 200:
                wc += 1
            else:
                pass
            TL.log("INFO", f"Watermarked -> {blue}3/{wc} ( {wc} Out of 3 )", blue)
        else:
            pass
    def CardRemover(self,payment_source):
        headers = {
                    "authority": "discord.com",
                    "accept": "*/*",
                    "accept-language": "en-US,en;q=0.9",
                    "authorization": self.token,
                    "referer": "https://discord.com/channels/@me",
                    "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": self.ua,
                    "x-debug-options": "bugReporterEnabled",
                    "x-discord-locale": "en-US",
                    "x-discord-timezone": "Europe/Budapest",
                    "x-super-properties": self.xprop,
                }
        response = self.client.get(
                    "https://discord.com/api/v9/users/@me/billing/subscriptions",
                    headers=headers,
                    cookies=Obtain_Cookies(),
                )
        if "id" in response.text:
            subscription_id = response.json()[0]["id"]
            json = {"payment_source_token": None,"gateway_checkout_context": None,"items": [],}
            params = {"location_stack": ["user settings","subscription header","premium subscription cancellation modal",],}
            response = self.client.patch(
                f"https://discord.com/api/v9/users/@me/billing/subscriptions/{subscription_id}",
                headers=headers,
                json=json,
                params=params,
                cookies=Obtain_Cookies(),
            )
        response = self.client.delete(
                f"https://discord.com/api/v9/users/@me/billing/payment-sources/{payment_source}",
                headers=headers,
                cookies=Obtain_Cookies(),
            )
        if response.status_code in (200,204):
            TL.log("INFO","Removed VCC Successfully.",blue)
            return True
        else:
            TL.log("INFO",f"Failed to remove VCC -> {response.json()}",red)
            return False
    def GetPaymentSource(self):
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "priority": "u=1, i",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not;A=Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Asia/Katmandu",
            "x-super-properties": self.xprop,
        }
        response = self.client.get(
            "https://discord.com/api/v9/users/@me/billing/payment-sources",
            headers=headers,
        )
        if "id" in response.text:
            TL.log(
                "PMID",
                f"Scraped payment souce ID -> {blue}{response.json()[0]['id']}",
                blue,
            )
            return response.json()[0]["id"]
        else:
            TL.log("ERRO", f"No payment method found in token, skipping..", red)
            return False

    def RedeemPromotion(self, Payment_Source):
      global success
      try:
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": f"https://discord.com/billing/promotions/{self.promo}",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Europe/Budapest",
            "x-super-properties": self.xprop,
        }
        json = {
            "channel_id": None,
            "payment_source_id": Payment_Source,
            "gateway_checkout_context": None,
        }
        # TL.log("INFO",f"Redeeming promo -> {self.promo} | {Payment_Source}",Fore.BLUE)
        response = self.client.post(
            f"https://discord.com/api/v9/entitlements/gift-codes/{self.promo}/redeem",
            headers=headers,
            json=json,
            cookies=Obtain_Cookies(),
        )
        if '"id"' in response.text:
            TL.log(
                "REDEEMED",
                f"Redeemed Promo In -> {green}{self.token[:23]}.... {white}, {black}time_taken={blue}{str(time.time()-self.start)}",
                Fore.GREEN,
            )
            if parseConfig()["Redeeming"]["RemoveVCC"]:
                self.CardRemover(payment_source=Payment_Source)
            success += 1
            self.Watermark()
            TL.add_content("Output/success.txt", self.full_token)
            if self.sleep_after > 0:
                TL.log(
                    "SLPT",
                    f"Sleeping For -> {blue}{self.SleepAfterXAmountOfRedeemsDelay}s {white}, {black}condition={blue}SleepAfterEachRedeems",
                    blue,
                )
                time.sleep(self.sleep_after)
            else:
                pass
            if (
                self.SleepAfterXAmountOfRedeems > 0
                and success == self.SleepAfterXAmountOfRedeems
            ):
                TL.log(
                    "SLPT",
                    f"Sleeping For -> {blue}{self.SleepAfterXAmountOfRedeemsDelay}s {white}, {black}condition={blue}SleepAfterXAmountOfRedeems",
                    blue,
                )
                time.sleep(self.SleepAfterXAmountOfRedeemsDelay)
            else:
                pass
            return True
        elif "Authentication" in response.text:
            try:
                TL.log(
                    "AUTH",
                    f"Authenticating VCC, Please wait this will take {blue}4-5s",
                    blue,
                )
                pi = response.json()["payment_id"]
                response = self.client.get(
                    f"https://discord.com/api/v9/users/@me/billing/stripe/payment-intents/payments/{pi}",
                    headers=headers,
                    cookies=Obtain_Cookies(),
                )
                full_secret = str(
                    response.json()["stripe_payment_intent_client_secret"]
                )
                secret = str(
                    response.json()["stripe_payment_intent_client_secret"]
                ).split("_secret_")[0]
                headers = {
                    "accept": "application/json",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://js.stripe.com",
                    "referer": "https://js.stripe.com/",
                    "sec-ch-ua": f'"Microsoft Edge";v="{self.chrome}", "Not:A-Brand";v="8", "Chromium";v="{self.chrome}"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "user-agent": self.ua,
                }
                data = {
                    "expected_payment_method_type": "card",
                    "use_stripe_sdk": "true",
                    "key": "pk_live_CUQtlpQUF0vufWpnpUmQvcdi",
                    "client_secret": full_secret,
                }
                response = self.client.post(
                    f"https://api.stripe.com/v1/payment_intents/{secret}/confirm",
                    headers=headers,
                    params=data,
                )
                three_ds_source = response.json()["next_action"]["use_stripe_sdk"][
                    "three_d_secure_2_source"
                ]
                response = self.client.post(
                    "https://api.stripe.com/v1/3ds2/authenticate",
                    headers=headers,
                    data=f"source={three_ds_source}&browser=%7B%22fingerprintAttempted%22%3Afalse%2C%22fingerprintData%22%3Anull%2C%22challengeWindowSize%22%3Anull%2C%22threeDSCompInd%22%3A%22Y%22%2C%22browserJavaEnabled%22%3Afalse%2C%22browserJavascriptEnabled%22%3Atrue%2C%22browserLanguage%22%3A%22en-US%22%2C%22browserColorDepth%22%3A%2224%22%2C%22browserScreenHeight%22%3A%221080%22%2C%22browserScreenWidth%22%3A%221920%22%2C%22browserTZ%22%3A%22-345%22%2C%22browserUserAgent%22%3A%22Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F123.0.0.0+Safari%2F537.36+Edg%2F123.0.0.0%22%7D&one_click_authn_device_support[hosted]=false&one_click_authn_device_support[same_origin_frame]=false&one_click_authn_device_support[spc_eligible]=false&one_click_authn_device_support[webauthn_eligible]=false&one_click_authn_device_support[publickey_credentials_get_allowed]=true&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi",
                )
                TL.log(
                    "3DS2",
                    f"https://api.stripe.com/v1/3ds2/authenticate -> {blue}VCC Authenticated Successfully",
                    blue,
                )
                self.RedeemPromotion(Payment_Source)
            except Exception as e:
                if counter[self.full_token] < self.max_tries:
                    counter[self.full_token] += 1
                    self.RedeemPromotion(
                        promo=self.promo,
                        Payment_Source=Payment_Source,
                        Token=self.token,
                    )
                else:
                    TL.log(
                        "AUTH",
                        f"VCC Auth Error -> {yellow}{self.token[:23]}...",
                        yellow,
                    )
            if (
                "Authentication" in response.text
                and counter[self.full_token] < self.max_tries
            ):
                counter[self.full_token] += 1
                self.RedeemPromotion(
                    promo=self.promo, Payment_Source=Payment_Source, Token=self.promo
                )
        else:

            TL.log("FAILED", f"Failed To Redeem Promo -> {red}{response.json()}", red)
            return False
      except Exception as e:
           TL.log("FAILED",f"Exception occured [{e}]", red)
    def AddVCC(self):
      try:
        if ":" in self.vcc:
            ccn = self.vcc.split(":")[0]
            exp_day = self.vcc.split(":")[1][:2]
            exp_year = self.vcc.split(":")[1][2:]
            cvc = self.vcc.split(":")[2]
        elif "|" in self.vcc:
            ccn, exp_day, exp_year, cvc = self.vcc.split("|")
        else:
            TL.log("FAIL", f"{yellow}Bad VCC Format", yellow)
            return False
        config = parseConfig()
        headers = {
            "authority": "api.stripe.com",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "referer": "https://js.stripe.com/",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.ua,
        }
        redeeming_config = config["Redeeming"]
        data = f"card[number]={ccn}&card[cvc]={cvc}&card[exp_month]={exp_day}&card[exp_year]={exp_year}&guid={uuid.uuid4()}&muid={uuid.uuid4()}&sid={uuid.uuid4()}&payment_user_agent=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85%3B+split-card-element&referrer=https%3A%2F%2Fdiscord.com&time_on_page=415638&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&pasted_fields=number%2Ccvc"
        response = self.client.post(
            "https://api.stripe.com/v1/tokens", headers=headers, data=data
        )
        logging_mode = parseConfig()["TerminalLogging"]["LoggingMode"]
        if '"id"' in response.text:
            vcc_token = response.json()["id"]
            if logging_mode.lower() == "all":
                TL.log("INFO", f"Tokenized -> {blue}{vcc_token}", magenta)
            else:
                pass
        else:
            TL.log(
                "FAIL",
                f"Failed To Tokenize Card ({yellow}Show this to response{white}) -> {red}{self.vcc} {white}| Response: {red}{response.json()}",
                red,
            )
            return False
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Europe/Budapest",
            "x-super-properties": self.xprop,
        }
        response = self.client.post(
            "https://discord.com/api/v9/users/@me/billing/stripe/setup-intents",
            headers=headers,
            cookies=Obtain_Cookies(),
        )
        if '"client_secret"' in response.text:
            client_secret = response.json()["client_secret"]
            separated_secret = client_secret.split("_secret_")[0]
            if logging_mode.lower() == "all":
                TL.log("INFO", f"Client Secret -> {blue}{client_secret}", magenta)
            else:
                pass
        else:
            TL.log(
                "FAIL",
                f"Failed To Scrape Client Secret -> {red}{self.vcc} {white}| {red}{response.json() if not '401' in response.text else 'Invalid Token Provided'}",
                red,
            )
            return False
        redeeming_config = config["Redeeming"]
        billing_config = config["Redeeming"]["BillingINFO"]
        if redeeming_config["BypassCannotRedeemGift"]:
            json = {
                "billing_address": {
                    "name": "Joseph Dbratt",
                    "line_1": "JKNSDFSUJNVONSDNMCKXMPC",
                    "line_2": "",
                    "city": billing_config["City"],
                    "state": billing_config["State"],
                    "postal_code": billing_config["Postal"],
                    "country": billing_config["Country"],
                    "email": "",
                },
            }
        else:
            json = {
                "billing_address": {
                    "name": "Joseph Dbratt",
                    "line_1": billing_config["Address"],
                    "line_2": "",
                    "city": billing_config["City"],
                    "state": billing_config["State"],
                    "postal_code": billing_config["Postal"],
                    "country": billing_config["Country"],
                    "email": "",
                },
            }
        response = self.client.post(
            "https://discord.com/api/v9/users/@me/billing/payment-sources/validate-billing-address",
            headers=headers,
            json=json,
            cookies=Obtain_Cookies(),
        )
        if '"token"' in response.text:
            billing_token = response.json()["token"]
            if logging_mode.lower() == "all":
                TL.log("INFO", f"Billing Token -> {blue}{billing_token}", magenta)
            else:
                pass
        else:
            TL.log(
                "FAIL",
                f"Failed To Scrape Billing Token -> {red}{self.vcc} | {response.json()}",
                red,
            )
            return False
        headers = {
            "authority": "api.stripe.com",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://js.stripe.com",
            "referer": "https://js.stripe.com/",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": self.ua,
        }
        if redeeming_config["BypassCannotRedeemGift"]:
            data = f"payment_method_data[type]=card&payment_method_data[card][token]={vcc_token}&payment_method_data[billing_details][address][line1]=JKNSDFSUJNVONSDNMCKXMPC&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][city]={billing_config['City']}&payment_method_data[billing_details][address][state]={billing_config['State']}&payment_method_data[billing_details][address][postal_code]={billing_config['Postal']}&payment_method_data[billing_details][address][country]={billing_config['Country']}&payment_method_data[billing_details][name]=Joseph Dbratt&payment_method_data[guid]={uuid.uuid4()}&payment_method_data[muid]={uuid.uuid4()}&payment_method_data[sid]={uuid.uuid4()}&payment_method_data[payment_user_agent]=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85&payment_method_data[referrer]=https%3A%2F%2Fdiscord.com&payment_method_data[time_on_page]=707159&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&client_secret={client_secret}"
        else:
           data = f"payment_method_data[type]=card&payment_method_data[card][token]={vcc_token}&payment_method_data[billing_details][address][line1]={billing_config['Address']}&payment_method_data[billing_details][address][line2]=&payment_method_data[billing_details][address][city]={billing_config['City']}&payment_method_data[billing_details][address][state]={billing_config['State']}&payment_method_data[billing_details][address][postal_code]={billing_config['Postal']}&payment_method_data[billing_details][address][country]={billing_config['Country']}&payment_method_data[billing_details][name]=Joseph Dbratt&payment_method_data[guid]={uuid.uuid4()}&payment_method_data[muid]={uuid.uuid4()}&payment_method_data[sid]={uuid.uuid4()}&payment_method_data[payment_user_agent]=stripe.js%2F28b7ba8f85%3B+stripe-js-v3%2F28b7ba8f85&payment_method_data[referrer]=https%3A%2F%2Fdiscord.com&payment_method_data[time_on_page]=707159&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_live_CUQtlpQUF0vufWpnpUmQvcdi&client_secret={client_secret}"
        response = self.client.post(
            f"https://api.stripe.com/v1/setup_intents/{separated_secret}/confirm",
            headers=headers,
            data=data,
        )
        if response.status_code == 200:
            pmtok = response.json()["payment_method"]
            if logging_mode.lower() == "all":
                TL.log("INFO", f"Payment Method -> {blue}{pmtok}", magenta)
            else:
                pass
        else:
            TL.log(
                "FAIL",
                f"Failed To Payment Method -> {red}{self.vcc} {white}| {red}{response.json()}",
                red,
            )
            return False
        headers = {
            "authority": "discord.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": self.token,
            "content-type": "application/json",
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": f'"Chromium";v="{self.chrome}", "Not(A:Brand";v="24", "Microsoft Edge";v="{self.chrome}"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": self.ua,
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "en-US",
            "x-discord-timezone": "Europe/Budapest",
            "x-super-properties": self.xprop,
        }
        if redeeming_config["BypassCannotRedeemGift"]:
            json = {
            "payment_gateway": 1,
            "token": pmtok,
            "billing_address": {
                "name": "Joseph Dbratt",
                "line_1": "JKNSDFSUJNVONSDNMCKXMPC",
                "line_2": None,
                "city": billing_config["City"],
                "state": billing_config["State"],
                "postal_code": billing_config["Postal"],
                "country": billing_config["Country"],
                "email": "",
            },
            "billing_address_token": billing_token,
        }
        else:
          json = {
            "payment_gateway": 1,
            "token": pmtok,
            "billing_address": {
                "name": "Joseph Dbratt",
                "line_1": billing_config["Address"],
                "line_2": None,
                "city": billing_config["City"],
                "state": billing_config["State"],
                "postal_code": billing_config["Postal"],
                "country": billing_config["Country"],
                "email": "",
            },
            "billing_address_token": billing_token,
        }
        response = self.client.post(
            "https://discord.com/api/v9/users/@me/billing/payment-sources",
            headers=headers,
            json=json,
            cookies=Obtain_Cookies(),
        )
        if '"id"' in response.text:
            TL.remove_content("Input/vccs.txt", self.vcc)
            TL.log(
                "INFO",
                f"Added VCC -> {blue}{self.token[:23]} {white}, {black}time_taken={blue}{str(time.time()-self.start)}",
                blue,
            )
            return response.json()["id"]
        else:
            TL.log(
                "FAIL",
                f"Failed to add card -> {red}{response.json() if not 'captcha' in response.text else 'Captcha Encountered'} {response.json()}",
                red,
            )
            return False
      except Exception as e:
          TL.log("FAILED",f"Exception occured [{e}]", red)
