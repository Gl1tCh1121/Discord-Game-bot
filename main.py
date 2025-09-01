import discord
from discord.ext import commands
from hangman.Hangman_words import word_list
from blackjack.blackjack import BlackjackGame
from hangman.hangman_game import HangmanGame
from data import get_user_data
from numgame.numgame import NumGame
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

active_games = {}
session_languages = {}  


def get_text(ctx, en_text, ge_text):
    lang = session_languages.get(ctx.channel.id, "en")
    return en_text if lang == "en" else ge_text


async def ask_language(ctx):
    """Ask the user to choose a language if not already set."""
    msg = await ctx.send(
        "**Choose language / აირჩიე ენა:**\n"
        "🇬🇧 English\n"
        "🇬🇪 ქართული"
    )
    await msg.add_reaction("🇬🇧")
    await msg.add_reaction("🇬🇪")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🇬🇧", "🇬🇪"] and reaction.message.id == msg.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        if str(reaction.emoji) == "🇬🇧":
            session_languages[ctx.channel.id] = "en"
            await ctx.send("Hello! 😍 I am Games Bot. To start a game, type `!start`. For commands, type `!command`.")
        else:
            session_languages[ctx.channel.id] = "ge"
            await ctx.send('**გამარჯობა😍მე ვარ Games bot, თამაშის დასაწყებად ჩაწერე "!start" მოდი ვითამაშოთ (დამატებითი ინფორმაციის მისაღებად დაწერეთ "!command")**')
    except asyncio.TimeoutError:
        await ctx.send("No reaction chosen. Defaulting to English.")
        session_languages[ctx.channel.id] = "en"


@bot.before_invoke
async def ensure_language(ctx):
    if ctx.channel.id not in session_languages:
        await ask_language(ctx)


@bot.command()
async def start(ctx):
    message = get_text(
        ctx,
        "**Available games:**\n!hangman - Start Hangman\n!blackjack - Start Blackjack\n!numgame - Start NumGame\n\n**Rules:**\n1. Start a game using a command.\n2. Collect GC (game coins).\n3. Have fun.\n4. Later, exchange GC for rewards.\n5. Blackjack win = 3 GC, other wins = 1 GC.",
        "**ხელმისაწვდომი თამაშები:**\n!hangman - დაიწყოს თამაში Hangman.\n!blackjack - დაიწყოს თამაში Blackjack.\n!numgame - დაიწყოს თამაში NumGame.\n\n**მოკლე წესები:**\n1. ჩართე თამაში კომანდის გამოძახებით.\n2. დააგროვე GC (game coin).\n3. გართობა.\n4. მოგვიანებით გადაცვალე GC პრიზებში.\n5. BlackJack მოგება = 3 GC, დანარჩენი თამაშები = 1 GC."
    )
    await ctx.send(message)


@bot.command()
async def hangman(ctx):
    if ctx.channel.id in active_games:
        await ctx.send(get_text(ctx, "A game is already running.", "თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში."))
        return

    game = HangmanGame(word_list, lang=session_languages.get(ctx.channel.id, "en"))
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if getattr(game, "stop_flag", False) or "🗶" not in getattr(game, "display", "") or getattr(game, "lives", 0) == 0:
        del active_games[ctx.channel.id]


@bot.command()
async def blackjack(ctx):
    if ctx.channel.id in active_games:
        await ctx.send(get_text(ctx, "A game is already running.", "თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში."))
        return

    game = BlackjackGame(lang=session_languages.get(ctx.channel.id, "en"))
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if not getattr(game, "game_active", True):
        del active_games[ctx.channel.id]


@bot.command()
async def numgame(ctx):
    if ctx.channel.id in active_games:
        await ctx.send(get_text(ctx, "A game is already running.", "თამაში უკვე მიმდინარეობს. ჯერ დაასრულეთ ის თამაში."))
        return

    game = NumGame(lang=session_languages.get(ctx.channel.id, "en"))
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if not getattr(game, "game_active", True):
        del active_games[ctx.channel.id]


@bot.command()
async def stop(ctx):
    if ctx.channel.id in active_games:
        game = active_games[ctx.channel.id]
        if hasattr(game, 'stop_game'):
            game.stop_game()
        await ctx.send(get_text(ctx, "Game stopped... 😶", "თამაში შეწყდა... 😶"))
        del active_games[ctx.channel.id]
    else:
        await ctx.send(get_text(ctx, "You are not in any game!", "ამჟამად არცერთ თამაშში არ იმყოფებით!"))


@bot.command()
async def command(ctx):
    help_message = get_text(
        ctx,
        "**Available commands:**\n!start - Get game info.\n!hangman - Start Hangman.\n!blackjack - Start Blackjack.\n!numgame - Start NumGame.\n!stop - Stop a game.\n!command - Show this message.\n!info - Show your stats.",
        "**ხელმისაწვდომი command:**\n!start - თამაშის გასაცნობად.\n!hangman - დაიწყოს თამაში Hangman.\n!blackjack - დაიწყოს თამაში Blackjack.\n!numgame - დაიწყოს თამაში NumGame.\n!stop - თამაშის შესაწყვეტად.\n!command - ამ მესიჯის საჩვენებლად.\n!info - რომ მიიღოთ ინფორმაცია თქვენს შესახებ."
    )
    await ctx.send(help_message)


@bot.command()
async def info(ctx):
    user_id = str(ctx.author.id)
    user_info = get_user_data(user_id)
    
    totalgp = user_info["gamesplayed"]
    gc = user_info["gamecoins"]
    wins = user_info["wins"]
    losses = user_info["losses"]
    games = user_info["games"]

    stats_message = get_text(
        ctx,
        f"🪙 **Game coins: {gc}**\n🏆 **Wins: {wins} || Losses: {losses}**\n🎮 **Total games: {totalgp}**\n🕹️ **Game details:**\n",
        f"🪙 **Game coins: {gc}**\n🏆 **მოგებები: {wins}   ||   წაგებები: {losses}**\n🎮 **თამაშების რაოდენობა: {totalgp}**\n🕹️ **თამაში შედეგების:**\n"
    )
    
    for game_name, result in games.items():
        stats_message += get_text(
            ctx,
            f"Game: **{game_name.capitalize()}** - Wins: {result['wins']}, Losses: {result['losses']}, Games played: {result['gamesplayed']}\n",
            f"თამაში: **{game_name.capitalize()}** - მოგება: {result['wins']}, წაგება: {result['losses']}, თამაშების რაოდენობა: {result['gamesplayed']}\n"
        )

    await ctx.send(stats_message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(get_text(ctx, "❌ Command not found! Try: `!command`", "❌ ესეთი კომანდი არ არსებობს! სცადე: `!command`"))
        await command(ctx)


bot.run('YOURDISCORDTOKEN')
