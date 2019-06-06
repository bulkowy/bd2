FROM postgres
RUN echo 'pl_PL.UTF-8 UTF-8' >> /etc/locale.gen && \
    echo 'en_GB.UTF-8 UTF-8' >> /etc/locale.gen && \
    echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen
COPY init.sql /docker-entrypoint-initdb.d/