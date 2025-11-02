import dspy
from signature import AnswerQuestion
import wikipedia

class WikipediaAgent(dspy.Module):
    def __init__(self):
      super().__init__()

    def retreive_info(self, question):
        results = wikipedia.search(question, results =3)
        summaries = []
        for result in results:
            try:
                summaries.append(wikipedia.summary(result, sentences = 3))
            except Exception:
                continue
        return "\n".join(summaries)

    def forward(self, question: str):
        info = self.retreive_info(question)
        return info



