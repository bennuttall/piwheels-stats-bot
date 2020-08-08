import psycopg2
from psycopg2.extras import DictCursor
from datetime import date, datetime, timedelta

interval_type = psycopg2.extensions.new_type(psycopg2.extensions.INTERVAL.values,
                                             'INTERVAL_STR', psycopg2.STRING)

def get_last_month_period():
    this_first = date(now.year, now.month, 1)
    prev_end = this_first - timedelta(days=1)
    prev_first = date(prev_end.year, prev_end.month, 1)
    return (prev_first, prev_end)

now = datetime.now()
yesterday_dt = now - timedelta(days=1)
yesterday = yesterday_dt.strftime('%Y-%m-%d')
first_of_last_month, end_of_last_month = get_last_month_period()

class PiWheelsDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            'dbname=piwheels',
            cursor_factory=DictCursor
        )

    def count_downloads_yesterday(self):
        query = """
        SELECT COUNT(*)
        FROM downloads
        WHERE accessed_at::date = date %s
        """
        values = (yesterday, )
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]

    def count_downloads_last_month(self):
        query = """
        SELECT COUNT(*)
        FROM downloads
        WHERE accessed_at::date BETWEEN date %s AND date %s
        """
        values = (first_of_last_month, end_of_last_month)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]

    def get_time_saved_yesterday(self):
        query = """
        SELECT JUSTIFY_INTERVAL(SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE WHEN b.duration > INTERVAL '6.7 seconds'
                THEN b.duration - INTERVAL '6.7 seconds'
                ELSE INTERVAL '0'
            END
        )) AS time_saved
        FROM downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
        WHERE f.abi_tag <> 'none'
        AND accessed_at::date = date %s;
        """
        values = (yesterday, )
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0].days

    def get_time_saved_last_month(self):
        query = """
        SELECT JUSTIFY_INTERVAL(SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE WHEN b.duration > INTERVAL '6.7 seconds'
                THEN b.duration - INTERVAL '6.7 seconds'
                ELSE INTERVAL '0'
            END
        )) AS time_saved
        FROM downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
        WHERE f.abi_tag <> 'none'
        AND accessed_at::date BETWEEN date %s AND date %s
        """
        values = (first_of_last_month, end_of_last_month)
        with self.conn:
            with self.conn.cursor() as cur:
                psycopg2.extensions.register_type(interval_type, cur)
                cur.execute(query, values)
                return cur.fetchone()[0]

    def get_downloads_count(self):
        query = """
        SELECT COUNT(*)
        FROM downloads
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()[0]

    def get_downloads_last_30_days(self):
        query = """
        SELECT downloads_last_month
        FROM get_statistics()
        """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchone()[0]

    def get_total_time_saved(self):
        query = """
        SELECT JUSTIFY_INTERVAL(SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE
                WHEN b.duration > INTERVAL '1 week' THEN INTERVAL '0'
                WHEN b.duration > INTERVAL '6.7 seconds' THEN b.duration - INTERVAL '6.7 seconds'
            ELSE INTERVAL '0'
            END
        )) AS time_saved
        FROM downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
        WHERE f.abi_tag <> 'none';
        """
        with self.conn:
            with self.conn.cursor() as cur:
                psycopg2.extensions.register_type(interval_type, cur)
                cur.execute(query)
                return cur.fetchone()[0]

    def get_time_saved_in_year(self, year):
        query = """
        SELECT JUSTIFY_INTERVAL(SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE
                WHEN b.duration > INTERVAL '1 week' THEN INTERVAL '0'
                WHEN b.duration > INTERVAL '6.7 seconds' THEN b.duration - INTERVAL '6.7 seconds'
            ELSE INTERVAL '0'
            END
        )) AS time_saved
        FROM downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
        WHERE f.abi_tag <> 'none'
        AND d.accessed_at::date > '%s-12-31'
        """
        with self.conn:
            with self.conn.cursor() as cur:
                psycopg2.extensions.register_type(interval_type, cur)
                cur.execute(query, (year - 1,))
                return cur.fetchone()[0]

    def get_downloads_in_last_week(self):
        query = """
        SELECT accessed_at::date AS day, COUNT(*) AS downloads
        FROM downloads
        WHERE accessed_at::date BETWEEN %s AND %s
        GROUP BY day
        ORDER BY day
        """
        day_1 = (yesterday_dt - timedelta(days=6)).strftime('%Y-%m-%d')
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, (day_1, yesterday))
                results = cur.fetchall()
        return [
            (day.strftime('%a'), num)
            for day, num in results
        ]
