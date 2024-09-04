from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from module.githubApi import GithubApi
from module.scheduler import Scheduler
from model.dayTotalCommitCount import DayTotalCommitCount
from model.userCommitCount import UserCommitCount

from datetime import datetime

class CommitCountScheduler:

    def __init__(self):
        self.api = GithubApi()
        self.scheduler = Scheduler()

        self.count = 1

    def run(self):
        self.scheduler.runSecondsIntervalJob(
            self.job,
            self.getIntervalSeconds()
        )

    def getIntervalSeconds(self):
        oneMinute = 60
        return oneMinute * 5

    def job(self):

        list = [
            {
                'userId': "wjdwoaud", # 유저 식별 값 
                'loginId': 'jjm159', # 깃허브 아이디
                'accessToken': 'test'
            }
        ] * 10

        # userId, totalCommitCount
        resultList = self.api.getAllTotalCommitCount(list=list)

        # dayTotalCommitCount 업데이트 
        totalCommitCount = sum([ item['totalCommitCount'] for item in resultList])
        currentDayKey = DayTotalCommitCount.makeCurrentDayKey()
        dayTotalCommitCountRepository.updateCount(currentDayKey, totalCommitCount)

        # user count 업데이트
        userCommitCountRepository.updateAllUserCount(resultList)



        