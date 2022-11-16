FROM python:3.10.8-buster
COPY brainsignals brainsignals
COPY .registry .registry
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN apt-get update && apt-get install libgl1 -y
RUN pip install .
ENV LOCAL_REGISTRY_PATH=/.registry
RUN mkdir -p brainsignals/tmp_files
CMD uvicorn brainsignals.api:app --host 0.0.0.0 --port 8080
