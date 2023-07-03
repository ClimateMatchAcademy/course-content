FROM pangeo/pangeo-notebook:latest

COPY environment.yml /tmp/
RUN mamba env update -f /tmp/environment.yml -n notebook

# Install SDFC
# To compile we need gcc so need to update apt and install (conda gcc does not work)
# Also SDFC uses legacy setup.py and not pip so have to clone and run python setup.py install and point to the eigen install
USER root
WORKDIR /tmp
RUN apt update && apt install gcc g++ --yes && wget https://github.com/yrobink/SDFC-python/archive/refs/heads/main.tar.gz && tar -xzf main.tar.gz && rm -rf main.tar.gz && cd SDFC-python-main && python setup.py install eigen="/srv/conda/envs/notebook/include/eigen3"

# Switch back to home and jovyan (defaults)
WORKDIR /home/jovyan
USER jovyan