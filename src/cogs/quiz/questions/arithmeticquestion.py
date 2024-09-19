import random

from cogs.quiz.questions.question import Question

OPERATOR = ["+", "-", "x", "/"]

class ArithmeticQuestion(Question):
    async def generate(self):
        self.answer_time = 0
        n_op =  1 #random.randint(1,2)
        op1 = random.choice(OPERATOR)
            
        if n_op == 2:
            op2 = random.choice(OPERATOR)

            bracket_op1 = False
            bracket_op2 = False

            if op1 in ["+", "-"] and op2 in ["x", "/"]:
                bracket_op1 = random.choice([True, False])
            elif op1 in ["x", "/"] and op2 in ["+", "-"]:
                bracket_op2 = random.choice([True, False])
        
        if n_op == 1:
            if op1 == "+":
                x1 = random.randint(100, 500)
                x2 = random.randint(100, 500)
                ans = x1 + x2
                self.answer_time += 6

            elif op1 == "-":
                ans = random.randint(100, 500)
                x2 = random.randint(100, 500)
                x1 = ans + x2
                self.answer_time += 8
            
            elif op1 == "x":
                x1 = random.randint(10, 100)
                x2 = random.randint(3, 9)
                ans = x1 * x2
                self.answer_time += 8
            
            elif op1 == "/":
                ans = random.randint(10, 100)
                x2 = random.randint(3, 9)
                x1 = ans * x2
                self.answer_time += 9
        
        self.correct_answer = ans

        if ans > 20:
            self.wrong_answers = [
                ans + 10,
                ans + random.choice([-10, 0, 10]) + random.randint(1, 9) * random.choice([1, -1]),
                ans - 10
            ]
        else:
            self.wrong_answers = [
                ans + random.randint(-min(ans, 10), -min(ans, 2)),
                ans + random.randint(-1, 1),
                ans + random.randint(2, 10)
            ]
        
        self.question = f"{x1} {op1} {x2} = ..."


    async def generate_old(self):
        if self.difficulty == "hard":
            op = "+"
        else:
            op = random.choice(OPERATOR) 

        if op == "+":
            if self.difficulty == "hard":
                n_min = 50
                n_max = 150
            else:
                n_min = 2
                n_max = 25
            
            num_1 = random.randint(n_min, n_max)
            num_2 = random.randint(n_min, n_max)
            self.correct_answer = num_1 + num_2

            
        elif op == "-":
            num_1 = random.randint(10,25)
            num_2 = random.randint(2, num_1-3)
            self.correct_answer = num_1 - num_2
        
        elif op == "x":
            num_1 = random.randint(2, 9)
            num_2 = random.randint(2, 9)
            self.correct_answer = num_1 * num_2

        self.question = f"{num_1} {op} {num_2} = ..."

        