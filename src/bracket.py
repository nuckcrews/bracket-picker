import json
from .model import OpenAIModel
from .tournament import MensTournament

__all__ = ["Bracket"]


class Bracket:

    def __init__(self, client, prompt):
        self._model = OpenAIModel(client)
        self.prompt = prompt
        self.current_round = 1
        self.rounds = 6
        self.picks = []

    def generate_bracket(self, callback):
        while self.current_round <= self.rounds:
            winners = self._pick_round(self.current_round)
            self._add_round_winners(winners)
            callback(self.current_round, winners)
            self.current_round += 1

    def _system_message(self):
        return {
            "role": "system",
            "content": "You are a highly intelligent college basketball fan. You have been selected to fill out a bracket for another fan based on their prompt. Always use the provided function to add your picks for the round.",
        }

    def _bracket_message(self):
        return {"role": "system", "content": f"Tournament Bracket:\m{MensTournament()}"}

    def _user_prompt(self):
        return {"role": "user", "content": self.prompt}

    def _pick_round(self, round):
        messages = [
            self._system_message(),
            self._bracket_message(),
            self._user_prompt(),
        ]
        messages.extend(self.picks)
        messages.append(
            {
                "role": "user",
                "content": "What are your picks for this next round? Add your picks to the add_picks function.",
            }
        )
        functions = self._functions()
        tools = self._tools()
        picks = self._model.tool(messages, functions, tools)[0]
        return picks

    def _add_round_winners(self, winners):
        self.picks.append(
            {
                "role": "assistant",
                "content": "The winners of this round are: " + json.dumps(winners),
            }
        )

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
                                        "team": {"type": "string"},
                                        "rank": {"type": "number"},
                                    },
                                    "required": ["team", "rank"],
                                    "description": "A team and their rank",
                                },
                            },
                        },
                        "required": ["picks"],
                    },
                },
            }
        ]

    def _add_picks(self, picks):
        return picks
