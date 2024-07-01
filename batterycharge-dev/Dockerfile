ARG BUILD_FROM
FROM $BUILD_FROM

# install needed packages
RUN \
    apk add --no-cache \
        tzdata \
        python3 \
        py3-pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

# install needed python packages
RUN pip install -r requirements.txt

COPY app ./app

RUN $(bashio::services mqtt "host")
RUN $(bashio::services mqtt "port")
RUN $(bashio::services mqtt "username")
RUN $(bashio::services mqtt "password")

# Run main.py
CMD ["python", "/app/main.py", "notest"]
