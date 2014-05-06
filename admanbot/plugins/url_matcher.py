import re
import requests
from readability.readability import Document

from brutal.core.plugin import BotPlugin, cmd, event, match, threaded


@threaded
@match(regex=r'(?:.*\s+|)((https?:\/\/)?([a-z0-9\.-]+)\.([a-z\.]{2,6})(/\w\.-]*)*([/a-z0-9\.-_%]+)?)(?:.*\s+|)')
def url_matcher(event, url, *args):
    if (not url.startswith("http://") and not url.startswith("https://")):
        url = "http://" + url
    
    try:
        r = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        event.log.debug("Server is not responding: " + str(url.encode("utf-8")))
        if vars(event)['meta']['nick'] is not '':
            return vars(event)['meta']['nick'] + ": server is not responding"
        return
    except:
        event.log.debug("Couldn't open url " + str(url.encode("utf-8")))
        if vars(event)['meta']['nick'] is not '':
            return vars(event)['meta']['nick'] + ": could not open url"
        return

    readable_article = Document(r.text).summary()
    readable_title = Document(r.text).short_title()

    tit = re.sub('<[^>]*>', '', readable_title)
    art = re.sub('<[^>]*>', '', readable_article)
    art = re.sub('\s\s+', '', art).replace("&#13;", " ").replace("\n", " ")

    return "> " + str(tit.encode("utf-8")) + " > " + str(art.encode("utf-8"))[:100] + "..."
