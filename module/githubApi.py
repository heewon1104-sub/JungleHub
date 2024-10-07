import requests
import json
from datetime import datetime, timedelta, timezone
from configuration.config import Config
from urllib.parse import parse_qs
import aiohttp
import asyncio


class GithubApi:

    def __init__(self):
        self.graphqlUrl = "https://api.github.com/graphql"
        self.githubUrl = "https://github.com"
        self.restAPIUrl = "https://api.github.com"
        config = Config()

        if config.isDev():
            self.clientId = config.find("GITHUB_CLIENT_ID_DEV")
            self.clientKey = config.find("GITHUB_CLIENT_SECRET_DEV")
        else:
            self.clientId = config.find("GITHUB_CLIENT_ID")
            self.clientKey = config.find("GITHUB_CLIENT_SECRET")

        self.scope = 'repo%20user'

    def getLoginUrl(self):
        githubLoginUrl = f"https://github.com/login/oauth/authorize?client_id={self.clientId}&scope={self.scope}"
        return githubLoginUrl

    def getAccessToken(self, code):
        headers = {
            "Content-Type": "application/json"
        }

        data = json.dumps({
            "code": code,
            "client_id": self.clientId,
            "client_secret": self.clientKey,
        })

        response = requests.post(self.githubUrl + "/login/oauth/access_token", headers=headers, data=data)

        if response.status_code == 200:
            resultText = response.text
            parsedQuery = parse_qs(resultText)
            return parsedQuery.get('access_token', [None])[0]
        else:
            print(response.text)

    def getUserInfo(self, githubAccessToken):
        headers = {
            "Authorization": f"bearer {githubAccessToken}"
        }

        response = requests.get(self.restAPIUrl + "/user", headers=headers)

        if response.status_code == 200:
            jsonResult = json.loads(response.text)
            return jsonResult
        else:
            print(response.text)

    def getTotalCommitCountToday(self, loginId, accessToken):

        def koreaNowDatetime():
            KST = timezone(timedelta(hours=9))
            return datetime.now(KST)

        def koreaNextDatetime(now):
            tomorrow = now + timedelta(days=1)
            return tomorrow

        def dateTimeToKSTString(date):

            # 문자열로 변환 (ISO 8601 형식)
            formatted_time = date.strftime('%Y-%m-%dT%H:%M:%S%z')

            # '+0900'을 '+09:00' 형식으로 변경
            formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]

            return formatted_time

        fromDatetime = koreaNowDatetime()
        toDatetime = koreaNextDatetime(fromDatetime)

        return self.getTotalCommitCount(
            loginId=loginId, 
            accessToken=accessToken, 
            fromDatetime=dateTimeToKSTString(fromDatetime), 
            toDatetime=dateTimeToKSTString(toDatetime)
        )
    

    # from, to를 date 타입으로 받아서, 아래 형태로 바꿔서 query 날리기
    def getTotalCommitCount(self, loginId, accessToken, fromDatetime, toDatetime):
        query = self.getTotalCommitCountQuery(loginId, fromDatetime=fromDatetime, toDatetime=toDatetime)
        headers = self.getTotalCommitCountHeader(accessToken)
        data = json.dumps({"query": query})
        
        response = requests.post(self.graphqlUrl, headers=headers, data=data)

        # 결과 출력
        if response.status_code == 200:
            result = response.json()  # 응답을 JSON으로 파싱

            if not result or not result['data'] or not result['data'] or not result['data']['contributionsCollection'] or not result['data']['contributionsCollection']['totalCommitContributions']:
                return 0

            try:
                total_commit_contributions = result['data']['user']['contributionsCollection']['totalCommitContributions']
            except KeyError:
                print("The expected key was not found in the response.")
        else:
            print(response.text)

        return total_commit_contributions
    
    def getTotalCommitCountQuery(self, loginId, fromDatetime, toDatetime):
        return f"""
        query {{
            user(login: "{loginId}") {{
                contributionsCollection(from: "{fromDatetime}", to: "{toDatetime}") {{
                    totalCommitContributions
                }}
            }}
        }}
        """

    def getTotalCommitCountHeader(self, accessToken):
        return {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }

    async def getDataAsync(self, url, data, headers):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    # JSON 응답인 경우
                    body = await response.json()
                    return body
                else:
                    # 오류 응답인 경우
                    error_message = await response.text()
                    print(f"Error: {response.status}, Message: {error_message}")
                    return None
    

    async def getTotalCommitCountTodayAsync(self, loginId, accessToken, userId):

        def nowDatetime():
            # 한국시간 기준, +6 기준으로 업데이트 하기 때문에 아래와 같이 -6을 함 
            ourZone = timezone(timedelta(hours=9-6))
            return datetime.now(ourZone).replace(hour=0, minute=0, second=0, microsecond=0)

        def nextDatetime(now):
            tomorrow = now + timedelta(days=1)
            return tomorrow

        def dateTimeToKSTString(date):
            formatted_time = date.strftime('%Y-%m-%dT%H:%M:%S%z')
            formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]
            return formatted_time

        fromDatetime = nowDatetime()
        toDatetime = nextDatetime(fromDatetime)

        return await self.getTotalCommitCountAsync(
            loginId=loginId, 
            accessToken=accessToken, 
            userId = userId,
            fromDatetime=dateTimeToKSTString(fromDatetime), 
            toDatetime=dateTimeToKSTString(toDatetime)
        )


    async def getTotalCommitCountAsync(self, loginId, accessToken, userId, fromDatetime, toDatetime):
        query = self.getTotalCommitCountQuery(loginId, fromDatetime=fromDatetime, toDatetime=toDatetime)
        headers = self.getTotalCommitCountHeader(accessToken)
        data = json.dumps({"query": query})
        
        response = await self.getDataAsync(url=self.graphqlUrl, data=data, headers=headers)

        return {
            "userId": userId,
            "totalCommitCount": response['data']['user']['contributionsCollection']['totalCommitContributions']
        }

    async def requestGetAllTotalCommitCount(self, list):
        tasks = [ self.getTotalCommitCountTodayAsync(item['loginId'], item['accessToken'], item['userId']) for item in list]
        responses = await asyncio.gather(*tasks)
        return responses

    def getAllTotalCommitCount(self, list):
        responses = asyncio.run(self.requestGetAllTotalCommitCount(list))
        return responses
        


