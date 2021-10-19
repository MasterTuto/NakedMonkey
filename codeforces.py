from random import choice
import requests
from typing import List


class Problem:
    def __init__(self, contest_obj):
        base_url = "https://codeforces.com/problemset/problem/{contest_id}/{index}"

        self.contest_id = contest_obj['contestId'] if 'contestId' in contest_obj else ''
        self.problemset_name = contest_obj['problemsetName'] if 'problemsetName' in contest_obj else ''
        self.index = contest_obj['index']
        self.name = contest_obj['name']
        self.type = contest_obj['type']
        self.rating = int(contest_obj['rating']) if 'rating' in contest_obj else -1
        self.tags = contest_obj['tags']


        self.url = base_url.format(contest_id=self.contest_id, index=self.index)
    
    def as_url(self):
        return self.url

    def __str__(self):
        return f"{self.contest_id}/{self.index}: {self.name}"

class CodeForces:
    def __init__(self):
        self.BASE_URL = "https://codeforces.com/api/{method_name}"
        pass

    def problems_not_solved_by(self, user:str, problems: List[Problem]) -> List[Problem]:
        def already_answered( problem ):
            return not any(
                x['problem']['contestId'] == problem['contestId'] and
                x['problem']['index'] == problem['index'] 
                    for x in got['result']
            )

        url = self.BASE_URL.format(method_name="user.status")

        got = requests.get(url, params={'handle': user}).json()

        if got['status'] == 'OK':
            return filter(already_answered,  problems)
        else:
            return []
    
    def get_problems(self, *filters, begin_rating=-1, end_rating=-1, user='') -> [Problem]:
        def is_rating_valid(p) -> bool:
            if 'rating' in p:
                if begin_rating > -1 and end_rating > -1:
                    return begin_rating <= p['rating'] <= end_rating
                elif begin_rating > -1:
                    return begin_rating <= p['rating']
                elif end_rating > -1:
                    return p['rating'] <= end_rating
            else:
                return False

        url = self.BASE_URL.format(method_name="problemset.problems")
        params = { "tags": ";".join(filters) }
        
        problems = requests.get( url, params=params ).json()['result']

        if 'problems' not in problems:
            return []

        problems = problems['problems']
        if begin_rating > -1 or end_rating > -1:
            problems = filter(is_rating_valid, problems)
        
        if user != '':
            problems = self.problems_not_solved_by(user, problems)
        
        return list( map(lambda p: Problem(p), problems) )


    def random_problem(self):
        return choice( self.get_problems() )

if __name__ == "__main__":
    cf = CodeForces()

    problems = cf.get_problems("", begin_rating=800, end_rating=-1, user="brenocarvalho2011")


    for p in problems:
        print (p)
