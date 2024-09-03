
from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler:

    def __init__(self, daemon=True):
        self._scheduler = BackgroundScheduler(daemon=daemon)

    def runSecondsIntervalJob(self, job, seconds):
        self._scheduler.add_job(job, 'interval', seconds=seconds)
        self._scheduler.start()

''' 사용 예시

scheduler = Scheduler()

def job():
    print(1)

scheduler.runSecondsIntervalJob(job=job, seconds=10)

참고: https://blablacoding.tistory.com/10

'''