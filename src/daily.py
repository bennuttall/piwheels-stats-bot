import io
import statistics

from logzero import logger, logfile
import matplotlib.pyplot as plt

from db import PiWheelsDatabase


logfile('/var/log/piwheels-twitter/daily.log', maxBytes=1e6)

db = PiWheelsDatabase()


def get_record(record_file):
    with open(record_file) as f:
        return int(f.read().strip())

def update_record(record_file, data):
    with open(record_file, 'w') as f:
        f.write(str(data))

def make_week_downloads_graph():
    logger.info('Making graph')
    downloads_last_week = db.get_downloads_in_last_week()
    days = [d[0] for d in downloads_last_week]
    downloads = [d[1] for d in downloads_last_week]

    fig, ax = plt.subplots()
    plt.bar(range(7), downloads)
    plt.title('Downloads in the last 7 days')
    plt.xticks(range(7), days)
    week_avg = statistics.mean(downloads)
    ax.plot([0, 6], [record_downloads, record_downloads], "r--", label="Record")
    ax.plot([0, 6], [week_avg, week_avg], "k--", label="Daily average")
    ax.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

def send_tweet(tweet, graph):
    logger.info('Uploading graph')
    response = twitter.upload_media(media=graph)
    media_ids = [response['media_id']]

    logger.info('Tweeting: {}'.format(tweet))
    try:
        twitter.update_status(status=tweet, media_ids=media_ids)
    except Exception as e:
        logger.error('{}: {}'.format(e.__class__.__name__, e))


try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

record_downloads_file = '/home/piwheels/daily_downloads_record.txt'
record_downloads = get_record(record_downloads_file)
record_time_saved_file = '/home/piwheels/daily_time_saved_record.txt'
record_time_saved = get_record(record_time_saved_file)

logger.info('START')

downloads = db.count_downloads_yesterday()
logger.debug('downloads: {}'.format(downloads))
time_saved = db.get_time_saved_yesterday()
logger.debug('time saved: {}'.format(time_saved))

downloads_record = ''
if downloads > record_downloads:
    downloads_record = ' (a new daily record)'
    update_record(record_downloads_file, downloads)

time_saved_record = ''
if time_saved > record_time_saved:
    time_saved_record = ' (a new daily record)'
    update_record(record_time_saved_file, time_saved)

tweet = ('Yesterday, {:,} packages were downloaded from piwheels.org{}, '
         'saving users over {} days{} of build time').format(
         downloads, downloads_record, time_saved, time_saved_record)

graph = make_week_downloads_graph()
send_tweet(tweet, graph)
