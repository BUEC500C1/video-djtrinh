import threading
import time
import requests
import queue
import twitter_api as twit
import subprocess
import datetime
import textwrap
import glob
import os
import os.path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def processor(q):
    while (True):
        item = q.get()
        if item is not None:
            create_images(item[0], item[1], item[2], item[3])
        q.task_done()
        time.sleep(.001)


def ffpmeg_processor(q2):
    while (True):
        username = q2.get()
        if username is not None:
            png_count = len(glob.glob1(r"processed_imgs/", username + r"*.png"))
            if (png_count < 20):
                q2.put(username)
            else:
                ffmpeg_call(username)
        time.sleep(.001)
        q2.task_done()


def producer(q, q_item):
    # the main thread will put new items to the queue
    for count, tweet in enumerate(q_item[2]):
        q.put([q_item[0], q_item[1], tweet, count])
    q.join()


def create_images(user_id, user_img_url, tweet, count):
    try:
        txt = tweet.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        try:
            txt = tweet.full_text
        except AttributeError:
            return

    font = ImageFont.truetype(r'font/Arial.ttf', 14)
    background = Image.new('RGBA', (1024, 768), (255, 255, 255, 255))
    response = requests.get(user_img_url)
    img = Image.open(BytesIO(response.content))
    draw = ImageDraw.Draw(background)
    lines = textwrap.wrap(txt, width=120)
    x, y = 50, 225
    for line in lines:
        width, height = font.getsize(line)
        draw.text(((x), y), line, font=font, fill="black")
        y += 15
    draw.text((120, 170), user_id, font=font, fill="black")
    offset = (50, 150)
    img_list = []
    try:
        if 'media' in tweet.entities:
            for medium in tweet.entities['media']:
                img_list.append(medium['media_url'])
        if len(img_list) != 0:
            response = requests.get(img_list[0])
            img = Image.open(BytesIO(response.content))
            # background.paste(img, (100, y))
    except Exception as e:
        print(e)
    background.paste(img, offset)
    background.save('./processed_imgs/'+str(user_id)+str(count)+'.png')


def ffmpeg_call(username):
    today = str(datetime.date.today()).replace('-', '_')
    try:
        subprocess.call(['./ffmpeg/bin/ffmpeg', '-y', '-r', '1/3', '-i', './processed_imgs/'+username+'%d.png',
                       '-pix_fmt', 'yuv420p', '-r', '25', '-loglevel', 'error', '-hide_banner',
                       'twitter_feed_' + username + '_' + today + '.mp4'], stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        print("Done with " + username + " video!")
        print("Twitter id? ", end='')
    except FileNotFoundError:
        return -1


def cli(q, q2):
    while(True):
        id = input("Twitter id? ")
        # Remove old pictures with matching Twitter ID
        filelist = glob.glob(os.path.join(r'processed_imgs/', id + "*.png"))
        for f in filelist:
            try:
                os.remove(f)
            except Exception as e:
                print(e)
        # Create processes to start generating pictures
        q_item = [id, twit.get_user_pic(id), twit.get_users_tweets(id)]
        t = threading.Thread(name="ProducerThread", target=producer, args=(q, q_item))
        q2.put(id)
        t.start()


if __name__ == '__main__':
    # create queue
    q = queue.Queue(maxsize=4)
    q2 = queue.Queue()

    # grab keys
    twit = twit.twitter_scrapper("keys")

    # 4 threads to do processes running at .001 seconds
    threads_num = 4
    for i in range(threads_num):
        t = threading.Thread(name="Thread Processor-" + str(i), target=processor, args=(q,))
        t.start()

    # FFMPEG thread
    t = threading.Thread(name="FFPMPEG Processor", target=ffpmeg_processor, args=(q2,))
    t.start()

    # CLI thread
    t = threading.Thread(name="CLI", target=cli, args=(q, q2,))
    t.start()
