import dspy

#used later when we let DSPy handle LLM inputs/outputs
class AnswerQuestion(dspy.Signature):
    question = dspy.InputField(prefix="Question:", format = str)
    info = dspy.InputField(prefix= "Wikipedia info:\n", format = str)
    answer = dspy.OutputField(prefix = "Answer:", format = str)


class CulturalEtiquette(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Cultural etiquette tips:", format=str)


class ReligionAndSpiritualSites(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Notable religious or spiritual sites:", format=str)


class FestivalsAndHolidays(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Festivals and holidays to know:", format=str)


class LanguageAndCommunication(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Language and communication tips:", format=str)


class FoodAndDiningNorms(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Food and dining norms:", format=str)


class HeritageAndMonuments(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Wikipedia snippets:\n", format=str)
    answer = dspy.OutputField(prefix="Heritage sites and monuments:", format=str)


class ConversationStarters(dspy.Signature):
    question = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Insights gathered (each line topic: details):\n", format=str)
    answer = dspy.OutputField(prefix="Conversation starters (return 3-5 bullet points, polite and culturally aware):", format=str)

