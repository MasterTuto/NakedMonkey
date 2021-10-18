from random import choice
import requests


class Problem:
    def __init__(self, contest_obj):
        base_url = "https://codeforces.com/problemset/problem/{contest_id}/{index}"
        self.contest_obj = contest_obj

        contest_id = contest_obj['contestId']
        index = contest_obj['index']
        self.url = base_url.format(contest_id=contest_id, index=index)
    
    def as_url(self):
        return self.url

class CodeForces:
    def __init__(self):
        self.BASE_URL = "https://codeforces.com/api/{method_name}"
        pass

    def get_problems(self, *filters, rating=-1) -> [Problem]:
        def is_rating_valid(p) -> bool:
            if 'rating' in p:
                return p['rating'] == rating
            else:
                return False

        url = self.BASE_URL.format(method_name="problemset.problems")
        params = { "tags": ";".join(filters) }

        print(params)
        
        problems = requests.get( url, params=params ).json()['result']

        if 'problems' not in problems:
            return []

        problems = problems['problems']
        if rating > -1:
            problems = filter(is_rating_valid, problems)
        
        return list( map(lambda p: Problem(p), problems) )


    def random_problem(self):
        return choice( self.get_problems() )
    


if __name__ == "__main__":
    cf = CodeForces()

    problems = cf.get_problems("implementation", rating=1100)
    problem = choice(problems)

    print( problem.url )
