import random
import discord
import asyncio
from data import update_user_data

class NumGame:

    def __init__(self):
        self.random_number = random.randint(1, 100)
        self.guess = None
        self.attempts = 0
        self.user_wins = 0
        self.user_losses = 0
        self.max_attempts = 0
        self.game_active = True
        self.guessed_numbers = set()
        self.started = False
        self.game_task = None

    async def start_game(self, ctx):
        if not self.started:
            self.guessed_numbers.clear()
            await ctx.send(file=discord.File('numgame/images/logo.jpg'))
            rules = (
                "**🧮 NumGame წესები 🧮**\n"
                "- კომპიუტერი იფიქრებს რიცხვს **1-100მდე**.\n"
                "- **მიზანი არის გამოიცნო კომპიუტერის ჩაფიქრებული რიცხვი** ისე, რომ არ ამოგეწუროს ცდები.\n"
                "- თამაშის დასაწყისში ირჩევ **მარტივ ანდ რთულ** მოუდს.\n"
                "- მარტივ მოუდში გეძლევა 10 ცდა, ხოლო რთულში 5.\n"
                "- თუ ცდების დასრულებამდე მოახერხებ გამოცნობას მოიგებ.\n"
            )
            await ctx.send(rules)
            self.started = True

        msg = await ctx.send("გამოხატე რეაქცია ✅ მარტივი მოუდისთვის ან ❌ რთულისთვის.")
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['✅', '❌']

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=30.0)
            if str(reaction.emoji) == '✅':
                self.max_attempts = 10
            elif str(reaction.emoji) == '❌':
                self.max_attempts = 5

            self.attempts = self.max_attempts
            self.game_task = asyncio.create_task(self.is_num(ctx))  

        except asyncio.TimeoutError:
            await ctx.send("დიდი ხანი დაგჭირდა! 😬 ცადე თავიდან.")

    async def is_num(self, ctx):
        while self.attempts > 0 and self.guess != self.random_number and self.game_active:
            await ctx.send(f"გამოიცანი (შენ გაქვს {self.attempts} ცდა დარჩენილი): 🧠 დაწერე რიცხვი 1-100 მდე.")

            def check(msg):
                return msg.author == ctx.author

            try:
                msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)

                if msg.content != "!stop":
                    if msg.content.isdigit() and int(msg.content) <= 100:
                        self.guess = int(msg.content)

                        if self.guess in self.guessed_numbers:
                            await ctx.send(f"❌ ეს რიცხვი უკვე გამოიყენე! სცადე ახალი რიცხვი.")
                        else:
                            self.guessed_numbers.add(self.guess)
                            if self.attempts > 1:
                                if self.guess == self.random_number:
                                    self.user_wins += 1
                                    await ctx.send(f"🎉 გილოცავ, შენ გამოიცანი რიცხვი! პასუხი იყო {self.random_number}. 🎊")
                                    await self.end_game(ctx)
                                    break
                                elif self.guess > self.random_number:
                                    self.attempts -= 1
                                    await ctx.send(f"ზედმეტად მაღალია! ცადე თავიდან. 🔺 ")
                                else:
                                    self.attempts -= 1
                                    await ctx.send(f"ზედმეტად დაბალია! ცადე თავიდან. 🔻 ")
                            else:
                                if self.guess == self.random_number:
                                    self.user_wins += 1
                                    await ctx.send(f"🎉 გილოცავ, შენ გამოიცანი რიცხვი! პასუხი იყო {self.random_number}. 🎊")
                                    await self.end_game(ctx)
                                    break
                                elif self.guess > self.random_number:
                                    self.attempts -= 1
                                    
                                else:
                                    self.attempts -= 1
                                    
                    else:
                        await ctx.send("❌ მხოლოდ რიცხვები შეგიძლია გამოიყენო 1-100მდე! 🧮")
                else:
                    self.game_active = False
                    
            except asyncio.TimeoutError:
                await ctx.send("⏰ დრო ამოიწურა! თამაში დასრულებულია.")
                self.game_active = False
                await self.end_game(ctx)
                break

        if self.guess != self.random_number and self.attempts == 0:
            self.user_losses += 1
            await ctx.send(f"😞 შენ ამოგეწურა ცდები! სწორი პასუხი იყო {self.random_number}.")
            await self.end_game(ctx)

   

    

    async def ask_play_again(self, ctx):
        msg = await ctx.send("გინდა თავიდან თამაში? 🔁\nგამოხატე რეაქცია 🔄 სათამაშოდ ან ❌ შესაწყვეტად.")
        await msg.add_reaction('🔄')
        await msg.add_reaction('❌')

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['🔄', '❌']

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=60.0)
            if str(reaction.emoji) == '🔄':
                await self.start_game(ctx)
            else:
                await ctx.send("მადლობა რომ თამაშობ! 🎮 ვიმედოვნებ მალე შევხვდებით. 👋")
                self.game_active = False

        except asyncio.TimeoutError:
            await ctx.send("⏰ დრო ამოიწურა! მადლობა რომ თამაშობ! 👋")
            self.game_active = False
        
    async def end_game(self, ctx):
        user_id = str(ctx.author.id)
        game_name = "NumGame"
        result = "win" if self.user_wins > self.user_losses else "lose"
        update_user_data(user_id, game_name, result) 
        await self.ask_play_again(ctx)
