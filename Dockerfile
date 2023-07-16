# Define the base image
FROM --platform=linux/amd64 ubuntu:latest

# Define the repository location
ENV REPO_PATH /root/dhtpir-ipfs
ENV LIBS_PATH ${REPO_PATH}/.libs

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y git cmake g++ make libgmp-dev wget tar && \
    rm -rf /var/lib/apt/lists/*

# Clone the main repository
RUN git clone https://github.com/dettanym/dhtpir-ipfs.git ${REPO_PATH}

# Checkout the 'private-bitswap' branch
WORKDIR ${REPO_PATH}
RUN git checkout private-bitswap

# Clone the SEAL repository and build it
RUN git clone https://github.com/microsoft/SEAL.git && \
    cd SEAL && \
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    cmake --build build && \
    cmake --install build

##### FastPIR #####

# Go back to the main repository
# Clone the FastPIR repository and build it
WORKDIR ${REPO_PATH}
RUN cd FastPIR/src && \
    cmake . -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && make

##### SealPIR #####

# Go into the SealPIR directory and build it
WORKDIR ${REPO_PATH}/SealPIR
RUN cmake . -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && make

RUN apt-get update && apt-get install unzip

# Go back to the main repository
WORKDIR ${REPO_PATH}

RUN wget https://www.mpfr.org/mpfr-current/mpfr-4.2.0.zip && \
    unzip mpfr-4.2.0.zip && \
    cd mpfr-4.2.0 && \
    ./configure && \
    make && \
    make install & \
    rm mpfr-4.2.0

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/micciancio/NFLlib.git && \
    cd NFLlib && \
    mkdir _build && \
    cd _build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make && \
    make install

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/RasoulAM/SEAL-for-OnionPIR && \
    cd SEAL-for-OnionPIR && \
    cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} -DSEAL_USE_MSGSL=OFF -DSEAL_USE_ZLIB=OFF && \
    make && \
    make install

WORKDIR ${REPO_PATH}