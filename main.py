import threading
import time
import queue

def processor(q):
    while (True):
        name = threading.currentThread().getName()
        print("Thread: {0} start get item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                            time.strftime('%H:%M:%S')))
        item = q.get()
        print("The item is %s" % item)
        time.sleep(.001)  # .001 seconds to process information
        print("Thread: {0} finish process item from queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                                 time.strftime(
                                                                                                     '%H:%M:%S')))
        q.task_done()


def producer(q, num_of_threads):
    # the main thread will put new items to the queue
    for i in range(int(num_of_threads)):
        name = threading.currentThread().getName()
        print("Thread: {0} start put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                            time.strftime('%H:%M:%S')))
        item = "item-" + str(i)
        q.put(item)
        print("Thread: {0} successfully put item into queue[current size = {1}] at time = {2} \n".format(name, q.qsize(),
                                                                                                   time.strftime(
                                                                                                       '%H:%M:%S')))
    q.join()


if __name__ == '__main__':
    q = queue.Queue(maxsize=4)

    threads_num = 4  # 4 threads to do processes running at .001 seconds
    for i in range(threads_num):
        t = threading.Thread(name="Thread Processor-" + str(i), target=processor, args=(q,))
        t.start()

    while(True):
        if q.empty():
            num_of_processes = input("How many tasks to queue?")
            t = threading.Thread(name="ProducerThread", target=producer, args=(q, num_of_processes,))
            t.start()
            q.join()