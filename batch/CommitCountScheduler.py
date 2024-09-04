from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository
from module.githubApi import GithubApi
from module.scheduler import Scheduler
from model.dayTotalCommitCount import DayTotalCommitCount
from model.userCommitCount import UserCommitCount


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

        result = profile_repository.read_all_jungler()

        def convert(user):
            return {
                'userId': user._id,
                'loginId': user.gitId, 
                'accessToken': user.githubaccesstoken
            }

        list = map(convert, result)

        # userId, totalCommitCount
        resultList = self.api.getAllTotalCommitCount(list=list)

        # dayTotalCommitCount 업데이트 
        totalCommitCount = sum([ item['totalCommitCount'] for item in resultList])
        currentDayKey = DayTotalCommitCount.makeCurrentDayKey()
        dayTotalCommitCountRepository.updateCount(currentDayKey, totalCommitCount)

        # user count 업데이트
        userCommitCountRepository.updateAllUserCount(resultList)


        # TODO: board block list 로직 추가

        