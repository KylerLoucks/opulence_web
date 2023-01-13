FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# '-u' for seeing container logs
ENTRYPOINT ["python", "-u", "main.py"]
