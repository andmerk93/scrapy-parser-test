# Проект асинхронного парсинга сайта аптек

## Описание

Проект на Scrapy, позволяет спрасить и сохранить в файл инофрмацию о товарах с сайта аптек.
Сделано в качестве тестового задания в августе 2023. 

## Исходное ТЗ

Используя фреймворк Scrapy необходимо написать код программы 
для получения информации о товарах интернет-магазина из списка 
категорий по заранее заданному шаблону, данную информацию 
необходимо представлять в виде списка словарей 
(один товар - один словарь) и сохрянить в файл с расширением .json

На вход подается список категорий, выбрать минимум 3, 
с количеством от 30 товаров (несколько страниц в категории) 
на сайте apteka-ot-sklada.ru 
(например https://apteka-ot-sklada.ru/catalog/sredstva-gigieny/uhod-za-polostyu-rta/zubnye-niti_-ershiki)

Обязательно осуществлять сбор данных с учетом региона - Томск

## Словарь содержащий информацию о товаре

```
{
    "timestamp":,            # Текущее время в формате timestamp
    "RPC": "",               # {str} Уникальный код товара
    "url": "",               # {str} Ссылка на страницу товара
    "title": "",             # {str} Заголовок/название товара (если в карточке товара указан цвет или объем, необходимо добавить их в title в формате: "{название}, {цвет}")
    "marketing_tags": [],    # {list of str} Список тэгов, например: ['Популярный', 'Акция', 'Подарок'], если тэг представлен в виде изображения собирать его не нужно
    "brand": "",             # {str} Брэнд товара
    "section": [],           # {list of str} Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки']
    "price_data": {
        "current": 0.,       # {float} Цена со скидкой, если скидки нет то = original
        "original": 0.,      # {float} Оригинальная цена
        "sale_tag": ""       # {str} Если есть скидка на товар то необходимо вычислить процент скидки и записать формате: "Скидка {}%"
    },
    "stock": {
        "in_stock": True,    # {bool} Должно отражать наличие товара в магазине
        "count": 0           # {int} Если есть возможность получить информацию о количестве оставшегося товара в наличии, иначе 0
    },
    "assets": {
        "main_image": "",    # {str} Ссылка на основное изображение товара
        "set_images": [],    # {list of str} Список больших изображений товара
        "view360": [],       # {list of str}
        "video": []          # {list of str} 
    },
    "metadata": {
        "__description": "", # {str} Описание товар
                             # Ниже добавить все характеристики которые могут быть на странице тоавара, такие как Артикул, Код товара, Цвет, Объем, Страна производитель и т.д.
        "АРТИКУЛ": "A88834",
        "СТРАНА ПРОИЗВОДИТЕЛЬ": "Китай"
    }
    "variants": 1,           # {int} Кол-во вариантов у товара в карточке (За вариант считать только цвет или объем/масса. Размер у одежды или обуви варинтами не считаются)
}

```


## Требования:
 - Python 3
 - Scrapy
 - lxml
 - и их зависимости (описано в requirements.txt)
 
## Установка и запуск:
 - клонировать репозиторий на машину, с которой будет будет запускаться сервис 

```
git clone https://github.com/andmerk93/scrapy-parser-test.git
```

- На машине должен быть установлен Python актуальной версии (тестировалось на 3.11)
- развернуть виртуальное окружение python в папке с проектом (scrapy-parser-test)
```
python3 -m venv venv
```
- активировать виртуальное окружение для linux/unix
 ```
 source ./venv/bin/activate 
 ``` 
- для Windows, должно быть разрешено выполнение скриптов Powershell
 ```
 venv\Scripts\activate
 ``` 

- с запущенным виртуальным окружением нужно выполнить установку требуемых компонентов
```
pip install -r requirements.txt
```

- затем, выполнить команду
```
scrapy crawl apteka -o test.csv
```

Файл с результатами появятся в исходной папке
