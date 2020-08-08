import io
import statistics

from logzero import logger, logfile
import matplotlib.pyplot as plt

from db import PiWheelsDatabase, get_last_month_period


plt.rcParams["figure.figsize"] = (10, 6)

logfile('/var/log/piwheels-twitter/monthly.log', maxBytes=1e6)

db = PiWheelsDatabase()

try:
    from twitter import twitter
except Exception as e:
    logger.error('{}: {}'.format(e.__class__.__name__, e))
    exit()

def make_month_downloads_graph():
    logger.info('Making graph')
    downloads_last_month = db.get_downloads_in_last_month()
    days = [d[0] for d in downloads_last_month]
    downloads = [d[1] for d in downloads_last_month]

    fig, ax = plt.subplots()
    plt.bar(range(len(days)), downloads)
    plt.title('Downloads in {}'.format(month))
    plt.xticks(range(len(days)), days)
    month_avg = statistics.mean(downloads)
    ax.plot(range(len(days)), [month_avg]*len(days), "k--", label="Daily average")
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


logger.info('START')

prev_first, prev_end = get_last_month_period()
month = prev_first.strftime('%B')
downloads = db.count_downloads_last_month()
logger.debug('downloads: {}'.format(downloads))
time_saved = db.get_time_saved_last_month()
logger.debug('time saved: {}'.format(time_saved))
time = ' '.join(time_saved.split()[:2])

tweet = ('Last month, {:,} packages were downloaded from piwheels.org, '
         'saving users over {} of build time').format(downloads, time)

graph = make_month_downloads_graph()
send_tweet(tweet, graph)
