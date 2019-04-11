from twitter import twitter
from db import PiWheelsDatabase
from math import floor

db = PiWheelsDatabase()

downloads = db.count_downloads_last_month()
time_saved = db.get_time_saved_last_month()
years = floor(float(str(time_saved).split(' ')[0]) // 365)
tweet = ('Last month, {:,} packages were downloaded from piwheels.org, '
         'saving users over {:,} years of build time').format(downloads, years)

if downloads and time_saved:
    print(f'Tweeting: {tweet}')
    twitter.update_status(status=tweet)
else:
    print(f'Not tweeting: {tweet}')
