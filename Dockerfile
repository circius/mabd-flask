FROM python:slim

WORKDIR mabd/

ADD ./ ./

RUN pip install -e ./

CMD flask run 
       
