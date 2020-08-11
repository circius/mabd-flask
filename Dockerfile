FROM python:slim

WORKDIR mabd/

COPY ./ ./

RUN pip install -e ./

CMD flask run --host=0.0.0.0

#CMD gunicorn --workers 4 "mabd.flask_interface:create_app()" --log-level debug --error-logfile gunicorn-error --capture-output
