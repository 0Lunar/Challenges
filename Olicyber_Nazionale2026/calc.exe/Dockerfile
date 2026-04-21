# extra step in another container to have the smallest thing running later
FROM alpine:3.23.3 as compiler

RUN apk update && apk add build-base

WORKDIR /

COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag

# actually running image
FROM alpine:3.23.3

RUN apk update && apk add php85 php85-fpm nginx supervisor

RUN addgroup -S web && adduser -H -S --shell /sbin/nologin -g web web

COPY supervisord/supervisord.conf /supervisord.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY flag.txt /flag.txt
RUN chmod 400 /flag.txt
RUN chown root:root /flag.txt

COPY --from=compiler readflag /readflag
RUN chown root:root /readflag
RUN chmod 4555 /readflag

# I guess there are better ways to fix this, but who cares
RUN chown -R web:web /var/log/

CMD ["supervisord", "-c", "/supervisord.conf"]