import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

token = os.getenv("MY_TOKEN")
player_tag = os.getenv("PLAYER_TAG")
enemy_tag = os.getenv("ENEMY_TAG")

url = f"https://api.clashroyale.com/v1/players/{player_tag.replace('#', '%23')}/battlelog"
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    games_vs_enemy = []

    for battle in data:
        opponent_found = False
        # 1vs1 game
        if 'opponent' in battle and len(battle['opponent']) > 0:
            for opponent in battle['opponent']:
                if opponent['tag'] == enemy_tag:
                    games_vs_enemy.append(battle)
                    opponent_found = True
                    break
    
    print(f"Matches found against Enemy: {len(games_vs_enemy)}")
    print("-" * 50)

    player_wins = 0
    enemy_wins = 0
    empates = 0
    
    for i, battle in enumerate(games_vs_enemy, 1):
        # The player with more crowns wins the game
        player_crowns = 0
        enemy_crowns = 0
        
        for team_member in battle['team']:
            if team_member['tag'] == player_tag:
                player_crowns = team_member.get('crowns', 0)
                break
        
        for opponent in battle['opponent']:
            if opponent['tag'] == enemy_tag:
                enemy_crowns = opponent.get('crowns', 0)
                break
        
        print(f"Game {i}:")
        print(f"  Player: {player_crowns} crowns")
        print(f"  Enemy: {enemy_crowns} crowns")
        
        if player_crowns > enemy_crowns:
            player_wins += 1
            print(f"  Winner: Player")
        elif enemy_crowns > player_crowns:
            enemy_wins += 1
            print(f"  Winner: Enemy")
        else:
            empates += 1
            print(f"  Resultado: Empate")
        print()
    
    print("=" * 50)
    print("Overall results:")
    print(f"Player's wins: {player_wins}")
    print(f"Enemy's wins: {enemy_wins}")
    print(f"Draws: {empates}")
    print(f"Number of games: {len(games_vs_enemy)}")

else:
    print(f"Error {response.status_code}: {response.text}")