import threading
import random
from collections import deque

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

buffer = deque()
lock = threading.Lock()
producer_is_done = threading.Event()

def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with lock:
            buffer.append(num)
            with open("all.txt", "a") as f:
                f.write(str(num) + "\n")
            if len(buffer) > BUFFER_SIZE:
                buffer.popleft()
    producer_is_done.set()

def even_consumer():
    while not producer_is_done.is_set() or buffer:
        with lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                with open("even.txt", "a") as f:
                    f.write(str(num) + "\n")

def odd_consumer():
    while not producer_is_done.is_set() or buffer:
        with lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                with open("odd.txt", "a") as f:
                    f.write(str(num) + "\n")

if __name__ == "__main__":
    producer_thread = threading.Thread(target=producer)
    consumer_even_thread = threading.Thread(target=even_consumer)
    consumer_odd_thread = threading.Thread(target=odd_consumer)

    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    print("All threads are terminated.")
