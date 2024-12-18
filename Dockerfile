FROM python:3.12.2

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt


RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

EXPOSE 8003

CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]