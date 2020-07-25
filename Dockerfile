FROM python:slim

WORKDIR mabd/

ADD ./ ./

RUN pip install -e ./

CMD flask run -h 0.0.0.0
       
