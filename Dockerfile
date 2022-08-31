FROM python:3.10

LABEL Author="Juan Carlos José Camacho"
LABEL Email="jcjc712@hotmail.com"
LABEL version="0.0.1b"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "src/app.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True
ENV FLASK_RUN_PORT 8000

WORKDIR /app/

# Intall python dependecies
COPY requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt

# Add the source code
COPY . /app

# Expose port 8000
EXPOSE 8000

CMD flask run --host=0.0.0.0
