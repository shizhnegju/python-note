FROM rock:base

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update && apt-get install sshpass
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000