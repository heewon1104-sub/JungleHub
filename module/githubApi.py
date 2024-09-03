import requests
import json
from datetime import datetime, timedelta, timezone
from configuration.config import Config
from urllib.parse import parse_qs

    
class GithubApi:

    def __init__(self):
        self.graphqlUrl = "https://api.github.com/graphql"
        self.restUrl = "https://github.com"
        config = Config()
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

        response = requests.post(self.restUrl + "/login/oauth/access_token", headers=headers, data=data)

        # 결과 출력
        print("🍎🍎🍎🍎🍎🍎🍎🍎🍎")
        if response.status_code == 200:
            resultText = response.text
            parsedQuery = parse_qs(resultText)
            return parsedQuery.get('access_token', [None])[0]
        else:
            print(response.text)


    def getTotalCommitCountToday(self):

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
        toDatetime = koreaNextDatetime()

        return self.getTotalCommitCount(dateTimeToKSTString(fromDatetime), dateTimeToKSTString(toDatetime))


    # from, to를 date 타입으로 받아서, 아래 형태로 바꿔서 query 날리기
    def getTotalCommitCount(self, loginId, accessToken, fromDatetime, toDatetime):

        query = f"""
        query {{
            user(login: "{loginId}") {{
                contributionsCollection(from: "{fromDatetime}", to: "{toDatetime}") {{
                    totalCommitContributions
                }}
            }}
        }}
        """
        headers = {
            "Authorization": f"Bearer {accessToken}",
            "Content-Type": "application/json"
        }

        data = json.dumps({"query": query})

        response = requests.post(self.graphqlUrl, headers=headers, data=data)

        # 결과 출력
        if response.status_code == 200:
            result = response.json()  # 응답을 JSON으로 파싱
            try:
                total_commit_contributions = result['data']['user']['contributionsCollection']['totalCommitContributions']
            except KeyError:
                print("The expected key was not found in the response.")
        else:
            print(response.text)

        return total_commit_contributions


