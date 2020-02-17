import threading
import time
import requests
import queue
import twitter_api as twit
import subprocess
import datetime
import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def processor(q, completion_queue):
    while (True):
        name = threading.currentThread().getName()
        print("Thread: {0} start get item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                            time.strftime('%H:%M:%S')))
        item = q.get()
        time.sleep(.001)
        create_images(item[0], item[1], item[2], item[3])
        print("The item is %s" % item[3])
        print("Thread: {0} finish process item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                                 time.strftime(

                                                                                                     '%H:%M:%S')))
        completion_queue.put(1)
        if completion_queue.qsize() == 20:
            ffmpeg_call()
            while(completion_queue.qsize() != 0):
                completion_queue.get()
        q.task_done()


def producer(q, q_item):
    # the main thread will put new items to the queue
    for count, tweet in enumerate(q_item[2]):
        name = threading.currentThread().getName()
        print("Thread: {0} start put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                            time.strftime('%H:%M:%S')))
        item = "item-" + str(i)
        q.put([q_item[0], q_item[1], tweet, count])
        print("Thread: {0} successfully put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                                   time.strftime(
                                                                                                       '%H:%M:%S')))
    q.join()


def create_images(user_id, user_img_url, tweet, count):
    try:
        txt = tweet.retweeted_status.full_text
    except AttributeError:  # Not a Retweet
        txt = tweet.full_text
    font = ImageFont.truetype('font\Arial.ttf', 14)
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
            background.paste(img, (100, y))
    except Exception as e:
        print(e)
    background.paste(img, offset)
    background.save('processed_imgs\/'+'img'+str(count)+'.png')



def ffmpeg_call():
    today = str(datetime.date.today()).replace('-', '_')
    subprocess.call(['ffmpeg\/bin\/ffmpeg', '-y', '-framerate', '1/3', '-i', 'processed_imgs\img%d.png', '-r', '25', '-pix_fmt', 'yuv420p', 'twitter_feed_'+today+'.mp4'])


if __name__ == '__main__':
    q = queue.Queue(maxsize=4)
    completion_queue = queue.Queue()
    twit = twit.twitter_scrapper("keys")

    threads_num = 4  # 4 threads to do processes running at .001 seconds
    for i in range(threads_num):
        t = threading.Thread(name="Thread Processor-" + str(i), target=processor, args=(q,completion_queue))
        t.start()

    while(True):
        id = input("Twitter id?")
        q_item = [id, twit.get_user_pic(id), twit.get_users_tweets(id)]

        t = threading.Thread(name="ProducerThread", target=producer, args=(q, q_item))
        t.start()
        q.join()