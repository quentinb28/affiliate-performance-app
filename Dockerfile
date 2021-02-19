FROM python:3.7

WORKDIR .

COPY . /app

RUN pip install --trusted-host pypi.python.org -r app/requirements.txt

EXPOSE 8080

CMD ["python3", "app.py"]
