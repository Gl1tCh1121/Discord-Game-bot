import discord
import random
import asyncio
from data import update_user_data

georgian_alphabet = set('აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ')
english_alphabet = set('abcdefghijklmnopqrstuvwxyz')


class HangmanGame:
    def __init__(self, word_list, lang="en"):
        self.word_list = word_list
        self.lang = lang
        self.chosen_word = ""
        self.display = []
        self.lives = 6
        self.used_letters = []
        self.stop_flag = False
        self.wins = 0
        self.losses = 0
        self.first_game = True

    def get_text(self, en_text, ge_text):
        return en_text if self.lang == "en" else ge_text

    def get_alphabet(self):
        return english_alphabet if self.lang == "en" else georgian_alphabet

    @staticmethod
    def is_valid_letter(letter, lang):
        if lang == "ka":
            return letter in georgian_alphabet
        return letter in english_alphabet

    async def start_game(self, ctx):
        if self.first_game:
            await self.show_intro(ctx)
            self.first_game = False

        while not self.stop_flag:
            self.reset_game()
            self.chosen_word = random.choice(self.word_list[self.lang])
            self.display = ["🗶"] * len(self.chosen_word)
            self.lives = 6
            self.used_letters = []

            await ctx.send(self.get_text(
                f"🔍 **The word has {len(self.chosen_word)} letters!**",
                f"🔍 **სიტყვა შედგება {len(self.chosen_word)} ასობგერისგან!**"
            ))
            await ctx.send(" ".join(self.display))

            while "🗶" in self.display and self.lives > 0:
                if self.stop_flag:
                    await ctx.send(self.get_text(
                        "⛔ Game stopped! 😅",
                        "⛔ თამაში შეწყდა! 😅"
                    ))
                    return

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                await ctx.send(self.get_text(
                    "\n✍️ **Type a letter or guess the word:**",
                    "\n✍️ **დაწერე ასობგერა ან სიტყვა:**"
                ))
                try:
                    guess_msg = await ctx.bot.wait_for('message', check=check, timeout=120)
                    guess = guess_msg.content.lower()
                except asyncio.TimeoutError:
                    if not self.stop_flag:
                        await ctx.send(self.get_text(
                            "⌛ **Time’s up, thanks for playing!**",
                            "⌛ **დრო ამოგეწურა, მადლობა თამაშისთვის! **"
                        ))
                        self.stop_flag = True
                    return

                if self.stop_flag:
                    return

                if guess == self.chosen_word:
                    self.wins += 1
                    await ctx.send(self.get_text(
                        f"🎉 **Congrats😃! You won!** The word was: **{self.chosen_word}**",
                        f"🎉 **გილოცავ😃! შენ მოიგე!** სიტყვა იყო: **{self.chosen_word}**"
                    ))
                    await ctx.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHlsOXF5c2doMnd6MW90bTRsZmQwemEybDEycmZjNzkzcnowem1qdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t3sZxY5zS5B0z5zMIz/giphy-downsized-large.gif")
                    await self.end_game(ctx, "win")
                    break

                if len(guess) != 1 or not HangmanGame.is_valid_letter(guess, self.lang):
                    await ctx.send(self.get_text(
                        "⚠️ **Please enter only 1 English letter, or the full word**",
                        "⚠️ **დაწერე მარტო 1 ასო ქართული ანბანიდან, ან მთლიანი სიტყვა**"
                    ))
                    continue

                if guess in self.used_letters:
                    if not self.stop_flag:
                        await ctx.send(self.get_text(
                            f"♻️ **You already tried this letter!**",
                            f"♻️ **ეს ასობგერა უკვე გამოყენებულია!**"
                        ))
                    continue

                self.used_letters.append(guess)
                if guess in self.chosen_word:
                    for index, letter in enumerate(self.chosen_word):
                        if letter == guess:
                            self.display[index] = letter
                    if not self.stop_flag:
                        await ctx.send(self.get_text(
                            f"✅ **Correct!** {''.join(self.display)}",
                            f"✅ **სწორია!** {''.join(self.display)}"
                        ))
                else:
                    self.lives -= 1
                    try:
                        if not self.stop_flag:
                            await ctx.send(file=discord.File(f'hangman/hangman_images/{self.lives}.png'))
                            await ctx.send(self.get_text(
                                f"❌ **Wrong!** You have **{self.lives}** lives left.",
                                f"❌ **არასწორია!** დარჩენილი გაქვს **{self.lives}** სიცოცხლე."
                            ))
                    except Exception as e:
                        await ctx.send(f"Image load failed: {e}")

                if self.lives == 0 and not self.stop_flag:
                    self.losses += 1
                    await ctx.send(self.get_text(
                        f"😢 **You lost!** The word was: **{self.chosen_word}**.",
                        f"😢 **წააგე!** სიტყვა იყო: **{self.chosen_word}**."
                    ))
                    await self.end_game(ctx, "lose")
                    break

                elif "🗶" not in self.display and not self.stop_flag:
                    self.wins += 1
                    await ctx.send(self.get_text(
                        f"🎉 **Congrats😃! You won!** The word was: **{self.chosen_word}**",
                        f"🎉 **გილოცავ😃! შენ მოიგე!** სიტყვა იყო: **{self.chosen_word}**"
                    ))
                    await ctx.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHlsOXF5c2doMnd6MW90bTRsZmQwemEybDEycmZjNzkzcnowem1qdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t3sZxY5zS5B0z5zMIz/giphy-downsized-large.gif")
                    await self.end_game(ctx, "win")
                    break

            await self.ask_play_again(ctx)

    async def end_game(self, ctx, result):
        user_id = str(ctx.author.id)
        game_name = "hangman"
        update_user_data(user_id, game_name, result)
        await ctx.send(self.get_text(
            "🎉 **Congrats, you won Hangman!**" if result == "win" else "😢 **You lost Hangman!**",
            "🎉 **გილოცავ, შენ მოიგე Hangman!**" if result == "win" else "😢 **წააგე Hangman!**"
        ))

    def reset_game(self):
        self.chosen_word = ""
        self.display = []
        self.lives = 6
        self.used_letters = []
        self.stop_flag = False

    async def show_intro(self, ctx):
        try:
            await ctx.send(file=discord.File('hangman/hangman_images/logo.jpeg'))
        except Exception as e:
            await ctx.send(f"Image load failed: {e}")

        rules_message = self.get_text(
            "🎮 **Hangman Rules:**\n"
            "🔹 A **random word** will be chosen.\n"
            "🔹 Guess **1 letter** or the full word.\n"
            "🔹 You have **6 lives**. Each wrong letter costs one.\n"
            "🔹 If you guess the word, you **win!**\n"
            "✨ **Have fun!** 😍",
            "🎮 **Hangman წესები:**\n"
            "🔹 **რენდომული სიტყვა** იქნება არჩეული.\n"
            "🔹 უნდა გამოიცნო **1 ასობგერა** ან მთლიანი სიტყვა.\n"
            "🔹 გაქვს **6 სიცოცხლე**. თითო არასწორ ასობგერაზე დაკარგავ ერთს.\n"
            "🔹 გამოცნობის შემთხვევაში **მოიგებ!**\n"
            "✨ **იმხიარულე!** 😍"
        )
        await ctx.send(rules_message)

    async def ask_play_again(self, ctx):
        msg = await ctx.send(self.get_text(
            "🔁 **Play again?** \nReact '🔁' to play or '❌' to quit.",
            "🔁 **გინდა ისევ თამაში?** \nდაწერე რეაქცია '🔁' რომ ითამაშო ან '❌' რომ შეწყვიტო."
        ))
        await msg.add_reaction("🔁")
        await msg.add_reaction("❌")

        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["🔁", "❌"]

        try:
            reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=check_reaction)
            if str(reaction.emoji) == "🔁":
                await ctx.send(self.get_text(
                    "🎮 **Great, let’s start again!**",
                    "🎮 **ძალიან კარგი, დავიწყოთ თავიდან!**"
                ))
                await self.start_game(ctx)
            else:
                await ctx.send(self.get_text(
                    "🙏 **Thanks for playing, see you!**",
                    "🙏 **მადლობა თამაშისთვის, შეხვედრამდე!**"
                ))
                self.stop_flag = True
        except asyncio.TimeoutError:
            await ctx.send(self.get_text(
                "⌛ **Time’s up, thanks for playing!**",
                "⌛ **დრო ამოიწურა, მადლობა თამაშისთვის!**"
            ))
            self.stop_flag = True
