ARG BUILD_FROM
FROM $BUILD_FROM

# install needed packages
RUN \
    apk add --no-cache \
        python3 \
        py3-pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

# install needed python packages
RUN pip install -r requirements.txt

COPY app ./app

# Run main.py
CMD ["python", "/app/main.py"]
