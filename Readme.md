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
docker run -d --name tax_benefits seniordev/rostelebot:0.{version_num}
```