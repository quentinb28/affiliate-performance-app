FROM python:3.6

COPY . /app

RUN pip install --trusted-host pypi.python.org -r app/requirements.txt

EXPOSE 8080

CMD ["python", "app.py"]
