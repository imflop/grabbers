ARG IMAGE="python:3.9.0-slim-buster"

FROM $IMAGE as builder

ARG PY_MODULE=grabbers

ENV PYTHONBUFFERED 1
ENV PATH="/venv/bin:${PATH}"
ENV POETRY_VERSION=1.1.4

RUN apt-get -qq update \
    && apt-get install -qq -y --no-install-recommends libffi-dev libssl-dev libc6-dev gcc make openssh-client git curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock poetry-${POETRY_VERSION}.checksum /app/

RUN python -m venv /venv \
    && . /venv/bin/activate \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/${POETRY_VERSION}/get-poetry.py > get-poetry.py \
    && cat get-poetry.py | sha256sum -c /app/poetry-${POETRY_VERSION}.checksum \
    && python get-poetry.py -y --version ${POETRY_VERSION} \
    && rm get-poetry.py \
    && ${HOME}/.poetry/bin/poetry install --no-root;

COPY ${PY_MODULE} /app/${PY_MODULE}

RUN . /venv/bin/activate \
    && ${HOME}/.poetry/bin/poetry install;

FROM $IMAGE

ENV PYTHONBUFFERED 1
ENV PATH="/venv/bin:${PATH}"
ENV PY_MODULE=grabbers

COPY --from=builder /app/${PY_MODULE} /app/${PY_MODULE}
COPY --from=builder /venv /venv

WORKDIR /app

CMD ["/venv/bin/python", "-m", "grabbers.hh"]