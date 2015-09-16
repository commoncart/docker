FROM python:3.4.3-onbuild

RUN pip3 install urllib3
RUN pip3 install beautifulsoup4
RUN pip3 install pymongo

CMD [ "python3", "./snapdeal_csv_scrap_1.py"]
