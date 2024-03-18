import json
from .model import OpenAIModel
from .tournament import MensTournament

__all__ = ["Bracket"]


class Bracket:

    def __init__(self, client, prompt, token_callback=None):
        self._model = OpenAIModel(client)
        self.prompt = prompt
        self.token_callback = token_callback
        self.current_round = 1
        self.rounds = 6
        self.picks = []
        self.tournament = MensTournament()

    def generate_bracket(self, callback):
        while self.current_round <= self.rounds:
            self.tournament = self._pick_round(self.current_round)
            callback(self.current_round, self.tournament)
            self.current_round += 1

    def _system_message(self):
        return {
            "role": "system",
            "content": "You are a highly intelligent college basketball fan. You have been selected to fill out a bracket for another fan based on their prompt. Always output all of the winners of the current round with the corresponding game number. The game number increments by 1 so the first game of the second round is 33. Always use the provided function to add your picks for the round and make sure to base your picks based on previous rounds. The picks must be valid.",
        }

    def _tournament_message(self):
        return {
            "role": "system",
            "content": "Some information about the March Madness Tournament:\nRound 1=1; Round 2=2; Sweet 16=3; Elite 8=4; Final 4=5; Championship=6;\nIt is the end of season tournament for NCAA basketball",
        }

    def _bracket_message(self):
        return {
            "role": "system",
            "content": f"Tournament Bracket:\n{json.dumps(self.tournament)}",
        }

    def _user_prompt(self):
        return {"role": "user", "content": "User Prompt: " + self.prompt}

    def _pick_round(self, round):
        messages = [
            self._tournament_message(),
            self._system_message(),
            self._bracket_message(),
            self._user_prompt(),
        ]
        messages.extend(self.picks)
        messages.append(
            {
                "role": "user",
                "content": f"What are your picks for the next round ({round}) based on my prompt and the results from the previous rounds? Add your picks to the add_picks function.",
            }
        )
        functions = self._functions()
        tools = self._tools()
        new_bracket = self._model.tool(messages, functions, tools)[0]

        if self.token_callback:
            self.token_callback(json.dumps(messages) + json.dumps(new_bracket))
        return new_bracket

    def _functions(self):
        return {"add_picks": self._add_picks}

    def _tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_picks",
                    "description": "Adds the picks to the bracket and returns the winners of the round",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "picks": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "game": {
                                            "type": "number",
                                            "description": "The game number played",
                                        },
                                        "name": {
                                            "type": "string",
                                            "description": "The name of the team",
                                        },
                                        "seed": {
                                            "type": "number",
                                            "description": "The seed of the team",
                                        },
                                    },
                                    "required": ["game", "name", "seed"],
                                    "description": "A team and their seed",
                                },
                            },
                        },
                        "required": ["picks"],
                    },
                },
            }
        ]

    def _add_picks(self, picks):
        print(picks)
        games = sorted(self.tournament, key=lambda k: k["game"])
        print(games)
        all_games = []
        new_games = []
        for game in games:
            winner = next(
                (winner for winner in picks if winner["game"] == game["game"]), None
            )
            if winner:
                game["winner"] = "team1" if game["team1"]["name"] == winner["name"] else "team2"

                if len(new_games) > 0 and new_games[-1]["team2"]["seed"] == 0:
                    new_games[-1]["team2"] = winner
                else:
                    new_games.append(
                        {
                            "game": len(games) + len(new_games) + 1,
                            "team1": {
                                "name": winner["name"],
                                "seed": winner["seed"],
                            },
                            "team2": {"name": "", "seed": 0},
                            "winner": "none",
                        }
                    )
            all_games.append(game)

        return all_games + new_games
