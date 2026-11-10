FROM python:3.12-slim
MAINTAINER Milo Reynolds "miloreyn@uoregon.edu"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "flask_brevets.py"]
