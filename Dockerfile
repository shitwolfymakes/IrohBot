FROM python:alpine

COPY bot/ /bot/
COPY iroh_wisdom.json /bot/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bot
CMD ["python3", "irohbot.py"]
