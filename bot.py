import discord
import sys
from scraper import Chapter


class MyClient(discord.Client):
    def __init__(self, user_id: int, message: str, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.message = message

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        user = await self.fetch_user(self.user_id)
        await user.send(self.message,suppress_embeds=None)
        await self.close() 


def build_message() -> str | None:
    latest: list[Chapter] = Chapter.fetchLastedChapters()
    last_found: Chapter = Chapter.readFromJson("lastestChapter.json")
    latest.sort()
    print(latest[3].writeToJson("test.json"))
    chapters_not_read = [chapter for chapter in latest if (chapter > last_found)]

    if not chapters_not_read:
        return None

    message = f"There have been {len(chapters_not_read)} new chapters posted\n"

    for chapter in chapters_not_read:
        message += f"- Chapter Name: {chapter.chapterName}\n"
        message += f"  Link: <{chapter.link}>\n"
    chapters_not_read[0].writeToJson("lastestChapter.json")
    return message


def main():
    user_id = int(sys.argv[1])
    bot_token = sys.argv[2]

    message = build_message()
    if message is None:
        return  # nothing to send

    intents = discord.Intents.default()
    client = MyClient(user_id=user_id, message=message, intents=intents)
    client.run(bot_token)



if __name__ == "__main__":
    main()