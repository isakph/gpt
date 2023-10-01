import os
import argparse
import openai
from typing import Union
from openai.openai_object import OpenAIObject

openai.api_key = os.environ.get('OPENAI_KEY')

# Think I'll skip implementing something like this. Just assume 3.5, as it is a lot cheaper.
# def choose_model(answer: Union[3.5, 4]) -> str:
#     if answer == 3.5:
#         return "gpt-3.5-turbo"
#     return "gpt-4"

def choose_model(model: Union[int, float]) -> str:
    """
    Accepts the values 3.5 and 4 and returns either the string 'gpt-3.5-turbo' or 'gpt-4'.
    """
    assert model == 3.5 or model == 4
    # while True:
    #     try: 
    #         choice = int(input("To choose model, enter 3.5 or 4: "))
    #     except ValueError:
    #         print("Invalid input. Try again.")
    #         continue
    #     else: break

    if model == 3.5:
        return "gpt-3.5-turbo"
    return "gpt-4"


class GPT_conversation:
    """
    TODO: Implement this class. 
    The idea, before implementing it, is that an object of this class can be
    used to carry on a conversation indefinitely or start new conversations
    as desired by the user. 
    """
    def __init__(self, model: str):
        assert model == "gpt-3.5-turbo" or model == "gpt-4"
        """
        Initiates a GPT_conversation object with default values.
        """
        self.messages = [] 


def get_first_response(message: str = None, print_to_terminal: bool = True) -> OpenAIObject:
    """
    Asks the user to enter:

    1) which model should be used, # TODO: Make a coherent implementation of model choice.
    2) a prompt, 

    and then requests a chat completion. The message is printed
    and the chat completion object returned.
    Might add support for other things than writing the message to stdout later.
    """
    if message is None:
        message = input("Your prompt: ")
    response = openai.ChatCompletion.create(
        #model = choose_model(int(input("enter 3.5 or 4"))),
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
            ]
        )
    
    if print_to_terminal:
        print(response['choices'][0]['message']['content'])
    return response
    
def hold_conversation(first_response: OpenAIObject) -> None:
    """
    Lets the user keep a conversation with ChatGPT (always 3.5 for the time being).
    The conversation keeps going until the user types '0'.
    """
    
    convo = [first_response['choices'][0]]
    keep_going = True
    while keep_going:
        next_message = input("Type your next prompt (or: 0 to stop, 1 to start a new conversation): ")
        try:
            if int(next_message) == 0:
                break
            if int(next_message) == 1:
                ... # TODO: Implement starting a new conversation
                # convo = something
        except ValueError:
            pass # Anything other than 0 is used to create a new chat completion.
        
        convo.append({"role": "user", "content": next_message})

        response = openai.ChatCompletion.create(
        # model = choose_model(int(input("enter 3.5 or 4"))),
            model = "gpt-3.5-turbo",
            messages = convo # TODO :I pass something wrong along somewhere. It's probably from when I created convo object originally.:
            # This was the error: openai.error.InvalidRequestError: Additional properties are not allowed ('finish_reason', 'index', 'message' were unexpected) - 'messages.0'
        )

        print(response['choices'][0]['message']['content']) # this might have to be tweaked as well
        convo.append(response['choices'][0])
        

def main():
    first_response = get_first_response()
    hold_conversation(first_response)

# response = get_first_response()
# print(type(response))
# print(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()