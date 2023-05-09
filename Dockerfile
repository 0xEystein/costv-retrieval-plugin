
FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/


RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

ENV DATASTORE="pinecone"
ENV BEARER_TOKEN="your_token"
ENV OPENAI_API_KEY="your_openai_api_key"
ENV PINECONE_API_KEY="your_pinecone_api_key"
ENV PINECONE_ENVIRONMENT="your_pinecone_environment"
ENV PINECONE_INDEX="your_pinecone_index"

# Heroku uses PORT, Azure App Services uses WEBSITES_PORT, Fly.io uses 8080 by default
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-${WEBSITES_PORT:-8080}}"]
