import random

class Question():
    def __init__(self, diff="normal"):
        self.difficulty = diff
        self.question = ""
        self.correct_answer = ""
        self.wrong_answers = ["", "", ""]
        self.answer_time = 5


    async def generate(self):
        pass
    

    def fill_dummy_answers(self, dummy_answers):
        random.shuffle(dummy_answers)

        while len(self.wrong_answers) < 3:
            self.wrong_answers.append(dummy_answers.pop(0))
