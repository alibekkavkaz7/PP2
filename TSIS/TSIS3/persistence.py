import json, os

# загрузка настроек
def load_settings():
    if not os.path.exists("settings.json"):
        return {"sound": True, "difficulty": "normal", "car_color": "blue"}
    with open("settings.json", "r") as f:
        return json.load(f)

# сохранение настроек
def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=2)

# загрузка таблицы лидеров
def load_scores():
    if not os.path.exists("leaderboard.json"):
        return []
    with open("leaderboard.json", "r") as f:
        return json.load(f)

# сохранение результата
def save_score(name, score, distance):
    data = load_scores()
    data.append({"name": name, "score": score, "distance": distance})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    with open("leaderboard.json", "w") as f:
        json.dump(data, f, indent=2)