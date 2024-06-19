FROM python:3.11

RUN apt update && \
    apt install -y default-jre && \
    apt clean;

WORKDIR /usr/src/app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]