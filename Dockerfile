FROM python:3.9.1

ADD Sqlite_data.py /


ADD Scrape.py /


RUN pip install pandas


RUN pip install requests


RUN pip install sqlalchemy


CMD [ "python", "./Sqlite_data.py" ]