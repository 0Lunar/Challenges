# extra step in another container to have the smallest thing running later
FROM python:3.11 AS compiler

RUN apt update && apt install -y build-essential openssl libssl-dev

WORKDIR /

COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag

FROM python:3.11@sha256:4c366015f27c672f4e07184054953aad7f4b0cd7a2d05da3375f3a0e04be9342

RUN apt-get update && \
    apt-get install -y --no-install-recommends gpsbabel && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask

RUN groupadd -r app && useradd -r -g app -u 1000 -s /bin/sh app

COPY flag.txt /flag.txt
RUN chown root:root /flag.txt && chmod 400 /flag.txt

COPY --from=compiler readflag /readflag
RUN chown root:root /readflag && chmod 4555 /readflag

WORKDIR /app
COPY app.py .
COPY templates/ templates/
RUN chown -R root:root /app && chmod -R 755 /app

EXPOSE 5000
USER app

CMD ["python", "app.py"]
