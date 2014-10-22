from brutal.core.plugin import match, threaded
import datetime
import re
import requests
from lxml import html

@threaded
@match(regex=r'(?:.*\s+|)bus\sz\s([A-Za-z\s]+)\sdo\s([A-Za-z\s]+)(?:.*\s+|)')
def traffic(event, departure, arrival, *args):
    msg = vars(event)['meta']['body']

    now = datetime.datetime.now()
    if ('zajtra' in msg):
        date = str((datetime.date.today() + datetime.timedelta(days=1)).strftime("%d.%m.%Y"))
    elif ('pozajtra' in msg):
        date = str((datetime.date.today() + datetime.timedelta(days=2)).strftime("%d.%m.%Y"))
    else:
        date = str(now.strftime("%d.%m.%Y"))

    time = datetime.datetime.now().time().strftime("%H:%M")
    if (re.search("(o\s[0-9]+:[0-9+])", msg)):
        time = re.match("[0-9]+:[0-9]+", msg)

    vehicle = "vlakbus"
    if 'vlak' in msg:
        vehicle = 'vlak'
    elif 'bus' in msg:
        vehicle = 'bus'

    url = "http://cp.atlas.sk/" + vehicle + "/spojenie/"
    try:
        r = requests.get(url, timeout=5, params={'date': date, 'time': time, 
                                                 'f':departure, 't':arrival,
                                                 'fc': '1', 'tc': 1, 'submit:': 'true'})
    except requests.exceptions.Timeout:
        event.log.debug("Server is not responding")
        if vars(event)['meta']['nick'] is not '':
            return vars(event)['meta']['nick'] + ": cp.sk not responding"
    
    tree = html.fromstring(r.text)
    #print tree.xpath('//div[@id="main-res-inner"]/table')
    print r.text
    return "there will be something"
    # return departure + " > " + arrival + " " + date
