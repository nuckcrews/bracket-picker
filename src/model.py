import json

__all__ = ["OpenAIModel"]

class OpenAIModel:

    def __init__(self, client):
        self._client = client

    def prompt(self, messages):
        response = self._client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.4
        )

        return response.choices[0].message.content

    def tool(self, messages, functions, tools):
        response = self._client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.5,
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if not tool_calls:
            raise Exception("No tool calls found in response")

        responses = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            responses.append(function_response)

        return responses