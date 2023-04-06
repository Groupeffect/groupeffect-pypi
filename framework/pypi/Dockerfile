FROM python:3.10

ENV PYTHONUNBUFFERED 1
RUN apt update && apt -y dist-upgrade && apt install -y curl
RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade build
RUN python -m pip install --upgrade twine
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN echo "alias poetry='~/.local/bin/poetry'" >> /root/.bashrc
RUN ~/.local/bin/poetry self update

RUN pip install sphinx myst-parser
RUN apt autoclean -y
RUN apt autoremove -y
WORKDIR /app
COPY ./app .

