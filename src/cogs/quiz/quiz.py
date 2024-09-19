import discord
import random
import asyncio

from discord.ext import commands
from cogs.quiz.questions.arithmeticquestion import ArithmeticQuestion
from cogs.quiz.questions.animestudioquestion import AnimeStudioQuestion
from cogs.quiz.questions.animevoiceactorquestion import AnimeVoiceActorQuestion

CHOICES_EMOJI_UNICODE = {
    "a": "\N{Regional Indicator Symbol Letter A}",
    "b": "\N{Regional Indicator Symbol Letter B}",
    "c": "\N{Regional Indicator Symbol Letter C}",
    "d": "\N{Regional Indicator Symbol Letter D}"
}

CHOICES_EMOJI_UNICODE_INV = {
    "\N{Regional Indicator Symbol Letter A}" : "a",
    "\N{Regional Indicator Symbol Letter B}" : "b",
    "\N{Regional Indicator Symbol Letter C}" : "c",
    "\N{Regional Indicator Symbol Letter D}" : "d"
}

CHOICES_EMOJI_SHORT = {
    "a": ":regional_indicator_a:",
    "b": ":regional_indicator_b:",
    "c": ":regional_indicator_c:",
    "d": ":regional_indicator_d:"
}

EMBED_COLOR = {
    "default" : 0x3498DB,
    "timeup" : 0xF1C40F,
    "correct": 0x2ECC71,
    "wrong"  : 0xE74C3C
}

class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data
    

    @commands.command(aliases=["q"])
    async def quiz(self, ctx, type_=None, difficulty="normal"):
        if ctx.channel.id in self.data["Quiz"]:
            await ctx.send("Please wait until the previous question is finished!")
            return

        embed = discord.Embed()
        embed.title = "Question"
        embed.colour = EMBED_COLOR["default"]

        type_ = self.infer_type(type_)

        if type_ == "math":
            question = ArithmeticQuestion(difficulty)
        elif type_ == "voiceactor":
            question =  AnimeVoiceActorQuestion()
        elif type_ == "animestudio":
            question = AnimeStudioQuestion()
        
        await question.generate()

        answer_positions = ["a", "b", "c", "d"]
        random.shuffle(answer_positions)
        choices = {}

        # Correct answer is indexed on the first entry of answer_positions
        choices[answer_positions[0]] = question.correct_answer
        
        for i in range(1, len(answer_positions)):
            choices[answer_positions[i]] = question.wrong_answers[i-1]
        
        # Sort the choices alphabetically
        choices = dict(sorted(choices.items()))

        txt = f"{question.question}\n"

        for x in choices:
            txt += f"\n{CHOICES_EMOJI_SHORT[x]} {choices[x]}"

        embed.description = txt

        msg = await ctx.send(embed=embed)

        self.data["Quiz"][ctx.channel.id] = {
            "message": msg,
            "answer": answer_positions[0],
            "answer_txt": choices[answer_positions[0]],
            "user_answers": {}
        }

        for x in choices:
            await msg.add_reaction(emoji=CHOICES_EMOJI_UNICODE[x])
        
        # Check all the answers from the reactions after the quiz duration period
        await asyncio.sleep(question.answer_time + 0.25)
        txt += "\n\n:hourglass: Time is up!"

        user_answers = self.data["Quiz"][ctx.channel.id]["user_answers"]
        n_answer  = len(user_answers)

        if n_answer == 0:
            txt += " No one answered the question :("
            embed.colour = EMBED_COLOR["timeup"]

        else:
            n_correct = 0

            for user_id, answer in user_answers.items():
                if answer == answer_positions[0]:
                    txt += f"\n:white_check_mark: <@{user_id}> answered correctly ({answer.upper()})"
                    n_correct += 1
                else:
                    txt += f"\n:x: <@{user_id}> answered wrongly ({answer.upper()})"
            
            if n_correct > 0:
                embed.colour = EMBED_COLOR["correct"]
            else:
                embed.colour = EMBED_COLOR["wrong"]
        
        embed.description = txt
        
        await msg.clear_reactions()
        await msg.edit(embed=embed)

        self.data["Quiz"].pop(ctx.channel.id)
    

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return

        msg = reaction.message

        if msg.channel.id not in self.data["Quiz"]:
            return
        
        channel_entry = self.data["Quiz"][msg.channel.id]

        if msg.id != channel_entry["message"].id:
            return

        if user.id in channel_entry["user_answers"]:
            return
        
        channel_entry["user_answers"][user.id] = CHOICES_EMOJI_UNICODE_INV[reaction.emoji]
    

    def infer_type(self, type_):
        if type_ in ["math", "m"]:
            return "math"
        elif type_ in ["voiceactor", "voiceactors", "va"]:
            return "voiceactor"
        elif type_ in ["animestudio", "animestudios", "studio", "studios", "st"]:
            return "animestudio"
        else:
            return random.choice(["voiceactor", "animestudio"])