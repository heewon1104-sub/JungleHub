from repository.dayTotalCommitCountRepository import dayTotalCommitCountRepository
from repository.userCommitCountRepository import userCommitCountRepository
from repository.repositoryProfile import profile_repository
from repository.boardBlockListRepository import boardBlockListRepository
from module.githubApi import GithubApi
from module.scheduler import Scheduler
from model.dayTotalCommitCount import DayTotalCommitCount
from model.userCommitCount import UserCommitCount
from model.boardBlockList import BoardBlockList
import random


class CommitCountScheduler:

    def __init__(self):
        self.api = GithubApi()
        self.scheduler = Scheduler()

    def run(self):
        self.scheduler.runSecondsIntervalJob(
            self.job,
            self.getIntervalSeconds()
        )

    def getIntervalSeconds(self):
        oneMinute = 60
        return oneMinute * 10

    def job(self):

        result = profile_repository.read_all_jungler()

        def convert(user):
            return {
                'userId': user._id,
                'loginId': user.gitId, 
                'accessToken': user.githubaccesstoken
            }

        userList = map(convert, result)

        # userId, totalCommitCount
        resultList = self.api.getAllTotalCommitCount(list=userList)

        # 모든 유저의 오늘 커밋 수
        todayTotalCommitCount = sum([ item['totalCommitCount'] for item in resultList])

        # 어제 까지의 누적값
        lastCumulativeCount = dayTotalCommitCountRepository.lastDayCumulative()

        # 오늘의 누적값
        cumulativeCount = lastCumulativeCount + todayTotalCommitCount
        
        currentDayKey = DayTotalCommitCount.makeCurrentDayKey()
        newTotalCommitCount = DayTotalCommitCount(currentDayKey, count=todayTotalCommitCount, cumulativeCount=cumulativeCount)
        dayTotalCommitCountRepository.update(newTotalCommitCount)

        # user count 업데이트
        userCommitCountRepository.updateAllUserCount(resultList)


        # TODO: board block list 로직 추가

        allIndices = []
        for i in range(0,35):
            allIndices.append(i)

        CONSTANT=3

        totalBlockCount = 35
        openRate = (todayTotalCommitCount / CONSTANT) / totalBlockCount 
        if openRate > 1:
            openRate = 1

        openCount = int(totalBlockCount * openRate)
        # blockedCount = totalBlockCount - openCount

        lastBlock = boardBlockListRepository.todayOpenList()

        if lastBlock is not None:
            lastOpenList = lastBlock.openList

            availAbleCount = openCount - len(lastOpenList)
            if availAbleCount < 0:
                availAbleCount = 0

            # 여기서 newAvailableCount만큼 랜덤하게 뽑으면 끝 
            availableList = list(set(allIndices) - set(lastOpenList))

            newOpenList = random.sample(availableList, availAbleCount)

            lastBlock.openList = sorted(lastOpenList + newOpenList)

            boardBlockListRepository.update(lastBlock)

        else: 
            resultList = sorted(random.sample(allIndices, openCount))
            new = BoardBlockList(_id=BoardBlockList.makeKey(), indices=resultList)
            boardBlockListRepository.update(new)
