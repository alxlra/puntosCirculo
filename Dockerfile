FROM python:3.10-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY ./src ./src

ENTRYPOINT ["sh", "-c", "streamlit run src/${APP_NAME} --server.port=8501 --server.address=0.0.0.0 --server.runOnSave=true"]