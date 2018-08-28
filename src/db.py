import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime, timedelta

class PiWheelsDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(
            'dbname=piwheels',
            cursor_factory=DictCursor
        )

    def get_downloads_in_last_day(self):
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
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
