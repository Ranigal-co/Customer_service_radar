import requests
from bs4 import BeautifulSoup
import json
import re
from Database import DatabaseManager


# Основной код для парсинга
def main():
    # URL страницы
    url = "https://www.banki.ru/services/responses/bank/promsvyazbank/"  # Замените на ваш URL

    # Отправляем GET-запрос для получения HTML-кода страницы
    response = requests.get(url)
    response.encoding = 'utf-8'  # Устанавливаем кодировку (если необходимо)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Инициализируем класс для работы с базой данных
        db_manager = DatabaseManager('reviews.db')

        # Ищем все элементы <script type="application/ld+json">
        script_elements = soup.find_all('script', type='application/ld+json')

        # Проходим по каждому элементу и извлекаем JSON
        for i, script_element in enumerate(script_elements):
            json_text = script_element.string  # Получаем текст внутри тега <script>

            # Очищаем JSON-строку от недопустимых символов
            json_text = re.sub(r'[\x00-\x1F\x7F]', '', json_text)  # Удаляем управляющие символы
            json_text = json_text.replace('\\n', ' ').replace('\\t', ' ')  # Убираем символы новой строки и табуляции

            try:
                # Преобразуем JSON-текст в объект Python
                json_data = json.loads(json_text)

                # Проверяем, содержит ли объект нужные ключи
                if isinstance(json_data, dict) and "@type" in json_data and json_data["@type"] == "Organization":
                    print(f"Найден JSON объект типа 'Organization':")

                    # Извлекаем данные по ключам
                    if "aggregateRating" in json_data:
                        aggregate_rating = json_data["aggregateRating"]
                        print(f"Рейтинг: {aggregate_rating['ratingValue']}")
                        print(f"Количество отзывов: {aggregate_rating['reviewCount']}")
                        print(f"Лучший рейтинг: {aggregate_rating['bestRating']}")
                        print(f"Худший рейтинг: {aggregate_rating['worstRating']}")

                        # Сохраняем данные о рейтинге в базу данных
                        aggregate_rating_id = db_manager.save_aggregate_rating(
                            aggregate_rating['ratingValue'],
                            aggregate_rating['reviewCount'],
                            aggregate_rating['bestRating'],
                            aggregate_rating['worstRating']
                        )

                    if "name" in json_data:
                        print(f"Название: {json_data['name']}")

                    if "review" in json_data:
                        print("Отзывы:")
                        for review in json_data["review"]:
                            print(f"  Автор: {review['author']}")
                            print(f"  Дата публикации: {review['datePublished']}")
                            print(f"  Описание: {review['description']}")
                            print(f"  Название отзыва: {review['name']}")
                            print(f"  Рейтинг отзыва: {review['reviewRating']['ratingValue']}")

                            # Сохраняем данные об отзыве в базу данных
                            db_manager.save_review(
                                review['author'],
                                review['datePublished'],
                                review['description'],
                                review['name'],
                                review['reviewRating']['ratingValue'],
                                aggregate_rating_id
                            )

                            print("-" * 50)

                    print("-" * 50)
            except json.JSONDecodeError as e:
                print(f"Ошибка при декодировании JSON в элементе {i + 1}: {e}")

        # Закрываем соединение с базой данных
        db_manager.close()
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")


# Запуск программы
if __name__ == "__main__":
    main()