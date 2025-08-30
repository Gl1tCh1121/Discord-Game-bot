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
        await ctx.send("A game is already running. Please finish it first.")
        return

    game = HangmanGame(word_list)
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.stop_flag or "🗶" not in game.display or game.lives == 0:
        del active_games[ctx.channel.id]

@bot.command()
async def blackjack(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("A game is already running. Please finish it first.")
        return

    game = BlackjackGame()
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.game_active == False:
        del active_games[ctx.channel.id]

@bot.command()
async def numgame(ctx):
    if ctx.channel.id in active_games:
        await ctx.send("A game is already running. Please finish it first.")
        return

    game = NumGame()
    active_games[ctx.channel.id] = game
    await game.start_game(ctx)

    if game.game_active == False:
        del active_games[ctx.channel.id]

@bot.command()
async def info(ctx):
    user_id = str(ctx.author.id)
    user_info = get_user_data(user_id)
    
    totalgp = user_info["gamesplayed"]
    gc = user_info["gamecoins"]
    wins = user_info["wins"]
    losses = user_info["losses"]
    games = user_info["games"]
    
    stats_message = f"🪙 **Game coins:   {gc}** \n"
    "\n"
    stats_message += f"🏆 **Wins: {wins}   ||   Losses: {losses}**\n"
    stats_message += f"🎮 **Total games played:  {totalgp}**\n"
    "\n"
    stats_message += "🕹️ **Game results:**\n"
    
    for game_name, result in games.items():
        stats_message += f"Game: **{game_name.capitalize()}** - Wins: {result['wins']},    Losses: {result['losses']},   Games played: {result['gamesplayed']}\n"
    
    await ctx.send(stats_message)

@bot.command()
async def hello(ctx):
    await ctx.send('**Hello 😍 I am Games Bot. To start a game, type "!start". Let’s play! (For more info type "!commands")**\n')

@bot.command()
async def start(ctx):
    message = (
        "**Available games:**\n"
        "!hangman - Start Hangman.\n"
        "!blackjack - Start Blackjack.\n"
        "!numgame - Start NumGame.\n"
        "\n"
        "**Quick rules:**\n"
        "1. Start a game with the command.\n"
        "2. Collect GC (game coins).\n"
        "3. Have fun.\n"
        "4. Later, exchange GC for cool rewards.\n"
        "5. Winning Blackjack gives you +3 GC, other games +1 GC.\n"
    )
    await ctx.send(message)

@bot.command()
async def stop(ctx):
    if ctx.channel.id in active_games:
        game = active_games[ctx.channel.id]
        if hasattr(game, 'stop_game'):
            game.stop_game()
        await ctx.send("Game stopped... 😶")
        del active_games[ctx.channel.id]
    else:
        await ctx.send("You are not in any active game right now!")

@bot.command()
async def commands(ctx):
    help_message = (
        "**Available commands:**\n"
        "!hello - Greet the bot.\n"
        "!start - Learn about the games.\n"
        "!hangman - Start Hangman.\n"
        "!blackjack - Start Blackjack.\n"
        "!numgame - Start NumGame.\n"
        "!stop - Stop the current game.\n"
        "!commands - Show this message.\n"
        "!info - Get your game stats.\n"
    )
    await ctx.send(help_message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ **That command doesn’t exist! Try:** `!commands`")
        help_message = (
        "**Available commands:**\n"
        "!hello - Greet the bot.\n"
        "!start - Learn about the games.\n"
        "!hangman - Start Hangman.\n"
        "!blackjack - Start Blackjack.\n"
        "!numgame - Start NumGame.\n"
        "!stop - Stop the current game.\n"
        "!commands - Show this message.\n"
        "!info - Get your game stats.\n"
        )
        await ctx.send(help_message)
    
bot.run('YOURDISCORDTOKEN')
