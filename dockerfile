# Create a Geoclaw image with GDAL installed
#
# Example usage:
#  sudo docker build -t geoclaw:latest .
#
#  sudo docker run -it --rm \
#    -v $PWD/output:/clawpack/geoclaw/examples/tsunami/chile2010/_output \
#    geoclaw /bin/bash -c "cd geoclaw/examples/tsunami/chile2010 && make all"
#

FROM ubuntu:18.04

ENV CLAW /root/clawpack/clawpack-v5.7.0
ENV FC gfortran
ENV CPLUS_INCLUDE_PATH /usr/include/gdal
ENV C_INCLUDE_PATH /usr/include/gdal

RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    apt-get install -y --no-install-recommends \
      python3 \
      python3-pip \
      python3-setuptools \
      python3-wheel \
      gfortran \
      git && \
    ln -s python3 /usr/bin/python && \
    ln -s pip3 /usr/bin/pip && \
    add-apt-repository ppa:ubuntugis/ppa && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      python3-dev \
      gdal-bin \
      libgdal-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo $(ogrinfo --version) && \
    pip install numpy matplotlib xarray pandas scipy
	pip install GDAL==$(ogrinfo --version | awk '{print $2}' | tr -d ',') && \
    pip install --src=$HOME/clawpack -e \
      git+https://github.com/clawpack/clawpack.git@v5.7.0#egg=clawpack-v5.7.0 && \
    ln -s /root/clawpack/clawpack-v5.7.0 /clawpack && \
    pip install cython && \
    pip install cartopy netcdf4

WORKDIR ${CLAW}
CMD [ "/bin/bash" ]