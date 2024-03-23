from openai.types.chat import ChatCompletion as BaseChatCompletion


class ChatCompletion(BaseChatCompletion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize an attribute to store additional data from server response
        self.evaluableai_data = {}

    def add_evaluableai_data(self, data):
        """
        Updates the additional data attribute with data from the server.

        Parameters:
        - data (dict): Data to append to the chat completion.
        """
        self.evaluableai_data.update(data)

    def get_evaluableai_data(self):
        """
        Retrieves the additional data associated with this chat completion.

        Returns:
        - dict: The additional data.
        """
        return self.evaluableai_data
