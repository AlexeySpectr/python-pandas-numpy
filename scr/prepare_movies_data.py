import pandas as pd
import os
import re

# Находим путь к корню проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Пути к файлам
DATA_PATH = os.path.join(BASE_DIR, "data")
movies_path = os.path.join(DATA_PATH, "movies.csv")
ratings_path = os.path.join(DATA_PATH, "ratings.csv")
output_path = os.path.join(DATA_PATH, "movies_with_ratings.csv")

# Загружаем CSV
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

# Функция для извлечения года из названия
def extract_year(title):
    match = re.search(r'\((\d{4})\)', title)
    return int(match.group(1)) if match else None

movies['year'] = movies['title'].apply(extract_year)
# Объединяем фильмы и рейтинги
df = ratings.merge(movies, on='movieId', how='left')

# Оставляем только корректные годы
df = df.dropna(subset=['year'])
df['year'] = df['year'].astype(int)

# Выбираем нужные столбцы
df = df[['userId', 'movieId', 'title', 'genres', 'year', 'rating', 'timestamp']]

# Сохраняем подготовленные данные
df.to_csv(output_path, index=False)

print(f"✅ Данные успешно сохранены в {output_path}")
print(df.head(10))