import random
import json
import subprocess
import time
from CAT.driver import get_driver
import catdriverandroid

famille = [
    "Olivier",
    "Laure",
    # "Sophie", "Maxime", "Marie-Odile", "Mike"
]
last = {
    "Olivier": "Maxime",
    "Laure": "Marie-Odile",
    "Sophie": "Laure",
    "Maxime": "Olivier",
    "Marie-Odile": "Mike",
    "Mike": "Sophie"
    }

contact = {
    "Olivier": "068-",
    "Laure": "06-",
    # "Sophie": "06-",
    # "Maxime": "06-‬",
    # "Marie-Odile": "06-",
    # "Mike": "06-"
    }
message = {
    "Mike": "He ben bon courage, les dieux de la chaussette t'ont confié Mike 😅"
}

default_message = "Pas de bol t'as chopper {} 💩"

picks = {}


def random_pick(l):
    # print(f"Picking from {l}")
    if len(l) == 0:
        raise Exception("Empty list, NEED TO BE RE-RUN")
    if len(l) == 1:
        return l[0]
    # print(f"{len(l)}", flush=True)
    return l[random.randint(0, len(l)-1)]

phone = get_driver('android-device')(config={"adb_id": "01d9613e733a3d64"})  # type: catdriverandroid.device.AndroidDriver

def send_sms(recipient, message):
    phone.close_app("com.google.android.apps.messaging")
    print(f"Sending message to {recipient} [{contact[recipient]}] with message : {message}")
    phone.adb.cmd(f"shell am start -n com.google.android.apps.messaging/com.google.android.apps.messaging.ui."
                            "conversation.LaunchConversationActivity -a android.intent.action.SENDTO "
                            f"-d sms:\"{contact[recipient]}\" --es\
                              sms_body \"{message}\"", ignore_stderr=True)
    time.sleep(5)

    phone.screen.find_text("Send SMS").click()

cible = famille.copy()
rf = random.sample(famille, len(famille))
for m in rf:
    print(f"Choosing chaussette for {m}")
    cf = cible.copy()
    if m in cf:
        cf.remove(m)
    pick = random_pick(cf)
    while last[m] == pick:
        if len(cf) == 1:
            raise Exception("NEED TO BE RE-RUN")
        pick = random_pick(cf)
    cible.remove(pick)

    picks[m] = pick

    print(f"Secret chaussette {m} -> {pick}", flush=True)


print(json.dumps(picks, indent=4))

for k,v in picks.items():
    send_sms(k, message.get(v, default_message.format(v)))

phone.update()