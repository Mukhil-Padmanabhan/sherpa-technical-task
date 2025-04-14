from openai import AzureOpenAI
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from app.config import settings
from app.utils.agentic_fallback import fallback_knowledge_search
import torch


torch.set_num_threads(1)

class GPTClient:
    """
    Handles GPT-based generation using Azure OpenAI with fallback to Hugging Face.
    """

    def __init__(self, api_key: str = None, endpoint: str = None):
        self.api_key = api_key or settings.AZURE_API_KEY
        self.endpoint = endpoint or settings.AZURE_ENDPOINT
        self.azure_model = settings.AZURE_GPT_MODEL
        self.api_version = settings.AZURE_GPT_VERSION
        self.fallback_model_id = settings.FALLBACK_LLM

        # Lazy loading for HuggingFace fallback
        self.fallback_pipeline = None

    def generate_answer(self, messages: list[dict]) -> str:
        """
        Calls Azure OpenAI GPT (chat format). Falls back to HF model if Azure fails.
        """
        try:
            client = AzureOpenAI(
                api_key=self.api_key,
                azure_endpoint=self.endpoint,
                api_version=self.api_version
            )
            response = client.chat.completions.create(
                model=self.azure_model,
                messages=messages,
                temperature=0.2
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Azure GPT failed: {e}")
            try:
                user_question = messages[-1]["content"]
                return fallback_knowledge_search(user_question)
            except Exception as agentic_error:
                print(f"[Agentic Fallback Failed]: {agentic_error}")
                raise Exception("All generation methods failed.")


    def _generate_with_fallback(self, prompt: str) -> str:
        """
        Uses Hugging Face pipeline (e.g., FLAN-T5, Mistral) as fallback.
        """
        try:
            if not self.fallback_pipeline:
                self.fallback_pipeline = pipeline(
                    "text2text-generation",
                    model=self.fallback_model_id,
                    tokenizer=self.fallback_model_id,
                    device=-1,
                    model_kwargs={"force_download": True}
                )
            result = self.fallback_pipeline(prompt, max_new_tokens=256)[0]["generated_text"]
            return result

        except Exception as e:
            print(f"[GPTClient] Fallback model also failed: {e}")
            return "Unable to process your request right now."
