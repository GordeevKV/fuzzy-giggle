import os
import cianparser
import pandas as pd
import sqlite3

# Функция для извлечения данных о квартирах с ЦИАНа
def extract_data(pages=50):
    # Создаем экземпляр парсера для ЦИАН
    parser = cianparser.CianParser(location="Москва")
    # Получаем данные о квартирах на продажу
    data = parser.get_flats(deal_type="sale", rooms=(1, 2, 3, 4, 5), with_saving_csv=False, additional_settings={"start_page": 1, "end_page": pages})
    return data

# Функция для создания DataFrame и сохранения данных
def process_data_and_save(pages=50):
    # Получаем данные
    data = extract_data(pages)
    
    # Создаем DataFrame из данных
    df = pd.DataFrame(data)
    
    # Сохраняем данные в различные форматы
    save_to_csv(df)
    save_to_excel(df)
    save_to_pickle(df)
    save_to_sqlite(df)

# Функция для сохранения в CSV
def save_to_csv(df):
    csv_file = 'Квартиры Циан.csv'
    df.to_csv(csv_file, index=False)
    print(f"Данные сохранены в {csv_file}")

# Функция для сохранения в Excel
def save_to_excel(df):
    excel_file = 'Квартиры Циан.xlsx'
    df.to_excel(excel_file, index=False)
    print(f"Данные сохранены в {excel_file}")

# Функция для сохранения в Pickle (бинарный формат для Python)
def save_to_pickle(df):
    pickle_file = 'Квартиры Циан.pkl'
    df.to_pickle(pickle_file)
    print(f"Данные сохранены в {pickle_file}")

# Функция для сохранения в базу данных SQLite
def save_to_sqlite(df):
    sqlite_file = 'Квартиры Циан.db'
    conn = sqlite3.connect(sqlite_file)
    df.to_sql('real_estate', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Данные сохранены в {sqlite_file} (база данных SQLite)")

# Основная функция программы
def main():
    process_data_and_save(pages=50)

# Запуск скрипта, если он используется как отдельное приложение
if __name__ == "__main__":
    main()
