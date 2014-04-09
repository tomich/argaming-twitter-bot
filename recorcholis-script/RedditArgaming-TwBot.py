
# RedditArgentina-TwBot 0.03 by /u/recorcholis adaptado a Argaming
 
import sqlite3
import praw
import time
from twitter import *

OAUTH_TOKEN = 'abc123'
OAUTH_SECRET = 'abc123'
CONSUMER_KEY = 'abc123'
CONSUMER_SECRET = 'abc123'

wait_time = 300
 
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "Bot awake, Tw Auth"
 
t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,CONSUMER_KEY, CONSUMER_SECRET))
 
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "DB Conn"
 
conn = sqlite3.connect('ArgamingTwitter.db')
c = conn.cursor()
 
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "Reddit Init"
 
r = praw.Reddit(user_agent='RedditArgaming-TwBot')
 
while True:
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "arggit check"
 
    submissions = r.get_subreddit('argaming').get_new(limit=50)
 
    new_post = False
 
    for submission in submissions:
        if submission.ups - submission.downs < 2:
            continue
 
        c.execute("SELECT COUNT(*) FROM submission WHERE id = '" + submission.id + "'")
        row = c.fetchone()
 
        if row[0] == 0:
            new_post = True
 
            if len(submission.title) < 110:
                twstatus = submission.title
            else:
                twstatus = submission.title[:110] + "(...)"
 
            twstatus += " " + submission.short_link
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "Tweeting ->", twstatus.encode('utf-8')
            try:
                t.statuses.update(status=twstatus)
            except TwitterHTTPError as twex:
                print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), twex
 
            c.execute("INSERT INTO submission (id, short_link, title) VALUES ('" + submission.id
                + "', '" + submission.short_link + "', '" + submission.title.replace("'", "''") + "')")
            conn.commit()
 
            break
 
    if not new_post:
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "Nothing but the sun"
 
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), "Esperando " + str(wait_time) + " segundos"
    time.sleep(wait_time)