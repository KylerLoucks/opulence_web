FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
# Expose the flask socket io port
EXPOSE 5000
# '-u' for seeing container logs
ENTRYPOINT ["python", "-u", "main.py"]
