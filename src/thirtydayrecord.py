from logzero import logger, logfile
from db import PiWheelsDatabase
import math

logfile('/var/log/piwheels-twitter/thirtydayrecord.log', maxBytes=1e6)
logger.info('START')

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

db = PiWheelsDatabase()

def get_last_milestone():
    with open('/home/piwheels/downloads30.txt', 'r') as f:
        return int(f.readline())

def update_downloads_last_count(downloads):
    with open('/home/piwheels/downloads30.txt', 'w') as f:
        f.write('{}'.format(downloads))

def roundup(n):
    hund_thou = 1e5
    return int(math.ceil(n / hund_thou) * hund_thou)

last_milestone = get_last_milestone()
logger.debug('last milestone: {}'.format(last_milestone))
next_milestone = roundup(last_milestone + 1)
logger.debug('next milestone: {}'.format(next_milestone))
downloads_now = db.get_downloads_last_30_days()
logger.debug('downloads now: {}'.format(downloads_now))

if downloads_now >= next_milestone:
    tweet = 'Now passed {:,} downloads in 30 days from piwheels.org'.format(next_milestone)
    logger.info('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)
    update_downloads_last_count(next_milestone)
else:
    logger.info('Not tweeting: {:,} < {:,}'.format(downloads_now, next_milestone))

