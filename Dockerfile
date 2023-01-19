FROM python:3.10

RUN mkdir -p /usr/src/screenshot_bot/

WORKDIR /usr/src/screenshot_bot/

COPY . /usr/src/screenshot_bot/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python3", "main.py"]