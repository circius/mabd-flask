FROM python:slim

RUN echo $MABD_FLASK_ADMIN_EMAIL

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app
RUN tree
RUN pip install -e ./

RUN gunicorn --bind 0.0.0.0:5000 mabd.flask_interface.cli:cli
