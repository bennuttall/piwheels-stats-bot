from twython import Twython
import os
from db import PiWheelsDatabase

twitter = Twython(
    os.environ['TWITTER_CON_KEY'],
    os.environ['TWITTER_CON_SEC'],
    os.environ['TWITTER_ACC_TOK'],
    os.environ['TWITTER_ACC_SEC']
)

db = PiWheelsDatabase()
downloads = db.get_downloads_in_last_day()
tweet = 'Yesterday, {:,} packages were downloaded from piwheels.org'.format(downloads)

print(tweet)
twitter.update_status(status=tweet)
