FROM python:3

COPY bot/config.py /bot/
COPY bot/irohbot.py /bot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot
CMD ["python3", "irohbot.py"]
