from app.config import settings
from app.services.gpt_client import GPTClient

class Summarizer:
    """
    Summarizes raw PDF content using GPT-4o (Azure) or a fallback LLM.
    Called once per document during PDF preprocessing.
    """
    def __init__(self):
        self.use_azure = True if settings.AZURE_API_KEY else False
        self.client = GPTClient(
            api_key=settings.AZURE_API_KEY,
            endpoint=settings.AZURE_ENDPOINT
        )

    def generate_summary(self, text: str) -> str:
        """
        Given long raw text, return a 4–6 bullet point summary.
        """
        if not text.strip():
            return "No summary available (empty content)."

        prompt = (
            "Summarize the following internal consulting document into 4–6 bullet points. "
            "Focus on key findings, insights, or trends. Keep it clear and executive-friendly.\n\n"
            f"{text[:3000]}"
        )

        try:
            messages = [
                {"role": "system", "content": "You are an expert consultant summarizing strategic reports."},
                {"role": "user", "content": prompt}
            ]
            return self.client.generate_answer(messages)
        except Exception as e:
            print(f"[Summarizer] LLM failed: {e}")
            return "Summary not available due to an internal error."