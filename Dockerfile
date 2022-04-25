from python:3.10-slim as install-deps

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD flask run

FROM install-deps as copy-files

COPY . .
