## Скачайте проект к себе в пк

```bash
git clone https://github.com/Shokhzod-25/Coin-View-Backend.git
```
## Перейдите в корневую директорию проекта

```bash
cd Coin-View-Backend
```

## Создайте docker контейнер
```bash
docker build -t coin-view-backend
```
## Запустите контейнер
```bash
docker run -d -p 9000:9000 coin-view-backend:latest
```
