import dspy

#used later when we let DSPy handle LLM inputs/outputs
class AnswerQuestion(dspy.Signature):
    question = dspy.InputField(prefix="Question:", format = str)
    info = dspy.InputField(prefix= "Wikipedia info:\n", format = str)
    answer = dspy.OutputField(prefix = "Answer:", format = str)