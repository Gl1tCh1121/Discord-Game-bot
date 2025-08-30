import discord
from discord.ext import commands
from hangman.Hangman_words import word_list
from blackjack.blackjack import BlackjackGame
from hangman.hangman_game import HangmanGame
from data import get_user_data
from numgame.numgame import NumGame

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


active_games = {}

@bot.command()
async def hangman(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში.")
        return

    game = HangmanGame(word_list)
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.stop_flag or "🗶" not in game.display or game.lives == 0:
        del active_games[ctx.channel.id]

@bot.command()
async def blackjack(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში.")
        return

    game = BlackjackGame()
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.game_active == False:
        del active_games[ctx.channel.id]

@bot.command()
async def numgame(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში.")
        return

    game = NumGame()
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.game_active == False:
        del active_games[ctx.channel.id]

@bot.command()
async def ინფო(ctx):
    user_id = str(ctx.author.id)
    user_info = get_user_data(user_id)
    
    totalgp = user_info["gamesplayed"]
    gc = user_info["gamecoins"]
    wins = user_info["wins"]
    losses = user_info["losses"]
    games = user_info["games"]
    
    stats_message = f"🪙 **Game coins:   {gc}** \n"
    "\n"
    stats_message += f"🏆 **მოგებები: {wins}   ||   წაგებები: {losses}**\n"
    stats_message += f"🎮 **თამაშების რაოდენობა:  {totalgp}**\n"
    "\n"
    stats_message += "🕹️ **თამაში შედეგების:**\n"
    
    for game_name, result in games.items():
        stats_message += f"თამაში: **{game_name.capitalize()}** - მოგება: {result['wins']},    წაგება: {result['losses']},   თამაშების რაოდენობა: {result['gamesplayed']}\n"
    
    await ctx.send(stats_message)

@bot.command()
async def გამარჯობა(ctx):
    await ctx.send('**გამარჯობა😍მე ვარ Games bot, თამაშის დასაწყებად ჩაწერე "!start" მოდი ვითამაშოთ (დამატებითი ინფორმაციის მისაღებად დაწერეთ "!კომანდები")**\n')

@bot.command()
async def start(ctx):
    message = (
        "**ხელმისაწვდომი თამაშები:**\n"
        "!hangman - დაიწყოს თამაში Hangman.\n"
        "!blackjack - დაიწყოს თამაში Blackjack.\n"
        "!numgame - დაიწყოს თამაში NumGame.\n"
        "\n"
        "**მოკლე წესები:**\n"
        "1.ჩართე თამაში კომანდის გამოძახებით.\n"
        "2.დააგროვე GC(game coin).\n"
        "3.გაერთე.\n"
        "4.მოგვიანებით გადაცვალე GC საინტერესო პრიზებში.\n"
        "5.BlackJack მოგების შემთხვევაში დაგერიცხებათ აგარიშზე 3 GC, ხოლო დანარჩენ თამაშებზე 1.\n"
    )
    await ctx.send(message)

@bot.command()
async def stop(ctx):
    if ctx.channel.id in active_games:
        game = active_games[ctx.channel.id]
        if hasattr(game, 'stop_game'):
            game.stop_game()
        await ctx.send("თამაში შეწყდა... 😶")
        del active_games[ctx.channel.id]
    else:
        await ctx.send("ამჟამად არცერთ თამაშში არ იმყოფებით!")

@bot.command()
async def კომანდები(ctx):
    help_message = (
        "**ხელმისაწვდომი კომანდები:**\n"
        "!გამარჯობა - Greet the bot.\n"
        "!start - თამაშის გასაცნობად.\n"
        "!hangman - დაიწყოს თამაში Hangman.\n"
        "!blackjack - დაიწყოს თამაში Blackjack.\n"
        "!numgame - დაიწყოს თამაში NumGame.\n"
        "!stop - თამაშის შესაწყვეტად.\n"
        "!კომანდები - ამ მესიჯის საჩვენებლად.\n"
        "!ინფო - რომ მიიღოთ ინფორმაცია თქვენს შესახებ.\n"
    )
    await ctx.send(help_message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ **ესეთი კომანდი არ არსებობს! სცადე:** `!კომანდები`")
        help_message = (
        "**ხელმისაწვდომი კომანდები:**\n"
        "!გამარჯობა - Greet the bot.\n"
        "!start - თამაშის გასაცნობად.\n"
        "!hangman - დაიწყოს თამაში Hangman.\n"
        "!blackjack - დაიწყოს თამაში Blackjack.\n"
        "!numgame - დაიწყოს თამაში NumGame.\n"
        "!stop - თამაშის შესაწყვეტად.\n"
        "!კომანდები - ამ მესიჯის საჩვენებლად.\n"
        "!ინფო - რომ მიიღოთ ინფორმაცია თქვენს შესახებ.\n"
        )
        await ctx.send(help_message)
    
bot.run('YOURDISCORDTOKEN')