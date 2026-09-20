import logging

from openai import OpenAI

from .config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self):
        self._gemini = OpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        self._groq = OpenAI(
            api_key=settings.groq_api_key, base_url="https://api.groq.com/openai/v1"
        )

    def complete(self, messages: list[dict], prefer_groq: bool = False):
        client = self._groq if prefer_groq else self._gemini
        model = "openai/gpt-oss-120b" if prefer_groq else "gemini-3.6-flash"
        try:
            response = client.chat.completions.create(model=model, messages=messages)
        except Exception as e:
            if not prefer_groq:
                logger.warning(
                    f"Primary provider failed with error: {e}. Falling back to Groq."
                )
                return self.complete(messages, prefer_groq=True)

            # If prefer_groq was already True and it failed, re-raise or handle the fallback error
            raise e  # noqa: TRY201
        return response.choices[0].message.content


llm_client = LLMClient()
