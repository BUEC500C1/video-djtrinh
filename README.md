# Twitter to Video

### Introduction
In this project, we will be creating a multi-threaded application that picks the top 20 tweets from a Twitter handle and makes a 30 sec video out of it.
Every three seconds, the top tweet will be shown along with their profile picture and username. Currently, the application is a single
process running with 4 threads. The output format is a 1024x768 resolustion mp4 file running at 25 frames per second. Each of the 4
threads is responsible for image processing, specifically creating the backgroud, drawing the username, user picture and writing the
tweet for all twenty images.

### Computer Evaluation

In my current computer configuration, I have a 6-core processor with 12 threads and a maximum clock rate of 4.1 Ghz. As a result of this, I am really unable to see any bottlenecks when running code conversion tests which were the following:

```python
ffmpeg.exe -i test.mp4 -c:a copy -c:v copy -r 30 -s hd720 -b:v 2M output.mp4
```

```python
ffmpeg.exe -i test.mp4 -c:a copy -c:v copy -r 30 -s hd480 -b:v 1M output.mp4
```

Each of the commands on a 3 minute test video finished in < 1 seconds. Because of this, we will be running the program with 4 threads which is overkill.

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

### Results
The bottleneck for the program is actually the image processing side. While the entire process finishes in approximately 3 secs, 4 threads really pushes the cpu and since it is a very powerful laptop CPU, results are available right away. The following snippet is a picture of the CPU usage when grabbing tweets with the Twitter API, image processig forming the final images for FFMPEG, and running FFMPEG. The program itself is using the 4 threads to process image requests from a Queue and the FFMPEG API is multithreaded from the operating system/HW.

<img src="https://github.com/BUEC500C1/video-djtrinh/blob/master/cpu_usage.PNG?raw=true">

The next steps for this project to to have a way to schedule multiple Twitter usernames and multi-processes. Also, a web interface of some sort can be utilized for a much better user experience. There are some corner cases that still need to be taken care of. For example, some Twitter users can have their account suspended affecting Tweet grabs.
