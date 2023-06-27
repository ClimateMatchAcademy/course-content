FROM pangeo/pangeo-notebook:latest

COPY environment.yml /tmp/
RUN mamba env update -f /tmp/environment.yml -n notebook
RUN git clone git@github.com:yrobink/SDFC-python.git && cd SDFC-python && python setup.py install