from logzero import logger, logfile
from db import PiWheelsDatabase

logfile('/var/log/piwheels-twitter/years_saved.log', maxBytes=1e6)
logger.info('START')

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

db = PiWheelsDatabase()

def get_years_saved():
    with open('/home/piwheels/time_saved.txt', 'r') as f:
        return int(f.readline())

def update_years_saved(time_saved):
    with open('/home/piwheels/time_saved.txt', 'w') as f:
        f.write('{}'.format(time_saved))

def roundup(n):
    years = 5
    return ((n // years) + 1) * years


years_saved_prev = get_years_saved()
logger.debug('years saved prev: {}'.format(years_saved_prev))
next_milestone = roundup(years_saved_prev)
logger.debug('next milestone: {}'.format(next_milestone))
time_saved_now = db.get_total_time_saved()
logger.debug('time saved now: {}'.format(time_saved_now))
years_saved = int(time_saved_now.split()[0])

if years_saved >= next_milestone:
    tweet = 'piwheels.org has now saved over {} years of build time'.format(next_milestone)
    logger.info('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)
else:
    logger.info('Not tweeting: {:,} < {:,}'.format(years_saved, next_milestone))

update_years_saved(years_saved)
