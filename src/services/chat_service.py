from src.models.llm_models import get_groq_model

class ChatService:
    def __init__(self, model_name='mixtral-8x7b-32768'):
        """
        Initialize the ChatService instance.

        Args:
            model_name (str): The name of the Large Language Model (LLM) to use.
                Defaults to 'mixtral-8x7b-32768'.
        """
        self.llm = get_groq_model(model_name)

    async def get_response(self, user_input: str) -> str:
        """
        Get the response from the LLM for the given user input.

        Args:
            user_input (str): The input from the user.

        Returns:
            str: The response from the LLM.
        """
        messages = [
            ("system", "You are a helpful assistant who gives the best possible answers for given query."),
            ("human", user_input),
        ]
        try:
            ai_msg = self.llm.invoke(messages)
            return ai_msg.content
        except Exception as e:
            return f"Error: {str(e)}"
