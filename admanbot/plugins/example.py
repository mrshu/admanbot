"""
Examples of brutal plugins. Primarily used for testing.
"""

from readability.readability import Document
import re
import requests

import time
from brutal.core.plugin import BotPlugin, cmd, event, match, threaded



@cmd
def ping(event):
    return 'pong, got {0!r}'.format(event)


@cmd
def testargs(event):
    return 'you passed in args: {0!r}'.format(event.args)


#@event(thread=True)
def sleepevent(event):
    time.sleep(7)
    return 'SOOOOOO sleepy'


@cmd(thread=True)
def sleep(event):
    time.sleep(5)
    return 'im sleepy...'


#@event
def test_event_parser(event):
    return 'EVENT!!! {0!r}'.format(event)

# @match(regex=r'^hi$')
# def matcher(event):
#    return 'Hello to you!'


@match(regex=r'(?:.*\s+|)((https?:\/\/)?([a-z0-9\.-]+)\.([a-z\.]{2,6})(/\w\.-]*)*([/a-z0-9\.-_%]+)?)(?:.*\s+|)')
def url_matcher(event, url, *args):
    if (not url.startswith("http://") and not url.startswith("https://")):
        url = "http://" + url

    try:
        r = requests.get(url)
    except:
        event.log.debug("Couldn't open url " + str(url.encode("utf-8")))
        return

    readable_article = Document(r.text).summary() 
    readable_title = Document(r.text).short_title()

    tit = re.sub('<[^>]*>', '', readable_title)
    art = re.sub('<[^>]*>', '', readable_article)
    art = re.sub('\s\s+', '', art).replace("&#13;", " ").replace("\n", " ")
        
    return "> " + str(tit.encode("utf-8")) + " > " + str(art.encode("utf-8"))[:100] + "..." 


class TestPlugin(BotPlugin):
    def setup(self, *args, **kwargs):
        self.log.debug('SETUP CALLED')
        self.counter = 0
        #self.loop_task(5, self.test_loop, now=False)
        #self.delay_task(10, self.future_task)

    def future_task(self):
        self.log.info('testing future task')
        return 'future!'

    @threaded
    def test_loop(self):
        self.log.info('testing looping task')
        return 'loop!'

    def say_hi(self, event=None):
        self.msg('from say_hi: {0!r}'.format(event), event=event)
        return 'hi'

    @threaded
    def say_delayed_hi(self, event=None):
        self.msg('from say_hi_threaded, sleeping for 5: {0!r}'.format(event), event=event)
        time.sleep(5)
        return 'even more delayed hi'

    @cmd
    def runlater(self, event):
        self.delay_task(5, self.say_hi, event=event)
        self.delay_task(5, self.say_delayed_hi, event=event)
        return 'will say hi in 5 seconds'

    @cmd
    def count(self, event):
        self.counter += 1
        return 'count {1!r} from class! got {0!r}'.format(event, self.counter)

    @cmd(thread=True)
    def inlinemsg(self, event):
        self.msg('sleeping for 5 seconds!', event=event)
        time.sleep(5)
        return 'done sleeping!'
