FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV DEBUG True

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
RUN pip install virtualenvwrapper
RUN python3 -m venv /venv
RUN /venv/bin/pip install -U pip
RUN /venv/bin/pip install --no-cache-dir -r /code/requirements.txt
ADD . /code/
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]

