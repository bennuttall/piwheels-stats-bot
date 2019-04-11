import psycopg2
from psycopg2.extras import DictCursor
from datetime import date, datetime, timedelta

def get_last_month_period():
    this_first = date(now.year, now.month, 1)
    prev_end = this_first - timedelta(days=1)
    prev_first = date(prev_end.year, prev_end.month, 1)
    return prev_first, prev_end

now = datetime.now()
yesterday = (now - timedelta(1)).strftime('%Y-%m-%d')
first_of_last_month, end_of_last_month = get_last_month_period()

class PiWheelsDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            'dbname=piwheels',
            cursor_factory=DictCursor
        )

    def count_downloads_yesterday(self):
        query = """
        SELECT
            COUNT(*)
        FROM
            downloads
        WHERE
            accessed_at::date = date %s
        """
        values = (yesterday, )
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]

    def count_downloads_last_month(self):
        query = """
        SELECT
            COUNT(*)
        FROM
            downloads
        WHERE
            accessed_at::date BETWEEN date %s AND date %s
        """
        values = (first_of_last_month, end_of_last_month)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]

	def get_time_saved_yesterday(self):
        query = """
                SELECT SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE WHEN b.duration > INTERVAL '6.7 seconds'
                THEN b.duration - INTERVAL '6.7 seconds'
                ELSE INTERVAL '0'
            END
        ) AS time_saved
                FROM
                        downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
                WHERE f.abi_tag <> 'none'
                AND accessed_at::date = date %s;
        """
        values = (yesterday, )
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]

	def get_time_saved_last_month(self):
        query = """
                SELECT SUM(
            CASE f.platform_tag
                WHEN 'linux_armv7l' THEN 1
                WHEN 'linux_armv6l' THEN 6
                ELSE 0
            END *
            CASE WHEN b.duration > INTERVAL '6.7 seconds'
                THEN b.duration - INTERVAL '6.7 seconds'
                ELSE INTERVAL '0'
            END
        ) AS time_saved
                FROM
                        downloads d
        JOIN files f ON d.filename = f.filename
        JOIN builds b ON b.build_id = f.build_id
                WHERE f.abi_tag <> 'none'
                AND accessed_at::date BETWEEN date %s AND date %s
        """
        values = (first_of_last_month, end_of_last_month)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, values)
                return cur.fetchone()[0]
