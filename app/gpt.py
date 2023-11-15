import sys
import os
import openai
from typing import Union, Dict, List, Any

openai.api_key = os.environ.get('OPENAI_KEY')


class GPT_conversation:
    """
    The idea is that an object of this class can be
    used to carry on a conversation indefinitely or start new conversations
    as desired by the user. 
    """
    def __init__(self, options: Dict[str, Any], stream: bool = False):
        """
        Initiates a GPT_conversation object with default values.
        @param options: TODO: the user
        can choose between 'gpt-3.5-turbo-1106' by entering 3.5 and 'gpt-4-1106-preview' by entering 4.
        @param stream: I intend to let the user enable stream at some point.
        """
        self._model = self.__choose_model(options['model'])
        self._debug = True if "debug" in options.keys() else False
        self._convo: list[dict] = []


    def __choose_model(self, choice: Union[int, float] = 3.5) -> str:
        """
        Accepts 3.5 or 4 as choice and returns either 'gpt-3.5-turbo' or 'gpt-4'.
        3.5 is the default value simply because it is cheaper to run.
        Update as of Nov. 6th, 2023: 
        Models gpt-4-turbo added as: gpt-4-1106-preview
        gpt-3-turbo updated as: gpt-3.5-turbo-1106
        """
        if choice == 4:
            return 'gpt-4-1106-preview'
        return 'gpt-3.5-turbo-1106'


    def __get_first_response(self, 
                        message: str = None,
                        print_to_terminal: bool = True # might add some other output option
                        ) -> List[Dict[str, str]]:
        """
        Asks the user to enter a prompt during the creation of the ChatCompletion. 
        A separate method for the first completion is practical to provide some 
        initial context.
        The response to this prompt is printed to terminal by default.
        """
        if message is None:
            message = input("Your prompt: ")
        
        context_and_message = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", 
                 "content": "I want concise answers with emphasis on technical details and explanations."},
                {"role": "assistant", "content": "I will do my best to explain things logically and precisely."},
                {"role": "user", "content": message}
                ]

        # Sending a chat completion request to OpenAI:
        chat_completion = openai.ChatCompletion.create(
            model = self._model,
            messages = context_and_message
            )
        
        if self._debug:
            print("Printing the chat completion object:", chat_completion)

        if print_to_terminal:
            print(chat_completion['choices'][0]['message']['content'])
        
        # Adding the dict containing 'user' and 'content' to the conversation
        self._convo = context_and_message
        self._convo.append(chat_completion['choices'][0]['message'])
        if self._debug:
            print("Printing the type of self._convo:", type(self._convo), 
                  "\nPrinting type of 'context_and_message:", type(context_and_message))
        

    def hold_conversation(self) -> None:
        """
        Lets the user keep a conversation with the chose model.
        The conversation keeps going until the user types '0'.
        The user can press 1 to initiate a new conversation
        """
        self.__get_first_response()
        
        keep_going = True
        while keep_going:
            next_message = input("Next prompt (0 to stop, 1 to start a new conversation): ")
            try:
                if int(next_message) == 0:
                    break
                if int(next_message) == 1:
                    self.__get_first_response()
                    continue
            except ValueError:
                pass # Anything other than 0 or 1 is used to create a new chat completion.
            
            self._convo.append({"content": next_message, "role": "user"})
            if self._debug:
                print("taking a look at 'self._convo' before creating another response:\n", self._convo)

            response = openai.ChatCompletion.create(
                model = self._model,
                messages = self._convo
            )
            answer = response['choices'][0]['message']['content']
            print(answer) # TODO: better way of delivering content
            self._convo.append({"role": "assistant", "content": answer}) 
        

def main(options = None):
    gpt_model = GPT_conversation(options)
    gpt_model.hold_conversation()


if __name__ == "__main__":
    options = {'model': 4} # TODO: Implement model choice
    arguments = set(sys.argv[1:]) # only "debug" is currently an accepted argument
    if "debug" in arguments:
        options["debug"] = True
    
    main(options)