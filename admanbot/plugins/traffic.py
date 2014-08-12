from brutal.core.plugin import match, threaded
import datetime


@threaded
@match(regex=r'(?:.*\s+|)bus\sz\s[A-Za-z]+\sdo[A-Za-z]+(?:.*\s+|)')
def traffic(event, url, *args):
    now = datetime.datetime.now()

    date = str(now.strftime("%d.%m.%Y"))

    return "asking for a bus?"
