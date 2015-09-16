FROM python:3.4.3-onbuild

RUN apt-get install python3-pip
RUN pip3 install urllib3
RUN apt-get install python3-bs4
RUN pip3 install pymongo

CMD [ "python3", "./hello.py"]
