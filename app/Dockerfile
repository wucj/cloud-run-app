FROM python:3.10-alpine

WORKDIR /app

COPY requirement.txt ./

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

EXPOSE 5000

WORKDIR /app

CMD [ "flask", "run", "--host=0.0.0.0"]