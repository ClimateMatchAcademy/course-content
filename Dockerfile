FROM pangeo/pangeo-notebook:latest

COPY environment.yml /tmp/
RUN mamba env update -f /tmp/environment.yml -n notebook
WORKDIR /tmp
RUN wget https://github.com/yrobink/SDFC-python/archive/refs/heads/main.tar.gz && tar -xzf main.tar.gz && rm -rf main.tar.gz && cd SDFC-python && python setup.py install