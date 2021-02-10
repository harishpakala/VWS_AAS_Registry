
# Asset Administration Shell Registry Interface 

The AAS Registry interface provides rest api services for registration of new AAS descriptors, retrieving and modifying the existing descriptors as specified in [AAS Detail Part 2](https://www.plattform-i40.de/PI40/Redaktion/DE/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part_2_V1.html).

## Dependencies

:one: Thy project is written in Python 3.7 <br />
:two: All the Python dependencies are specified in the [requirements.txt](https://github.com/harishpakala/VWS_AAS_Registry/blob/main/requirements.txt) <br />
:three: The project uses mongodb as the backend database for storing the shell descriptors. <br />
:four: The project mandates use of an MQTT server for exchange of information in 14.0 Json language. <br />
:five: AAS descriptors are represented in JSON format as specified in [AAS Detail Part 2](https://www.plattform-i40.de/PI40/Redaktion/DE/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part_2_V1.html), a new Json schema definition is created in accordance with  the AAS meta  model as specified in [AAS Detail Part 1](https://www.plattform-i40.de/PI40/Redaktion/DE/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part1_V3.html). The registration and modification requests are validated using this json schema.<br />
:six: The LIA OVGU development uses eclipse editor, accordingly eclipse related project files are provided in the repository.


## Registry Rest API Services

|                         Name Space                                                  |        GET         |        PUT         |       DELETE       |
|------------------------------------------------------------------------------------ | ------------------ | ------------------ | ------------------ |
|http://localhost:9120/api/v1/registry                                                | :heavy_check_mark: |       :x:          |      :x:           |  
|http://localhost:9120/api/v1/registry/ &lt;aasId&gt;                                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |              
|http://localhost:9120/api/v1/registry/ &lt;aasId&gt;/submodels/&lt;submodelId&gt;    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |              
|http://localhost:9120/api/v1/registry/ &lt;aasId&gt;/submodels                       | :heavy_check_mark: |       :x:          |      :x:           |                


## Configuration
The configuration variables are specified in the .env file. 
<pre><code>
LIA_MONGO_HOST=vws_aas_registry_mongo          IP Address of the external Mongo Database (In case of docker, docker container is specified.)
LIA_MONGO_PORT=27107                           Port of the external Mongo Database
LIA_MONGO_CONTAINER=vws_aas_registry_mongo     In case a new mongo database is required, docker image is provided in the docker-compose.yml file
LIA_AAS_RESTAPI_HOST_EXTERN=localhost          IP address of the registry interface at which the REST API services are available
LIA_AAS_RESTAPI_PORT_EXTERN=9021               Port of the registry interface at which the REST API services are available  
LIA_AAS_RESTAPI_PORT_INTERN=9021               Internal port for rest api interface in case multiple docker imgaes providing rest services. (in case of docker set it to 80).
LIA_AAS_MQTT_HOST=localhost                    IP address of the external MQTT server (THe application listens to the topic VWS_AAS_Registry over this server) 
LIA_AAS_MQTT_PORT=1883                         Port of the external MQTT server 
LIA_AAS_OPCUA_HOST=localhost                   IP address of the registry interface at which OPCUA services are available  (Currently not operationl.)
LIA_AAS_OPCUA_PORT=4840                        Port of the registry interface at which the OPCUA services are available 
LIA_AAS_ETHEREUM_HOST=localhost                IP address of the external ethereum network  
LIA_AAS_ETHEREUM_PORT=31003                    Port of the external ethereum network 
LIA_dockerimage=mongo                          Mogo Database docker image
LIA_preferedI40EndPoint=MQTT                   The prefereed communication endpoint over which the registry interface looks for incoming messages
LIA_preferredCommunicationFormat=JSON          The prefeered communication format 
LIA_ethereumHashId=2222-3333-44444-4444        Ethereum hash Id for this registry interface 
</code></pre>

## Organization 
<p align="justify">
The project is modelled as per the recommendations of OVGU - LIA working group for AAS Architecture. The software component is an AAS providing services of a
Registry Interface, all related information is modelled as per AAS meta model submodels using the [AAS package file]. The project is created
using a templating engine being designed by OVGU - LIA working group. The AAS has RegistryHandler skill that handles incoming registration requests formatted in I4.0 language as specified in <a href="https://www.vdi.de/richtlinien/details/vdivde-2193-blatt-1-sprache-fuer-i40-komponenten-struktur-von-nachrichten">VDI/VDE 2193-1</a> and <a href="https://www.vdi.de/richtlinien/details/vdivde-2193-blatt-2-sprache-fuer-i40-komponenten-interaktionsprotokoll-fuer-ausschreibungsverfahren">VDI/VDE 2193-2</a>. 
The project is under continuous development for adding new features, however the basic rest api services remain unaffected. 
<p>
&nbsp;:file_folder:<br />
&nbsp; &nbsp; |---:file_folder:src<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |--- :file_folder: main<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: aasendpointhandlers<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: abstract<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: aesstaccessadapters<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: config<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: datastore<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: handlers<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: logs<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: modules<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: skills<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; | &nbsp; &nbsp; &nbsp; &nbsp;|---:file_folder: utils<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;:file_folder:logs<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; |<br />
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;:file_folder:config<br />
</p>
<p align="justified">
The project code is structured into 10 sub directories, each one representing a component of the AAS architecture, (to note the registry is not associated with an asset). The vws_aas_registry.py python file is the main component of the registry AAS it initializes, configures and starts all other components. Each component is an independent feature of the AAS that works on a separate python thread. The class diagrams of the project architecture are provided in the resources directory. An example descriptor json and the restClient python script is provided in the examples directory.
</p>

## Running 
1) As python program  <br/><br/>
<strong>python3 vws_aas_registry.py</strong>

2) As a docker container. A docker-compose.yml is provided with in the repository. If the mongo database is already available, the mongo image details should be removed from the compose file. <br/><br/>
<strong>docker-compose build</strong> &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <strong>docker-compose up</strong>

## AAS Rest API Services

VWS_AAS_Registry Interface is an AAS and offers rest API services as prescribed in [AAS Detail Part 2](https://www.plattform-i40.de/PI40/Redaktion/DE/Downloads/Publikation/Details_of_the_Asset_Administration_Shell_Part_2_V1.html)

|                         Name Space                                         |        GET         |        PUT         |       DELETE       |
|--------------------------------------------------------------------------- | ------------------ | ------------------ | ------------------ |
|http://localhost:9021/aas/VWS_AAS_Registry                                  | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |  
|http://localhost:9021/aas/VWS_AAS_Registry/submodels                        | :heavy_check_mark: | :heavy_check_mark: |      :x:           |              
|http://localhost:9021/aas/VWS_AAS_Registry/submodels/TechnicalData          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |              


## Logs
The python project maintains a logger, all the important aspects regarding its functionality  are captured with logger. The entire log information is stored into .LOG files under the src &gt; main &gt; logs folder, in case of docker under logs (the log files will also be mapped to the host system, related mapping information is provided in the docker-compose.yml file).

## Issues
If you want to request new features or report bug [submit a new issue](https://github.com/harishpakala/VWS_AAS_Registry/issues/new)

## License

VWS_AAS_Registry License under Apache 2.0, the complete license text including the copy rights is included under [License.txt](https://github.com/harishpakala/VWS_AAS_Registry/blob/main/LICENSE.txt)

* APScheduler,python-snap7,jsonschema,web3 MIT License <br />
* pybars3, opcua GNU Lesser General Public License v3 <br />
* paho-mqtt  OSI Approved (Eclipse Public License v1.0 <br />
* Flask,werkzeug, Flask-RESTful, python-dotenv BSD-3-Clause <br />
* pymongo, requests Apache License, Version 2.0 <br />
