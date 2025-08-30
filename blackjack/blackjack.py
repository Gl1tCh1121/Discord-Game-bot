import discord
import random
import asyncio
from data import update_user_data
from discord.ext import tasks


class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()

    def create_deck(self):
        return [2, 3, 4, 5, 6, 7, 8, 9,10, 11, 'jack', 'queen', 'king'] * 4

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.cards = self.create_deck()
            self.shuffle()
        return self.cards.pop()


class BlackjackGame:
    def __init__(self):
        self.deck = Deck()
        self.reset_game()

    def reset_game(self):
        self.pc_hand = []
        self.user_hand = []
        self.pc_hand_sum = 0
        self.user_hand_sum = 0
        self.user_wins = 0
        self.user_losses = 0
        self.game_active = True

    def add_card(self, hand):
        card = self.deck.draw_card()
        hand.append(card)

        if card in ['jack', 'queen', 'king']:
            return 10

        elif card == 11:
            return 11  

        return card  

    def calculate_hand_sum(self, hand):
        total = 0
        ace_count = 0

        for card in hand:
            if card in ['jack', 'queen', 'king']:
                total += 10
            elif card == 11:  
                total += 11
                ace_count += 1
            else:
                total += card

        while total > 21 and ace_count:
            total -= 10  
            ace_count -= 1

        return total

    def get_card_image_name(self, card):
        return card if isinstance(card, str) else str(card)

    async def start_game(self, ctx):
        self.reset_game()
        await ctx.send(file=discord.File('blackjack/images/logo.jpg'))
        await asyncio.sleep(1)  # Small delay

        rules = (
            "**🎲 Blackjack წესები 🎲**\n"
            "- **მიზანი არის მიაღწიო 21 ქულას** ისე, რომ არ გადაცდე.\n"
            "- თამაშის დასაწყისში მოგცემთ **ორი ქარდი**.\n"
            "- შეგიძლია აირჩიო **'Hit'** (ქარდის დამატება) ან **'Stand'** (დასრულება).\n"
            "- თუ **21 ქულაზე მეტს დააგროვებთ**, წააგებთ.\n"
            "- დილერი უნდა **აიღოს ქარდი მინიმუმ 17 ქულამდე**.\n"
            "- თამაშის ბოლოს **უმაღლესი ქულა იგებს**.\n\n"
            "**მზად ხარ დასაწყებად?** გამოხატე რეაქცია '✅' რომ ითამაშო ან '❌' რომ შეწყვიტო."
        )
        await ctx.send(rules)
        await asyncio.sleep(1)  # Small delay

        msg = await ctx.send("👉", embed=discord.Embed(description="✅ - მზად ვარ\n❌ - არ ვარ მზად"))
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['✅', '❌']

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=60.0)
            if str(reaction.emoji) == '❌':
                await ctx.send("თამაში დასრულდა. 🎮")
                return
        except asyncio.TimeoutError:
            await ctx.send("დრო გაგივიდა! თამაში დასრულებულია.")
            return

        await self.play_round(ctx)

    async def play_round(self, ctx):
        for _ in range(2):
            self.user_hand_sum += self.add_card(self.user_hand)
            self.pc_hand_sum += self.add_card(self.pc_hand)

        self.user_hand_sum = self.calculate_hand_sum(self.user_hand)
        self.pc_hand_sum = self.calculate_hand_sum(self.pc_hand)

        await self.show_user_hand(ctx)
        await self.show_dealer_card(ctx)
        await asyncio.sleep(1)  # Small delay

        await self.player_turn(ctx)

    async def show_user_hand(self, ctx):
        await ctx.send("**შენი ქარდებია:**")
        for card in self.user_hand:
            await ctx.send(file=discord.File(f'blackjack/images/{self.get_card_image_name(card)}.png'))
            await asyncio.sleep(1)  # Small delay

    async def show_dealer_card(self, ctx):
        await ctx.send("**დილერის ქარდი:**")
        await ctx.send(file=discord.File(f'blackjack/images/{self.get_card_image_name(self.pc_hand[0])}.png'))
        await asyncio.sleep(1)  # Small delay

    async def player_turn(self, ctx):
        while  self.game_active:
            if await self.check_game_over(ctx):
                break

            msg = await ctx.send(embed=discord.Embed(description="🃏 - აიღე ქარდი\n✋ - ადექი"))
            await msg.add_reaction("🃏")
            await msg.add_reaction("✋")

            def check(reaction, user):
                return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['🃏', '✋']

            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=60.0)
                if str(reaction.emoji) == '🃏':
                    self.user_hand_sum += self.add_card(self.user_hand)
                    self.user_hand_sum = self.calculate_hand_sum(self.user_hand)

                    last_card = self.user_hand[-1]
                    await ctx.send(f'**შენი ქარდია:  **')
                    await ctx.send(file=discord.File(f'blackjack/images/{self.get_card_image_name(last_card)}.png'))
                    await ctx.send(f'**ქულების რაოდენობა: {self.user_hand_sum}**')
                    await asyncio.sleep(1)  # Small delay

                elif str(reaction.emoji) == '✋':
                    await self.dealer_turn(ctx)
                    break
            except asyncio.TimeoutError:
                await ctx.send("დრო გაგივიდა! თამაში დასრულებულია.")
                self.user_losses += 1
                self.game_active = False
                break

    async def dealer_turn(self, ctx):
        while self.pc_hand_sum < 17:
            self.pc_hand_sum += self.add_card(self.pc_hand)
            self.pc_hand_sum = self.calculate_hand_sum(self.pc_hand)

            if await self.check_game_over(ctx):
                return
        await self.check_winner(ctx)
    async def dealer_turn2(self, ctx):
        while self.pc_hand_sum < 17:
            self.pc_hand_sum += self.add_card(self.pc_hand)
            self.pc_hand_sum = self.calculate_hand_sum(self.pc_hand)

    async def check_game_over(self, ctx):
        if self.user_hand_sum == 21 and self.pc_hand_sum == 21:
            await ctx.send("🤝 ფრეა! 🤝!  ორივეს გაქვთ 21 ქულა!")
            await self.end_game(ctx)
            await self.show_dealer_hand(ctx)
            await self.ask_play_again(ctx)
        elif self.user_hand_sum == 21:
            await self.dealer_turn2(ctx)
            if self.pc_hand_sum == 21:
                await self.check_game_over(ctx)
            else:   
                await ctx.send("🎉** BLACKJACK! **🎉 შენ მოიგე!")
                self.user_wins += 1
                await self.end_game(ctx)
                await self.show_dealer_hand(ctx)
                await self.ask_play_again(ctx)
                return True
        elif self.user_hand_sum > 21:
            self.user_losses += 1
            await ctx.send("😞 შენ გაქვს 21-ზე მეტი ქულა, წააგე! 😞")
            await self.end_game(ctx)
            await self.ask_play_again(ctx)
            return True

        elif self.pc_hand_sum == 21:
            await ctx.send("**BLACKJACK!**  წააგე დილერს აქვს 21 ქულა!")
            self.user_losses += 1
            await self.end_game(ctx)
            await self.show_dealer_hand(ctx)
            await self.ask_play_again(ctx)
            return True
        return False

    async def check_winner(self, ctx):
        await self.show_dealer_hand(ctx)

        if self.pc_hand_sum > 21 or self.user_hand_sum > self.pc_hand_sum and self.user_hand_sum <22:
            self.user_wins += 1
            await ctx.send("🎉 შენ მოიგე! 🎉")
        elif self.user_hand_sum < self.pc_hand_sum <= 21:
            self.user_losses += 1
            await ctx.send("😞 წააგე! 😞")
        else:
            await ctx.send("🤝 ფრეა! 🤝")
            
        await self.end_game(ctx)
        await self.ask_play_again(ctx)
        
    async def show_dealer_hand(self, ctx):
        await ctx.send("**დილერის ქარდებია:**")
        for i, card in enumerate(self.pc_hand):
            if i == 0:
                continue
            await ctx.send(file=discord.File(f'blackjack/images/{self.get_card_image_name(card)}.png'))
            await asyncio.sleep(1)
            
        await ctx.send(f"დილერის ქარდების ჯამი: {self.pc_hand_sum}")

    async def ask_play_again(self, ctx):
        msg = await ctx.send("გინდა ისევ თამაში? გამოხატე რეაქცია '🔁' რომ ითამაშო ან '❌' რომ შეწყვიტო.")
        await msg.add_reaction("🔁")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id and str(reaction.emoji) in ['🔁', '❌']

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check, timeout=60.0)
            if str(reaction.emoji) == '🔁':
                self.reset_game()
                await self.play_round(ctx)
            else:
                await ctx.send("მადლობა თამაშისთვის! 🎮")
                self.game_active = False
        except asyncio.TimeoutError:
            await ctx.send("დრო გაგივიდა! თამაში დასრულებულია.")
            self.game_active = False


    async def end_game(self, ctx):
        user_id = str(ctx.author.id)
        game_name = "blackjack"
        if self.user_wins > self.user_losses:
            result = "win" 
        elif self.user_wins == self.user_losses:
            result = "tie" 
        else:
            result = "lose"
        update_user_data(user_id, game_name, result) 
