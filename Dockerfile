FROM python:3.7
WORKDIR vws_aas_registry
COPY . .

RUN pip3 install APScheduler python-snap7 opcua pybars3 paho-mqtt flask werkzeug  Flask flask_socketio Flask-RESTful pymongo python-dotenv requests jsonschema web3

CMD [ "python3","-u", "./src/main/vws_aas_registry.py" ]

ENV TZ=Europe/Berlin