# Uses the queue.Queue class to create a queue used to run jobs in the background.
# Queue is a FIFO

from queue import Queue
from threading import Thread
from time import sleep
from random import randint

from opentelemetry import metrics

class Jobs:
    
    def __init__(self):
        self.q = Queue()
        self.q_counter = metrics.get_meter("jobs.enqueued").create_up_down_counter(
            name="jobs_queue_length",
            description="number of jobs in the queue"
        )
        self.__stop_processing = object()

    def enqueue(self, job, *args, **kwargs):
        self.q.put(job(*args, **kwargs))
        self.q_counter.add(1)

    def process(self):
        for job, args, kwargs in iter(self.q.get, self.__stop_processing):
            job(*args, **kwargs)
            self.q_counter.add(-1)

    # Method that starts the processing of running jobs in a non-blocking way.
    def start(self):
        Thread(target=self.process, daemon=True).start()

    # Method that stops the processing of running jobs.
    def stop(self):
        self.enqueue(self.__stop_processing)
        
            
def translate_post(content, from_lang='jp', to_lang='en'):
    ''' translate content from one language to another '''
    sleep(randint(1, 15)) # simulate a long running job
    return content # returns the same content for this demo.

# Example usage:
# jobs = Jobs()
# jobs.enqueue(translate_post, 'こんにちは世界')
# jobs.enqueue(translate_post, 'こんにちは世界', from_lang='ja', to_lang='fr')
# jobs.enqueue(translate_post, 'こんにちは世界', from_lang='ja', to_lang='es')
# jobs.enqueue(jobs.StopProcessing)