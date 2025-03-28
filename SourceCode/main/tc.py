import tls_client
from SourceCode.Modules.logger import *
import tls_client


def check_token(token: str) -> bool:
    global valid, invalid
    ft = token
    token = ft.split(":")[2] if "@" in ft else ft
    url = "https://discord.com/api/v9/users/@me"
    session = tls_client.Session(
        client_identifier="chorme_126", random_tls_extension_order=True
    )
    headers = {
        "Authorization": token,
    }
    r = session.get(url, headers=headers)
    if r.status_code == 200:
        TL.log("VALID", f"Valid -> {green}{token[:23]}....", Fore.GREEN)
        valid += 1
    else:
        TL.log("INVALID", f"Invalid -> {red}{token[:23]}....", Fore.RED)
        TL.remove_content("Input/tokens.txt", ft)
        invalid += 1
