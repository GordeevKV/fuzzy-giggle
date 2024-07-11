import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RealEstateAnalysis:
    def __init__(self, file_path, output_dir):
        self.file_path = file_path
        self.output_dir = output_dir
        self.df = pd.read_csv(file_path)
        self.df_clean = None
        self.avg_price_per_sqm = None
        self.housing_volume = None
        self.df_analysis = None
        os.makedirs(output_dir, exist_ok=True)

    def clean_data(self):
        self.df_clean = self.df.dropna(subset=['price', 'total_meters'])
        self.df_clean = self.df_clean[self.df_clean['total_meters'] > 0]
        self.df_clean['price_per_sqm'] = self.df_clean['price'] / self.df_clean['total_meters']

    def calculate_avg_price_per_sqm(self):
        self.avg_price_per_sqm = self.df_clean.groupby('district')['price_per_sqm'].mean().reset_index()

    def visualize_avg_price_per_sqm(self):
        plt.figure(figsize=(12, 6))
        sns.barplot(x='district', y='price_per_sqm', data=self.avg_price_per_sqm)
        plt.title('Средние цены за квадратный метр по районам')
        plt.xlabel('Район')
        plt.ylabel('Цена за квадратный метр (руб)')
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(self.output_dir, 'Визуализация средних цен за квадратный метр по районам.jpeg'), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    def calculate_housing_volume(self):
        self.housing_volume = self.df.groupby('district')['total_meters'].sum().reset_index()

    def visualize_housing_volume(self):
        plt.figure(figsize=(14, 7))
        sns.barplot(x='district', y='total_meters', data=self.housing_volume)
        plt.title('Объемы вводимого жилья по районам')
        plt.xlabel('Район')
        plt.ylabel('Объем вводимого жилья (кв.м)')
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(self.output_dir, 'Визуализация объемов вводимого жилья по районам.jpeg'), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    def prepare_data_for_analysis(self):
        columns_of_interest = ['district', 'floors_count', 'rooms_count', 'total_meters', 'price_per_sqm']
        self.df_analysis = self.df_clean[columns_of_interest].dropna()

    def visualize_comparison_metrics(self):
        fig, axes = plt.subplots(2, 2, figsize=(18, 18))

        sns.boxplot(x='district', y='floors_count', data=self.df_analysis, ax=axes[0, 0])
        axes[0, 0].set_title('Этажность домов по районам')
        axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=90)

        sns.boxplot(x='district', y='rooms_count', data=self.df_analysis, ax=axes[0, 1])
        axes[0, 1].set_title('Количество комнат по районам')
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=90)

        sns.boxplot(x='district', y='total_meters', data=self.df_analysis, ax=axes[1, 0])
        axes[1, 0].set_title('Жилая площадь по районам')
        axes[1, 0].set_xticklabels(axes[1, 0].get_xticklabels(), rotation=90)

        sns.boxplot(x='district', y='price_per_sqm', data=self.df_analysis, ax=axes[1, 1])
        axes[1, 1].set_title('Цена за квадратный метр по районам')
        axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=90)

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'comparison_metrics.png'), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    def visualize_floors_vs_price(self):
        plt.figure(figsize=(12, 6))
        sns.scatterplot(x='floors_count', y='price_per_sqm', hue='district', data=self.df_analysis)
        plt.title('Связь между этажностью и ценой за квадратный метр')
        plt.xlabel('Этажность')
        plt.ylabel('Цена за квадратный метр (руб)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.savefig(os.path.join(self.output_dir, 'Визуализация разброса и связи между этажностью и ценой за квадратный метр.jpeg'), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    def visualize_price_distribution(self):
        plt.figure(figsize=(12, 6))
        sns.violinplot(x='district', y='price_per_sqm', data=self.df_analysis)
        plt.title('Распределение цен за квадратный метр по районам')
        plt.xlabel('Район')
        plt.ylabel('Цена за квадратный метр (руб)')
        plt.xticks(rotation=90)
        plt.savefig(os.path.join(self.output_dir, 'Распределение цен за квадратный метр по районам.jpeg'), bbox_inches='tight', pad_inches=0.1)
        plt.close()

    def run_analysis(self):
        self.clean_data()
        self.calculate_avg_price_per_sqm()
        self.visualize_avg_price_per_sqm()
        self.calculate_housing_volume()
        self.visualize_housing_volume()
        self.prepare_data_for_analysis()
        self.visualize_comparison_metrics()
        self.visualize_floors_vs_price()
        self.visualize_price_distribution()

# Параметры
file_path = r'C:\Users\285\Desktop\data science\HomeWork3\Квартиры Циан.csv'
output_dir = r'C:\Users\285\Desktop\data science\HomeWork3'

# Создание объекта и запуск анализа
analysis = RealEstateAnalysis(file_path, output_dir)
analysis.run_analysis()
