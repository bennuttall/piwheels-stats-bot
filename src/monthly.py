from logzero import logger, logfile
from db import PiWheelsDatabase

logfile('/var/log/piwheels-twitter/monthly.log', maxBytes=1e6)
logger.info('START')

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

db = PiWheelsDatabase()

downloads = db.count_downloads_last_month()
logger.debug('downloads: {}'.format(downloads))
time_saved = db.get_time_saved_last_month()
logger.debug('time saved: {}'.format(time_saved))
time = ' '.join(time_saved.split()[:2])

tweet = ('Last month, {:,} packages were downloaded from piwheels.org, '
         'saving users over {} of build time').format(downloads, time)

try:
    logger.info('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
