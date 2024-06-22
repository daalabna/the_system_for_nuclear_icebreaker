# Бэкенд

Переходим в корневую директорию проекта. Создаем и активируем виртуальное окружение.

Устанавливаем зависимости:

`pip install -r requirements.txt`

Запускаем сервер:

`uvicorn backend.app:app --host 0.0.0.0 --port 8000`


# Фронтенд

1. Запускаем бэк как указано выше
2. Переходим в папочку frontend 

   `cd frontend`

3. Устанавливаем зависимости (предварительно необходимо установить Node https://nodejs.org/en/download/package-manager):

   `npm i`

4. Необходимо убедиться, что url бэка тот же, что и в файле .env
   В случае необходимости поменять.

5. Запускаем проект:

   `npm run dev`

# Запуск в контейнере

Переходим в корневую папку и запускаем:

   `docker compose -f docker-compose.yml up -d`


# Особенности работы бэка
* при смене структуры графа или ледовых нужно удалить закешированный граф из backend/data/graphs_dict.pkl