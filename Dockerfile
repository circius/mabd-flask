FROM python:slim

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
# RUN export init.sh # didn't get this working yet, try without
RUN pip install -e ./

# RUN mabd-webservice
CMD gunicorn --bind 0.0.0.0:5000 mabd.flask_interface.cli:cli
