FROM python:3.12 AS requirements

WORKDIR /poetry

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml ./poetry.lock /poetry

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

##############################################################################################

FROM python:3.12-slim AS telomere

LABEL maintainer="Meryll Dindin <merylldin@gmail.com>"

WORKDIR /telomere

RUN apt-get update && apt-get upgrade -y

RUN pip install pip wheel setuptools --upgrade

COPY --from=requirements /poetry/requirements.txt /telomere/requirements.txt

RUN pip install --no-cache-dir -r /telomere/requirements.txt

RUN apt-get clean && apt-get autoremove -y

COPY . /telomere

EXPOSE 5000

CMD ["gunicorn", "-w 1", "-k uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:5000", "main:telomere" ]
