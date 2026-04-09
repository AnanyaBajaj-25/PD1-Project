import dspy

# Used when we let DSPy handle LLM inputs/outputs
class AnswerQuestion(dspy.Signature):
    question = dspy.InputField(prefix="Question:", format=str)
    info = dspy.InputField(prefix="Wikipedia info:\n", format=str)
    answer = dspy.OutputField(prefix="Answer:", format=str)


class CulturalEtiquette(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Relevant cultural context:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    etiquette = dspy.OutputField(prefix="Cultural Etiquette:", format=str)


class SpiritualSites(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Religion & spiritual highlights:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    sites = dspy.OutputField(prefix="Spiritual Sites:", format=str)


class FestivalsHolidays(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Festival & holiday context:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    festivals = dspy.OutputField(prefix="Festivals & Holidays:", format=str)


class LanguageCommunication(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Language & communication insights:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    guidance_output = dspy.OutputField(prefix="Language & Communication:", format=str)


class FoodDiningNorms(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Cuisine & dining customs:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    dining = dspy.OutputField(prefix="Food & Dining Norms:", format=str)


class HeritageMonuments(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Heritage & landmark information:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    highlights = dspy.OutputField(prefix="Heritage & Monuments:", format=str)


class ConversationStarters(dspy.Signature):
    destination = dspy.InputField(prefix="Destination:", format=str)
    info = dspy.InputField(prefix="Combined cultural insights:\n", format=str)
    guidance = dspy.InputField(prefix="Guidelines:", format=str)
    questions = dspy.OutputField(prefix="Conversation Starters:", format=str)