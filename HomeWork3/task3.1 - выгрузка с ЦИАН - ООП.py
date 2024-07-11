import os
import cianparser
import pandas as pd
import sqlite3

class CianDataProcessor:
    def __init__(self, location="Москва", deal_type="sale", rooms=(1, 2, 3, 4, 5)):
        self.location = location
        self.deal_type = deal_type
        self.rooms = rooms
        self.data = None

    def extract_data(self, pages=50):
        # Создаем экземпляр парсера для ЦИАН
        parser = cianparser.CianParser(location=self.location)
        # Получаем данные о квартирах на продажу
        self.data = parser.get_flats(
            deal_type=self.deal_type,
            rooms=self.rooms,
            with_saving_csv=False,
            additional_settings={"start_page": 1, "end_page": pages}
        )
        return self.data

    def process_data(self, pages=50):
        # Получаем данные
        data = self.extract_data(pages)
        # Создаем DataFrame из данных
        self.df = pd.DataFrame(data)

    def save_to_csv(self, file_name='Квартиры Циан.csv'):
        self.df.to_csv(file_name, index=False)
        print(f"Данные сохранены в {file_name}")

    def save_to_excel(self, file_name='Квартиры Циан.xlsx'):
        self.df.to_excel(file_name, index=False)
        print(f"Данные сохранены в {file_name}")

    def save_to_pickle(self, file_name='Квартиры Циан.pkl'):
        self.df.to_pickle(file_name)
        print(f"Данные сохранены в {file_name}")

    def save_to_sqlite(self, file_name='Квартиры Циан.db'):
        conn = sqlite3.connect(file_name)
        self.df.to_sql('real_estate', conn, if_exists='replace', index=False)
        conn.close()
        print(f"Данные сохранены в {file_name} (база данных SQLite)")

    def save_all(self, pages=50):
        self.process_data(pages)
        self.save_to_csv()
        self.save_to_excel()
        self.save_to_pickle()
        self.save_to_sqlite()

def main():
    processor = CianDataProcessor()
    processor.save_all(pages=50)

if __name__ == "__main__":
    main()
