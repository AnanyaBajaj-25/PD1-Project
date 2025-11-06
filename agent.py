import dspy
from signature import AnswerQuestion
import wikipedia
from config import lm 

class WikipediaAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.answerer = dspy.Predict(AnswerQuestion)
        
    def retrieve_info(self, question):
        try:
            results = wikipedia.search(question, results=3)
            summaries = []
            for title in results:
                try:
                    summaries.append(wikipedia.summary(title, sentences=3))
                except Exception:
                    continue
            return "\n".join(summaries) or "No relevant information found."
        except Exception:
            return "Error retrieving information."

    def forward(self, question: str):
        info = self.retrieve_info(question)
        with dspy.settings.context(lm=lm):
            response = self.answerer(question=question, info=info)
        return response.answer