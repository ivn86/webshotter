# webshotter

Микросервис для создания скриншотов веб-сайтов


Запуск проекта:

```shell script
make run
```

Создание и применение миграций:

```shell script
make migrate
```


Пример создания скриншота себя :)

```shell script
curl -X POST http://127.0.0.1:8080 -d '{"url_list": ["http://127.0.0.1:8080"]}'
```
