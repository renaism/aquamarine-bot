import random

from cogs.quiz.questions.animequestion import AnimeQuestion
from jikanpy import AioJikan

class AnimeVoiceActorQuestion(AnimeQuestion):
    async def generate(self):
        # Normal: Character->VA? | Invert: VA->Character? 
        invert = random.choice([True, False])

        # Choose anime from top 500 popularity ranking
        anime = await self.get_entry(page_max=5)

        aio_jikan = AioJikan()

        res = await aio_jikan.anime(anime["mal_id"], extension="characters_staff")
        
        await aio_jikan.close()

        characters = res["characters"]
        main_characters    = list(filter(lambda x: x["role"] == "Main", characters))
        support_characters = list(filter(lambda x: x["role"] == "Supporting", characters))

        random.shuffle(main_characters)
        character = main_characters.pop()
        character_va = list(filter(lambda x: x["language"] == "Japanese", character["voice_actors"]))[0]

        if not invert:
            self.question = f"Who is the voice actor of {character['name'].replace(',', '')} from \"{anime['title']}\"?"
            self.correct_answer = character_va["name"].replace(",", "")
        else:
            self.question = f"Which character {character_va['name'].replace(',', '')} voiced in \"{anime['title']}\"?"
            self.correct_answer = character["name"].replace(",", "")

        # Choose wrong answers from the VAs of other main characters
        self.wrong_answers = []
        i = 0

        while len(self.wrong_answers) < 3 and i < len(main_characters):
            other_char = main_characters[i]
            other_char_va = list(filter(lambda x: x["language"] == "Japanese", other_char["voice_actors"]))[0]
            
            if other_char_va["mal_id"] == character_va["mal_id"]:
                continue
            
            if not invert:
                self.wrong_answers.append(other_char_va["name"].replace(",", ""))
            else:
                self.wrong_answers.append(other_char["name"].replace(",", ""))
            
            i += 1
        
        # Choose wrong answers from the VAs of supporting characters
        i = 0
        random.shuffle(support_characters)

        while len(self.wrong_answers) < 3 and i < len(support_characters):
            other_char = support_characters[i]
            other_char_va = list(filter(lambda x: x["language"] == "Japanese", other_char["voice_actors"]))[0]
            
            if other_char_va["mal_id"] == character_va["mal_id"]:
                continue
            
            if not invert:
                self.wrong_answers.append(other_char_va["name"].replace(",", ""))
            else:
                self.wrong_answers.append(other_char["name"].replace(",", ""))
            
            i += 1
        
        # If the wrong answers can't be filled by characters from the same anime
        if len(self.wrong_answers) < 3:
            if not invert:
                self.fill_dummy_answers(["Umuzaki Naturo", "Uhicha Sakuse", "Hanuro Saruka"])
            else:
                self.fill_dummy_answers(["Spongebob Squarepants", "Patrick Star", "Squidward Tentacles"])



