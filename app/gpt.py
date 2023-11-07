import os
import openai
from typing import Union, Dict, List
# from openai.openai_object import OpenAIObject

openai.api_key = os.environ.get('OPENAI_KEY')


class GPT_conversation:
    """
    TODO: Implement this class. 
    The idea, before implementing it, is that an object of this class can be
    used to carry on a conversation indefinitely or start new conversations
    as desired by the user. 
    """
    def __init__(self, options: Dict[str, Union[int, float]], stream: bool = False):
        """
        Initiates a GPT_conversation object with default values.
        @param options: At the moment, this only implements model choice: the user
        can choose between 'gpt-3.5-turbo' by entering 3.5 and 'gpt-4' by entering 4.
        @param stream: I intend to let the user enable stream at some point.
        """
        self._model = self.__choose_model(options['model'])


    def __choose_model(self, choice: Union[int, float] = 3.5) -> str:
        """
        Accepts 3.5 or 4 as choice and returns either 'gpt-3.5-turbo' or 'gpt-4'.
        3.5 is the default value simply because it is cheaper to run.
        Update as of Nov. 6th, 2023: 
        Models gpt-4-turbo added as: gpt-4-1106-preview
        gpt-3-turbo updated as: gpt-3.5-turbo-1106
        TODO: Make use of these
        """
        if choice == 4:
            return 'gpt-4'
        return 'gpt-3.5-turbo'


    def __get_first_response(self, 
                        message: str = None,
                        print_to_terminal: bool = True # might add some other output option
                        ) -> List[Dict[str, str]]:
        """
        Asks the user to enter a prompt during the creation of the ChatCompletion. 
        The response to this prompt is printed to terminal.
        """
        if message is None:
            message = input("Your prompt: ")
        # if options is not None: # this should be deletable
        #     assert options['model'] == 3.5 or options['model'] == 4
        #     model_choice = self.__choose_model(options['model'])

        chat_completion = openai.ChatCompletion.create(
            model = self._model,
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
                ]
            )
        
        if print_to_terminal:
            print(chat_completion['choices'][0]['message']['content'])
        return [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
                {'content': chat_completion['choices'][0]['message']['content'],
                 'user': 'assistant'}]
        

    def hold_conversation(self) -> None:
        """
        Lets the user keep a conversation with the chose model.
        The conversation keeps going until the user types '0'.
        The user can press 1 to initiate a new conversation
        """
        convo = self.__get_first_response()
        
        keep_going = True
        while keep_going:
            next_message = input("Type your next prompt (0 to stop, 1 to start a new conversation): ")
            try:
                if int(next_message) == 0:
                    break
                if int(next_message) == 1:
                    convo = self.__get_first_response()
                    continue
            except ValueError:
                pass # Anything other than 0 or 1 is used to create a new chat completion.
            
            convo.append({"role": "user", "content": next_message})
            print("taking a look at 'convo' before creating a second response:\n", convo) # looks good, but "'user' is unexpected" is the error

            response = openai.ChatCompletion.create(
                model = self._model,
                messages = convo # TODO :I pass something wrong along somewhere. It's probably from when I created convo object originally.:
                # This was the error: openai.error.InvalidRequestError: Additional properties are not allowed ('finish_reason', 'index', 'message' were unexpected) - 'messages.0'
            )
            answer = response['choices'][0]['message']['content']
            print(answer) # this might have to be tweaked as well
            convo.append({"role": "assistant", "content": answer}) # I'm appending a list, right?
        

def main(options = None):
    gpt_model = GPT_conversation(options)
    gpt_model.hold_conversation()
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Who won the world series in 2020?"},
    #         {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #         {"role": "user", "content": "Where was it played?"}
    #     ]
    # )
    # print(response)
    # answer = response['choices'][0]['message']['content']
    # print(answer)

if __name__ == "__main__":
    options = {'model': 3.5}
    main(options)