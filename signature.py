import dspy

class AnswerQuestion(dspy.Signature):
    question = dspy.InputField(prefix="Question:", format = str)
    info = dspy.InputField(prefix= "Wikipedia info:\n", format = str)
    answer = dspy.OutputField(prefix = "Answer:", format = str)