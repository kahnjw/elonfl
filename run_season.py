import csv
from rerank import rerank


class Team(object):
    def __init__(self, name):
        self.name = name
        self.score = 1200
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.pd_list = []
        self.points_scored_list = []
        self.points_allowed_list = []

    def update_score(self, new_score):
        self.score = new_score

    def discount_score(self):
        self.score = (self.score + 2400) / 3
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.pd_list = []
        self.points_scored_list = []
        self.points_allowed_list = []

    def win(self):
        self.wins += 1

    def loss(self):
        self.losses += 1

    def tie(self):
        self.ties += 1

    def record(self):
        if self.ties == 0:
            return '%d-%d' % (self.wins, self.losses)

        return '%d-%d-%d' % (self.wins, self.losses, self.ties)

    def add_score(self, _for, against):
        self.pd_list.append(_for - against)
        self.points_scored_list.append(_for)
        self.points_allowed_list.append(against)

    def pd(self):
        return float(sum(self.pd_list)) / len(self.pd_list)

    def points_for(self):
        return float(sum(self.points_scored_list)) / len(
            self.points_scored_list)

    def points_against(self):
        return float(sum(self.points_allowed_list)) / len(
            self.points_allowed_list)


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

    def discount_season(self):
        for name, team in self.teams.items():
            team.discount_score()

    def print_ranking(self):
        team_list = list()

        for name, team in self.teams.items():
            team_list.append(team)

        gaurd = '|------|----------------------|--------|-------|----------|----------|-----------|'

        print(gaurd)
        print('| Rank | Team                 | Record | PD    | Pts For  | Pts Agst | Elo Score |')
        print(gaurd)

        team_list.sort(key=lambda team: team.score, reverse=True)
        rank = 0
        for team in team_list:
            rank += 1

            team_data = (rank, team.name, team.record(), team.pd(),
                         team.points_for(), team.points_against(), team.score)

            print('| %4d | %20s | %6s | %5.1f | %8.1f | %8.1f | %9.4f |' % team_data)

        print(gaurd)


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

        if score_team_1 > score_team_2:
            self.team_1.win()
            self.team_2.loss()
        elif score_team_1 < score_team_2:
            self.team_2.win()
            self.team_1.loss()
        else:
            self.team_2.tie()
            self.team_1.tie()

        self.team_1.add_score(score_team_1, score_team_2)
        self.team_2.add_score(score_team_2, score_team_1)

        self.team_1.update_score(r_1)
        self.team_2.update_score(r_2)


def run_season(season='2015', last=False):
    season_int = int(season)

    if season_int != 2011 and not last:
        team_manager = run_season(str(season_int - 1), True)
        team_manager.discount_season()
    else:
        team_manager = TeamManager()

    csv_file_path = 'data/%s.season.csv' % season
    team_manager = TeamManager()

    with open(csv_file_path, 'rw+') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # The first row of CSV is column information
        next(reader, None)

        for row in reader:

            team_1 = team_manager.get_or_create_team(row[4])
            team_2 = team_manager.get_or_create_team(row[6])

            score_team_1 = int(row[7])
            score_team_2 = int(row[8])

            game = Game(team_1, team_2)
            game.set_outcome(score_team_1, score_team_2)

        if not last:
            team_manager.print_ranking()

    return team_manager
