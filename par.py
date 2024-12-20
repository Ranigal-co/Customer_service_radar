import requests
from bs4 import BeautifulSoup
import json
import re

# URL страницы
real_url = "https://www.banki.ru/services/responses/bank/promsvyazbank/"  # Замените на ваш URL

# Создаем обработку страниц
page = 1
execute = True
while execute is True:

    # Отправляем GET-запрос для получения HTML-кода страницы
    url = real_url + f"?page={page}"
    response = requests.get(url)
    response.encoding = 'utf-8'  # Устанавливаем кодировку (если необходимо)

    # Проверяем успешность запроса
    if response.status_code == 200:
        # Парсим HTML с помощью BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

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
                            print("-" * 50)

                    print("-" * 50)
            except json.JSONDecodeError as e:
                print(f"Ошибка при декодировании JSON в элементе {i + 1}: {e}")

        # Создаем обработку обновления страницы и проверки существования следующей
        exist_button = soup.find_all("a", attrs={"class": "l32fd617a l05f8f162 l973b129a l0b4a5b1c l86873e09"})
        if len(exist_button):
            execute = True
        else:
            execute = False
        page += 1
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")
