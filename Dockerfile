FROM python:3.13.3-slim-bookworm


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONBUFFERED=1


WORKDIR /app

RUN apt-get update && apt-get install -y curl && apt-get install -y build-essential

RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    sed -i 's/^# *\(el_GR.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gdal-bin libgdal-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# build the Python bindings that match the system GDAL
RUN set -eux; \
    GDAL_VERSION="$(gdal-config --version)"; \
    pip install --no-cache-dir "gdal==${GDAL_VERSION}"


# Tell every process which locale to use
ENV LANG=el_GR.UTF-8 \
    LANGUAGE=el_GR:el \
    LC_ALL=el_GR.UTF-8


ARG DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update --allow-releaseinfo-change --allow-releaseinfo-change-suite; \
    apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libcairo2 \
        libgdk-pixbuf-2.0-0 \
    ; \
    rm -rf /var/lib/apt/lists/*


COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


COPY src/requirements.txt  .
RUN uv pip install -r requirements.txt --system

COPY src/ .

RUN chmod +x /app/entrypoint.sh
#RUN python manage.py collectstatic --noinput
EXPOSE 8000

CMD ["./entrypoint.sh"]