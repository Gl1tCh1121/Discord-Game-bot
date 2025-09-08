<h1 align="center">Discord Games Bot</h1>

<p>
  A fun Discord bot with multiple mini-games, player statistics, and a reward system.<br>
  <br>
  Enjoy playing directly in your Discord server!
</p>

<hr>

<h2> Features</h2>
<ul>
  <li><b>3 Games available:</b>
    <ul>
      <li><b>Hangman</b> – guess the hidden word.</li>
      <li><b>Blackjack</b> – classic card game against th e dealer.</li>
      <li><b>NumGame</b> – guess the number challenge.</li>
    </ul>
  </li>
  <li> <b>Game Coins (GC) for future market:</b>
    <ul>
      <li>+3 GC for winning Blackjack.</li>
      <li>+1 GC for winning other games.</li>
    </ul>
  </li>
  <li> <b>Player stats tracking:</b>
    <ul>
      <li>Wins / Losses</li>
      <li>Total games played</li>
      <li>Game Coins balance</li>
      <li>Per-game statistics</li>
    </ul>
  </li>
  <li> <b>Stop games anytime</b> with <code>!stop</code>.</li>
</ul>

<hr>

<h2>Project Structure</h2>

<pre>
📦 your-bot/
 ┣ 📂 blackjack/      # Blackjack game logic & assets
 ┣ 📂 hangman/        # Hangman game logic & assets
 ┣ 📂 numgame/        # Number guessing game logic
 ┣ 📜 data.py         # Handles user data (wins, losses, coins)
 ┣ 📜 main.py         # Main bot file (commands & game management)
 ┣ 📜 user_data.json  # Stores player stats
 ┣ 📜 README.md       # Project documentation
</pre>

<hr>

<h2> Getting Started</h2>

<h3>1. Clone the repository</h3>

<h3>2. Install dependencies</h3>
<pre><code>pip install discord
</code></pre>

<h3>3. Add your Discord bot token</h3>
<p>Open <code>main.py</code> and replace:</p>
<pre><code>bot.run('YOURDISCORDTOKEN')
</code></pre>
<p>with your actual bot token.</p>

<h3>4. Run the bot</h3>
<pre><code>python main.py
</code></pre>

<hr>

<h2> Commands</h2>

<table>
  <tr><th>Command</th><th>Description</th></tr>
  <tr><td><code>!hello</code></td><td>Greet the bot & choose language</td></tr>
  <tr><td><code>!start</code></td><td>Show available games & rules</td></tr>
  <tr><td><code>!hangman</code></td><td>Start a Hangman game</td></tr>
  <tr><td><code>!blackjack</code></td><td>Start a Blackjack game</td></tr>
  <tr><td><code>!numgame</code></td><td>Start a Number Game</td></tr>
  <tr><td><code>!info</code></td><td>Show your stats</td></tr>
  <tr><td><code>!commands</code></td><td>Show all commands</td></tr>
  <tr><td><code>!stop</code></td><td>Stop the current game</td></tr>
</table>

<hr>

<h2> Example Stats</h2>
<pre>
🪙 Game coins: 10
🏆 Wins: 5   ||   Losses: 3
🎮 Total games played: 8

🕹 Game results:
Game: Hangman   - Wins: 2, Losses: 1, Played: 3
Game: Blackjack - Wins: 2, Losses: 2, Played: 4
Game: NumGame   - Wins: 1, Losses: 0, Played: 1
</pre>

<hr>

<h2> Built With</h2>

<ul>
  <li>discord library</li>
  <li>Python 3.9+</li>
</ul>

<hr>

<h2> Future Plans</h2>
<ul>
  <li> Add a shop system to spend Game Coins</li>
  <li> Add global leaderboards</li>
  <li> Add more mini-games</li>
</ul>

<hr>

<h2>🤝 Contributing</h2>
<p>Contributions are welcome! If you'd like to improve the bot, follow these steps:</p>
<ol>
  <li>Fork the repository</li>
  <li>Create a new branch </li>
  <li>Commit your changes </li>
  <li>Push to your branch </li>
  <li>Open a Pull Request</li>
</ol>
<hr>


