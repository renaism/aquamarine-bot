import random

from cogs.quiz.questions.animequestion import AnimeQuestion
from jikanpy import AioJikan

class AnimeStudioQuestion(AnimeQuestion):
    async def generate(self):
        # Choose the variation, a=anime->studio, b=studio->anime
        invert = random.choice([True, False])

        # Choose anime from top 1000 popularity ranking
        anime = await self.get_entry()
        anime_studios = [ x["name"] for x in anime["studios"] ]

        if not invert:
            self.question = f"Which animation studio produced \"{anime['title']}\"?"
            self.correct_answer = anime_studios[0]
        else:
            self.question = f"Which anime is produced by {anime_studios[0]}?"
            self.correct_answer = anime["title"]
        
        # Get wrong answers from the recommended anime
        aio_jikan = AioJikan()
        self.wrong_answers = []

        res = await aio_jikan.anime(anime["mal_id"], extension="recommendations")
        anime_recommendations = res["recommendations"]

        i_start, i_end = 0, 10

        while len(self.wrong_answers) < 3 and i_start < len(anime_recommendations):
            anime_rec_slice = anime_recommendations[i_start:i_end]
            random.shuffle(anime_rec_slice)
            j = 0

            while len(self.wrong_answers) < 3 and j < len(anime_rec_slice):
                mal_id = anime_rec_slice[j]["mal_id"]
                rel_anime = await aio_jikan.anime(mal_id)
                rel_anime_studios = [ x["name"] for x in rel_anime["studios"] ]

                if not invert and rel_anime_studios[0] not in anime_studios + self.wrong_answers:
                    self.wrong_answers.append(rel_anime_studios[0])
                
                elif invert and anime_studios[0] not in rel_anime_studios:
                    self.wrong_answers.append(rel_anime["title"])
                
                j += 1
            
            i_start = i_end
            i_end += 10
        
        await aio_jikan.close()

        # If the wrong answers can't be filled by recommended anime alone
        if len(self.wrong_answers) < 3:
            if not invert:
                self.fill_dummy_answers(["Disney", "Pixar", "Nickelodeon"])
            else:
                self.fill_dummy_answers(["Avatar the Legend of Aang", "Dora the Explorer", "Spongebob Squarepants"])
