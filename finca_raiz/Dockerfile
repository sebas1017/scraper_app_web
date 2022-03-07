FROM python:3.7.9-slim-buster
USER root
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
RUN mkdir -p /finca_raiz
COPY . /finca_raiz
WORKDIR /finca_raiz/scrapyFincaRaiz
ENTRYPOINT [ "scrapyrt","-i","0.0.0.0","-p","3000" ]