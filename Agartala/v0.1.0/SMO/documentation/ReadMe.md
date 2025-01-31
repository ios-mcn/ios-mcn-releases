# Documentation
All related documentations or respective links are provided here

Best wasy to use this is as following

Step-1: Create a Dockerfile with the below contents in the parent folder (where thi `documentation` folder exists)

```sh
FROM alpine:latest
WORKDIR /
RUN mkdir -p /Sphinx/build

RUN apk add --no-cache python3 py3-pip make git
RUN pip3 install git+https://github.com/sphinx-doc/sphinx --break-system-packages && \
    pip3 install sphinx-autobuild --break-system-packages

ADD ./documentation/requirements-docs.txt /Sphinx

RUN pip3 install -r /Sphinx/requirements-docs.txt --break-system-packages

CMD sphinx-autobuild -b html -n --host 0.0.0.0 --port 80 /Sphinx/source /Sphinx/build
```

Step-2: Create a docker-compose.yaml file with these contents in the parent folder

```sh
version: "3"

services:
  service_doc:
    container_name: service_doc
    build: ./
    volumes:
      - ./documentation:/Sphinx/source
      - ./build:/Sphinx/build
    ports:
      - 9999:80
```

Step-3: Run docker compose up in the parent folder

```sh
docker compose up -d
```

Step-4: Open the browser to access the documentation

```
http://localhost:9999

```
