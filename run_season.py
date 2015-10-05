import csv
from rerank import rerank


class Team(object):
    def __init__(self, name, score=1200.0):
        self.name = name
        self.score = 1200

    def update_score(self, new_score):
        self.score = new_score


class TeamManager(object):

    teams = {}

    def create_team(self, team_name):
        self.teams[team_name] = Team(team_name)

        return self.teams[team_name]

    def get_or_create_team(self, team_name):
        team = self.teams.get(team_name)

        if team:
            return team

        return self.create_team(team_name)

    def print_ranking(self):
        team_list = list()

        for name, team in self.teams.items():
            team_list.append(team)

        print('|------|----------------------|-----------|')
        print('| Rank | Team                 | Elo Score |')
        print('|------|----------------------|-----------|')

        team_list.sort(key=lambda team: team.score, reverse=True)
        rank = 0
        for team in team_list:
            rank += 1

            print('| %4d | %20s | %.4f |' % (rank, team.name, team.score))

        print('|------|----------------------|-----------|')


class Game(object):
    def __init__(self, team_1, team_2):
        self.team_1 = team_1
        self.team_2 = team_2

    def predict_to_win(self):
        if self.team_1.score > self.team_2.score:
            return self.team_1

        elif self.team_1.score < self.team_2.score:
            return self.team_2

        return None

    def set_outcome(self, score_team_1, score_team_2):
        r_1, r_2 = rerank(self.team_1.score, self.team_2.score, score_team_1,
                          score_team_2)

        self.team_1.update_score(r_1)
        self.team_2.update_score(r_2)


def run_season(season='2015'):
    csv_file_path = 'data/%s.season.csv' % season
    team_manager = TeamManager()

    with open(csv_file_path, 'rw+') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # The first row of CSV, is column information
        next(reader, None)

        for row in reader:

            team_1 = team_manager.get_or_create_team(row[4])
            team_2 = team_manager.get_or_create_team(row[6])

            score_team_1 = int(row[7])
            score_team_2 = int(row[8])

            game = Game(team_1, team_2)
            game.set_outcome(score_team_1, score_team_2)

        team_manager.print_ranking()
