FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9090/tcp
CMD [ "uwsgi", "--ini", "app.ini" ]
