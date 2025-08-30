import discord
import random
import asyncio
from data import update_user_data

georgian_alphabet = set('ა ბ გ დ ე ვ ზ თ ი კ ლ მ ნ ო პ ჟ რ ს ტ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჯ ჰ')


class HangmanGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.chosen_word = ""
        self.display = []
        self.lives = 6
        self.used_letters = []
        self.stop_flag = False
        self.wins = 0
        self.losses = 0
        self.first_game = True

    async def start_game(self, ctx):
        if self.first_game:
            await self.show_intro(ctx)
            self.first_game = False

        while not self.stop_flag:
            self.reset_game()
            self.chosen_word = random.choice(self.word_list)
            self.display = ["🗶"] * len(self.chosen_word)
            self.lives = 6
            self.used_letters = []

            await ctx.send(f"🔍 **სიტყვა შედგება {len(self.chosen_word)} ასობგერისგან!**")
            await ctx.send(" ".join(self.display))

            while "🗶" in self.display and self.lives > 0:
                if self.stop_flag:
                    await ctx.send("⛔ თამაში შეწყდა! 😅")
                    return

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                await ctx.send("\n✍️ **დაწერე ასობგერა:**")
                try:
                    guess_msg = await ctx.bot.wait_for('message', check=check, timeout=120)
                    guess = guess_msg.content.lower()
                except asyncio.TimeoutError:
                    if not self.stop_flag:
                        await ctx.send("⌛ **დრო ამოგეწურა, მადლობა თამაშისთვის! **")
                    return

                if self.stop_flag:
                    return

                if guess == self.chosen_word:
                    self.wins += 1
                    await ctx.send(f"🎉 **გილოცავ😃! შენ მოიგე!** სიტყვა იყო: **{self.chosen_word}**")
                    await ctx.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHlsOXF5c2doMnd6MW90bTRsZmQwemEybDEycmZjNzkzcnowem1qdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t3sZxY5zS5B0z5zMIz/giphy-downsized-large.gif")
                    await self.end_game(ctx, "win")  # Call end_game with result as "win"
                    break

                if len(guess) != 1 or guess not in georgian_alphabet:
                    if not self.stop_flag:
                        await ctx.send("⚠️ **დაწერე მარტო 1 ასო ქართული ანბანიდან, ან მთლიანი სიტყვა**")
                    continue

                if guess in self.used_letters:
                    if not self.stop_flag:
                        await ctx.send(f"♻️ **ეს ასობგერა უკვე გამოყენებულია!**")
                    continue

                self.used_letters.append(guess)
                if guess in self.chosen_word:
                    for index, letter in enumerate(self.chosen_word):
                        if letter == guess:
                            self.display[index] = letter
                    if not self.stop_flag:
                        await ctx.send(f"✅ **სწორია!** {''.join(self.display)}")
                else:
                    self.lives -= 1
                    try:
                        if not self.stop_flag:
                            await ctx.send(file=discord.File(f'hangman/hangman_images/{self.lives}.png'))
                            await ctx.send(f"❌ **არასწორია!** დარჩენილი გაქვს **{self.lives}** სიცოცხლე.")
                    except Exception as e:
                        await ctx.send(f"სურათის ჩატვირთვა ვერ მოხერხდა: {e}")

                if self.lives == 0 and not self.stop_flag:
                    self.losses += 1
                    await ctx.send(f"😢 **წააგე!** სიტყვა იყო: **{self.chosen_word}**.")
                    await self.end_game(ctx, "lose")  # Call end_game with result as "lose"
                    break
                elif "🗶" not in self.display and not self.stop_flag:
                    self.wins += 1
                    await ctx.send(f"🎉 **გილოცავ😃! შენ მოიგე!** სიტყვა იყო: **{self.chosen_word}**")
                    await ctx.send("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHlsOXF5c2doMnd6MW90bTRsZmQwemEybDEycmZjNzkzcnowem1qdiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t3sZxY5zS5B0z5zMIz/giphy-downsized-large.gif")
                    await self.end_game(ctx, "win")  # Call end_game with result as "win"
                    break

            await self.ask_play_again(ctx)

    async def end_game(self, ctx, result):
        user_id = str(ctx.author.id)
        game_name = "hangman"
        update_user_data(user_id, game_name, result)  # Update data

        if result == "win":
            await ctx.send(f"🎉 **გილოცავ, შენ მოიგე Hangman!**")
        else:
            await ctx.send(f"😢 **წააგე Hangman!**")

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
            await ctx.send(f"სურათის ჩატვირთვა ვერ მოხერხდა: {e}")

        rules_message = (
            "🎮 **Hangman წესები:**\n"
            "🔹 **რენდომული სიტყვა** იქნება არჩეული.\n"
            "🔹 უნდა გამოიცნო **1 ასობგერა** ან მთლიანი სიტყვა.\n"
            "🔹 გაქვს **6 სიცოცხლე**. თითო არასწორ ასობგერაზე დაკარგავ ერთს.\n"
            "🔹 გამოცნობის შემთხვევაში **მოიგებ!**\n"
            "✨ **იმხიარულე!** 😍\n"
        )
        await ctx.send(rules_message)

    def reset_game(self):
        self.chosen_word = ""
        self.display = []
        self.lives = 6
        self.used_letters = []
        self.stop_flag = False

    async def ask_play_again(self, ctx):
        msg = await ctx.send("🔁 **გინდა ისევ თამაში?** \nდაწერე რეაქცია '🔁' რომ ითამაშო ან '❌' რომ შეწყვიტო.")
        await msg.add_reaction("🔁")
        await msg.add_reaction("❌")

        def check_reaction(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["🔁", "❌"]

        try:
            reaction, _ = await ctx.bot.wait_for("reaction_add", timeout=60.0, check=check_reaction)
            if str(reaction.emoji) == "🔁":
                await ctx.send("🎮 **ძალიან კარგი, დავიწყოთ თავიდან!**")
                await self.start_game(ctx)  
            else:
                await ctx.send("🙏 **მადლობა თამაშისთვის, შეხვედრამდე!**")
                self.stop_flag = True
        except asyncio.TimeoutError:
            await ctx.send("⌛ **დრო ამოიწურა, მადლობა თამაშისთვის!**")
            self.stop_flag = True  


