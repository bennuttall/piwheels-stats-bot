from twitter import twitter
from db import PiWheelsDatabase
import math

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
next_milestone = roundup(downloads_last_count)
downloads_now = db.get_downloads_count()

if downloads_now >= next_milestone:
    tweet = 'Now passed {:,} downloads from piwheels.org'.format(next_milestone)
    print('Tweeting: {}'.format(tweet))
    twitter.update_status(status=tweet)

update_downloads_last_count(downloads_now)
