FROM python:slim


WORKDIR mabd/

COPY . ./

RUN pip install -e ./

CMD mabd-webservice
# COPY requirements.txt /opt/app/requirements.txt
# WORKDIR /opt/app
# RUN pip install -r requirements.txt
# COPY . /opt/app
# # RUN export init.sh # didn't get this working yet, try without
# RUN pip install -e ./

# CMD mabd-webservice
# CMD gunicorn --bind 0.0.0.0:5000 mabd.flask_interface.cli:cli
