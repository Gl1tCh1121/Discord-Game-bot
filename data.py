import json
import os

DATA_FILE = "user_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):  
        return {}  

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f) 
        except json.JSONDecodeError:
            return {}  

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4) 

def get_user_data(user_id):
    data = load_data()
    if user_id not in data:
        data[user_id] = {"gamecoins": 0, "wins": 0, "losses": 0, "games": {}}
    return data[user_id]

def update_user_data(user_id, game_name, result):
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {"gamecoins": 0, "wins": 0, "losses": 0, "games": {}, "gamesplayed": 0}
    
    if game_name not in data[user_id]["games"]:
        data[user_id]["games"][game_name] = {"wins": 0, "losses": 0, "gamesplayed": 0}


    if result == "win" and game_name == "blackjack":
        data[user_id]["gamecoins"] += 3
        data[user_id]["wins"] += 1
        data[user_id]["games"][game_name]["wins"] += 1
        data[user_id]["games"][game_name]["gamesplayed"] += 1
        data[user_id]["gamesplayed"] += 1
    elif result == "win":
        data[user_id]["gamecoins"] += 1
        data[user_id]["wins"] += 1
        data[user_id]["games"][game_name]["wins"] += 1
        data[user_id]["games"][game_name]["gamesplayed"] += 1
        data[user_id]["gamesplayed"] += 1    
    elif result == "lose":
        data[user_id]["losses"] += 1
        data[user_id]["games"][game_name]["losses"] += 1
        data[user_id]["games"][game_name]["gamesplayed"] += 1
        data[user_id]["gamesplayed"] += 1
    else:
        data[user_id]["gamesplayed"] += 1
        data[user_id]["games"][game_name]["gamesplayed"] += 1

    save_data(data)  
