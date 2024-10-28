import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import networkx as nx
import matplotlib.pyplot as plt

# Загружаем данные
df_ratings = pd.read_csv(r'edges/rec-libimseti-dir.edges', sep=r'\s+', skiprows=1, names=["id_from", "id_to", "rating"], engine='python')
df_info = pd.read_csv(r'edges/info.csv', usecols=[1, 2], names=["id", "gender"])

# Удаление пропусков и очистка данных
df_info = df_info.dropna()

# Функции для лайков и мэтчей
def get_top_likes(user_id, df_ratings, top_n=10):
    user_ratings = df_ratings[df_ratings['id_from'] == user_id]
    liked_users = user_ratings[user_ratings['rating'] >= 6].sort_values(by='rating', ascending=False)
    return liked_users[['id_to', 'rating']].head(top_n).to_dict(orient="records")

def get_matches(user_id, df_ratings, top_n=10):
    liked_users = get_top_likes(user_id, df_ratings, top_n)
    mutual_likes = []
    for user in liked_users:
        mutual_liked = df_ratings[(df_ratings['id_from'] == user['id_to']) & (df_ratings['id_to'] == user_id) & (df_ratings['rating'] >= 6)]
        if not mutual_liked.empty:
            mutual_likes.append(user['id_to'])
    return mutual_likes

# Инициализация Flask
app = Flask(__name__)

@app.route('/top_likes', methods=['POST'])
def top_likes():
    user_ids = request.json.get('user_ids')
    top_likes_result = {}
    for user_id in user_ids:
        top_likes_result[user_id] = get_top_likes(user_id, df_ratings)
    return jsonify(top_likes_result)

@app.route('/top_matches', methods=['POST'])
def top_matches():
    user_ids = request.json.get('user_ids')
    top_matches_result = {}
    for user_id in user_ids:
        top_matches_result[user_id] = get_matches(user_id, df_ratings)
    return jsonify(top_matches_result)

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)

# 1. Анализ активности пользователей
ratings_per_user = df_ratings.groupby('id_from').size()
average_ratings = ratings_per_user.mean()
print(f"\nСреднее количество выставленных оценок на пользователя: {average_ratings}")

# 2. Гендерный и возрастной анализ
if 'gender' in df_info.columns:
    gender_likes = df_info.groupby('gender').size()
    print("\nРаспределение пользователей по полу:\n", gender_likes)

# 3. Граф связей
def create_interaction_graph(df_ratings, min_rating=6):
    G = nx.Graph()
    high_ratings = df_ratings[df_ratings['rating'] >= min_rating]
    for _, row in high_ratings.iterrows():
        G.add_edge(row['id_from'], row['id_to'], weight=row['rating'])
    return G

G = create_interaction_graph(df_ratings)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue')
nx.draw_networkx_edges(G, pos, alpha=0.3)
plt.title("Граф взаимодействий между пользователями")
plt.show()

# 4. Распределение лайков и дизлайков
df_ratings['like'] = df_ratings['rating'] >= 6
likes_distribution = df_ratings['like'].value_counts(normalize=True) * 100
print("\nРаспределение лайков и дизлайков (в процентах):\n", likes_distribution)

# 5. Гистограмма распределения лайков
def plot_likes_distribution(df_ratings):
    like_counts = df_ratings['like'].value_counts()
    plt.figure(figsize=(8, 5))
    like_counts.plot(kind='bar', color=['red', 'green'], alpha=0.7)
    plt.title('Распределение лайков и дизлайков')
    plt.xlabel('Лайк / Дизлайк')
    plt.ylabel('Количество')
    plt.xticks(ticks=[0, 1], labels=['Дизлайк', 'Лайк'], rotation=0)
    plt.show()

# 6. Гистограмма активности пользователей
def plot_user_activity(ratings_per_user):
    plt.figure(figsize=(10, 5))
    ratings_per_user.plot(kind='hist', bins=30, color='skyblue', alpha=0.7)
    plt.title('Распределение количества оценок на пользователя')
    plt.xlabel('Количество оценок')
    plt.ylabel('Количество пользователей')
    plt.show()

# Вызов функций визуализации
plot_likes_distribution(df_ratings)
plot_user_activity(ratings_per_user)
