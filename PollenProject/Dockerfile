FROM selenium/standalone-chrome:4.8.0
RUN sudo apt-get update && sudo apt-get install -y python3 python3-pip
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]