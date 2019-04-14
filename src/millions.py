from logzero import logger, logfile
from db import PiWheelsDatabase
import math

logfile('/var/log/piwheels-twitter/millions.log', maxBytes=1e6)
logger.info('START')

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

db = PiWheelsDatabase()

def get_downloads_last_count():
    with open('/home/piwheels/downloads.txt', 'r') as f:
        return int(f.readline())

def update_downloads_last_count(downloads):
    with open('/home/piwheels/downloads.txt', 'w') as f:
        f.write('{}'.format(downloads))

def roundup(n):
    million = 10**6
    return int(math.ceil(n / million)) * million

downloads_last_count = get_downloads_last_count()
logger.debug('last count: {}'.format(downloads_last_count))
next_milestone = roundup(downloads_last_count)
logger.debug('next milestone: {}'.format(next_milestone))
downloads_now = db.get_downloads_count()
logger.debug('downloads now: {}'.format(downloads_now))

if downloads_now >= next_milestone:
    tweet = 'Now passed {:,} downloads from piwheels.org'.format(next_milestone)
    logger.info('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)
else:
    logger.info('Not tweeting: {:,} < {:,}'.format(downloads_now, next_milestone))

update_downloads_last_count(downloads_now)
