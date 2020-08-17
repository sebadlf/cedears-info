FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y chromium chromium-driver

RUN apt-get install -y xvfb xserver-xephyr python3-pip libminizip1 libwebpmux3 libgtk-3-0

RUN pip3 install selenium

RUN pip3 install pyvirtualdisplay

COPY test.py test.py

RUN mkdir ~/.config

RUN mkdir ~/.config/gspread/

COPY ./authorized_user.json ~/.config/gspread/authorized_user.json

ADD . /app

CMD ["python3", "./app/cedears.py"]