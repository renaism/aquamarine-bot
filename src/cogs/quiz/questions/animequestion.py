import random

from cogs.quiz.questions.question import Question
from jikanpy import AioJikan

class AnimeQuestion(Question):
    async def get_entry(self, type_="anime", page_min=1, page_max=10, subtype="bypopularity"):
        aio_jikan = AioJikan()

        page = random.randint(page_min, page_max)
        res = await aio_jikan.top(type=type_, page=page, subtype=subtype)
        mal_id = res["top"][random.randint(0, 49)]["mal_id"]
        anime = await aio_jikan.anime(mal_id)

        await aio_jikan.close()

        return anime