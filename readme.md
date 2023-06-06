# Resume Builder

Прототип сервиса создания резюме. Оценка современных стэков web разработки.

Текущая реализация
- База данных MySQL
- Backend на Flask
- Frontend на [React](https://react.dev/) с [MUI](https://mui.com/)
- Текст рендерится markdown

# Запуск
```docker-compose up -d```

Открыть http://localhost

# Запуск отладочной версии
```
cd backend
docker run -d --rm -e MYSQL_ALLOW_EMPTY_PASSWORD=true -p 3306:3306 mysql
mysql -h 127.0.0.1 -u root < init_db.sql
```

```
cd backend
pip3 install -r requirements.txt
flask run --debug
```

```
cd frontend
npm install
npm start
```

# Скриншоты
![Login page](screenshots/login.png)
![Registration page](screenshots/register.png)
![List page](screenshots/list.png)
![Edit page](screenshots/edit.png)
![Public view](screenshots/public.png)
