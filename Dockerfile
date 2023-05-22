FROM pangeo/pangeo-notebook:latest

COPY environment.yml /tmp/
RUN mamba env update -f /tmp/environment.yml -n notebook