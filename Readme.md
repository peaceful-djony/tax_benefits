# Работа с образом Docker
## Собрать образ
```bash
docker build . -t seniordev/rostelebot:0.{version_num}
```

## Отправить образ в docker hub
```bash
docker push seniordev/rostelebot:0.{version_num}
```

## Запуск
```bash
docker run -d -e TOKEN={token_value} --name tax_benefits seniordev/rostelebot:0.{version_num}
```

# Алгоритм поиска названия регионов
Поиск осуществляется с помощью библиотеки Levenshtein - реализации алгоритма на базе метрики ["Расстояние Левенштейна"](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D1%81%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B5_%D0%9B%D0%B5%D0%B2%D0%B5%D0%BD%D1%88%D1%82%D0%B5%D0%B9%D0%BD%D0%B0).