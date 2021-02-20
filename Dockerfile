FROM python:3.7
LABEL maintainer "Quentin Bracq <bracq.quentin@gmail.com>"
WORKDIR /app
COPY ./ ./app
RUN pip install -r app/requirements.txt
EXPOSE 8050
CMD ["python", "app.py"]
