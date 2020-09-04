import random
import sys
import time
from multiprocessing import Process, JoinableQueue
import numpy as np
import sharedmem


def process(i, q, arg):
    while True:
        size = q.get(block=True)
        if isinstance(size, int):
            arr = np.frombuffer(arg, count=size)
        else:
            arr = size
        print(i, arr.sum())
        q.task_done()


def main(share):
    SIZE = 10000000
    shared = sharedmem.empty(SIZE)
    queues = [JoinableQueue(maxsize=1) for i in range(10)]
    processes = [Process(target=process, args=(i, q, shared)) for i, q in enumerate(queues)]
    [p.start() for p in processes]
    while True:
        time.sleep(5)
        size = random.randint(SIZE-1000, SIZE)
        dat = np.random.random(size)
        shared[:size] = dat
        put = size if share else dat
        print("regenerated", size, "; sum: ", dat.sum())
        [q.put(put) for q in queues]
        [q.join() for q in queues]


if __name__ == "__main__":
    share = True
    if len(sys.argv) > 1 and sys.argv[1] == "--no-share":
        share = False
    main(share=share)
