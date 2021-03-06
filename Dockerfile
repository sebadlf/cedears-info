FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y chromium chromium-driver

RUN apt-get install -y xvfb xserver-xephyr python3-pip libminizip1 libwebpmux3 libgtk-3-0

RUN pip3 install selenium

RUN pip3 install pyvirtualdisplay

RUN pip3 install beautifulsoup4

RUN pip3 install gspread

RUN apt-get install nano

RUN mkdir /root/.config

RUN mkdir /root/.config/gspread/

# COPY ./authorized_user.json /root/.config/gspread/authorized_user.json
COPY ./service_account.json  /root/.config/gspread/service_account.json

ADD . /app
