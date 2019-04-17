from twython import Twython
from auth import *
import sys

class MockTwython:
    def update_status(self, *args, **kwargs):
        pass

if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    print("DEBUG MODE")
    twitter = MockTwython()
else:
    twitter = Twython(CON_KEY, CON_SEC, ACC_TOK, ACC_SEC)
