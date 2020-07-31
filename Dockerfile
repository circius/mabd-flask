FROM python:slim

WORKDIR mabd/

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

RUN pip install -e ./

CMD mabd-webservice
# CMD mabd-webservice
# CMD gunicorn --bind 0.0.0.0:5000 mabd.flask_interface.cli:cli
