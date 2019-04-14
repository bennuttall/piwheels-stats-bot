from logzero import logger, logfile
from db import PiWheelsDatabase

logfile('/var/log/piwheels-twitter/daily.log', maxBytes=1e6)
logger.info('START')

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

db = PiWheelsDatabase()

downloads = db.count_downloads_yesterday()
logger.debug('downloads: {}'.format(downloads))
time_saved = db.get_time_saved_yesterday()
logger.debug('time saved: {}'.format(time_saved))

tweet = ('Yesterday, {:,} packages were downloaded from piwheels.org, '
         'saving users over {} days of build time').format(downloads,
                                                           time_saved.days)

try:
    logger.info('Tweeting: {}'.format(tweet))
    #twitter.update_status(status=tweet)
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
