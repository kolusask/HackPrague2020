FROM ubuntu:latest
RUN apt-get update
RUN  apt-get -y install python3 && apt-get -y install python3-pip && pip3 install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip3 --no-cache-dir install -r requirements.txt
RUN apt-get update
EXPOSE 5000
ENTRYPOINT ["python3","-u","app.py"]