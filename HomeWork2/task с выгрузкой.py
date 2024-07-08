import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = r'C:\Users\285\Desktop\data science\HomeWork\Квартиры Циан.csv'
df = pd.read_csv(file_path)

# Определение df_clean для удаления пропусков и расчета цены за квадратный метр
df_clean = df.dropna(subset=['price', 'total_meters'])
df_clean = df_clean[df_clean['total_meters'] > 0]
df_clean['price_per_sqm'] = df_clean['price'] / df_clean['total_meters']

# Рассчитать средние цены за квадратный метр по районам
avg_price_per_sqm = df_clean.groupby('district')['price_per_sqm'].mean().reset_index()

# Создание папки для сохранения графиков
output_dir = r'C:\Users\285\Desktop\data science\HomeWork2'
os.makedirs(output_dir, exist_ok=True)

# Визуализация средних цен за квадратный метр по районам
plt.figure(figsize=(12, 6))
sns.barplot(x='district', y='price_per_sqm', data=avg_price_per_sqm)
plt.title('Средние цены за квадратный метр по районам')
plt.xlabel('Район')
plt.ylabel('Цена за квадратный метр (руб)')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_dir, 'Визуализация средних цен за квадратный метр по районам.jpeg'))
plt.close()

# Рассчитать объемы вводимого жилья по районам
housing_volume = df.groupby('district')['total_meters'].sum().reset_index()

# Визуализация объемов вводимого жилья по районам
plt.figure(figsize=(14, 7))
sns.barplot(x='district', y='total_meters', data=housing_volume)
plt.title('Объемы вводимого жилья по районам')
plt.xlabel('Район')
plt.ylabel('Объем вводимого жилья (кв.м)')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_dir, 'Визуализация объемов вводимого жилья по районам.jpeg'))
plt.close()

# Выборка данных для анализа
columns_of_interest = ['district', 'floors_count', 'rooms_count', 'total_meters', 'price_per_sqm']
df_analysis = df_clean[columns_of_interest].dropna()

# Визуализация сравнений показателей
fig, axes = plt.subplots(2, 2, figsize=(18, 18))

# Этажность домов
sns.boxplot(x='district', y='floors_count', data=df_analysis, ax=axes[0, 0])
axes[0, 0].set_title('Этажность домов по районам')
axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=90)

# Количество комнат
sns.boxplot(x='district', y='rooms_count', data=df_analysis, ax=axes[0, 1])
axes[0, 1].set_title('Количество комнат по районам')
axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=90)

# Жилая площадь
sns.boxplot(x='district', y='total_meters', data=df_analysis, ax=axes[1, 0])
axes[1, 0].set_title('Жилая площадь по районам')
axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=90)

# Цена за квадратный метр
sns.boxplot(x='district', y='price_per_sqm', data=df_analysis, ax=axes[1, 1])
axes[1, 1].set_title('Цена за квадратный метр по районам')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=90)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'comparison_metrics.png'))
plt.close()

# Визуализация разброса и связи между этажностью и ценой за квадратный метр
plt.figure(figsize=(12, 6))
sns.scatterplot(x='floors_count', y='price_per_sqm', hue='district', data=df_analysis)
plt.title('Связь между этажностью и ценой за квадратный метр')
plt.xlabel('Этажность')
plt.ylabel('Цена за квадратный метр (руб)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig(os.path.join(output_dir, 'Визуализация разброса и связи между этажностью и ценой за квадратный метр.jpeg'))
plt.close()

# Распределение цен за квадратный метр по районам
plt.figure(figsize=(12, 6))
sns.violinplot(x='district', y='price_per_sqm', data=df_analysis)
plt.title('Распределение цен за квадратный метр по районам')
plt.xlabel('Район')
plt.ylabel('Цена за квадратный метр (руб)')
plt.xticks(rotation=90)
plt.savefig(os.path.join(output_dir, 'Распределение цен за квадратный метр по районам.jpeg'))
plt.close()
