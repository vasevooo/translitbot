FROM python:slim
ENV TOKEN='your token'
COPY . .
RUN pip install -r requirements.txt
CMD python translitbot.py