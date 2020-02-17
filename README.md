# Twitter to Video

### Introduction
In this project, we will be creating a multi-threaded application that picks the top 20 tweets from a Twitter handle and makes a 30 sec video out of it.
Every three seconds, the top tweet will be shown along with their profile picture and username. Currently, the application is a single
process running with 4 threads. The output format is a 1024x768 resolustion mp4 file running at 25 frames per second. Each of the 4
threads is responding for image processing, specifically creating the backgroud, drawing the username, user picture and writing the
tweet for all twenty images.

### How to Run?
This application requires primarily Tweepy, Python 3, and other packages specified in the requirements.txt file.

Please make sure all APIs have been installed before running the program. To run the program, run python main.py. 
Twitter keys must be in the root program directory named keys. The following is the format needed.

```python
[auth]
consumer_key = ****
consumer_secret = ****
access_token = ****
access_secret = ****
```

The following screenshots is the program in action and working:

<img src="https://github.com/BUEC500C1/video-djtrinh/blob/master/cli_picture.PNG?raw=true">

<img src="https://github.com/BUEC500C1/video-djtrinh/blob/master/Example.PNG?raw=true">
