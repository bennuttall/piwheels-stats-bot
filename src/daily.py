from logzero import logger, logfile
from db import PiWheelsDatabase

logfile('/var/log/piwheels-twitter/daily.log', maxBytes=1e6)
logger.info('START')
record_file = '/home/piwheels/daily_record.txt'

def update_record(downloads):
    with open(record_file, 'w') as f:
        f.write(str(downloads))

def get_record():
    with open(record_file) as f:
        return int(f.read().strip())

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
record = get_record()

if downloads > record:
    downloads_record = ' (a new daily record)'
    update_record(downloads)
else:
    downloads_record = ''

time_saved_record = ''

tweet = ('Yesterday, {:,} packages were downloaded from piwheels.org{}, '
         'saving users over {} days of build time').format(downloads,
                                                           downloads_record,
                                                           time_saved.days,
                                                           time_saved_record)
try:
    logger.info('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
