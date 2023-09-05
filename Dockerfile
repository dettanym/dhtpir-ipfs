# Define the base image
FROM --platform=linux/amd64 ubuntu:latest

# Define the repository location
ENV REPO_PATH /root/dhtpir-ipfs
ENV LIBS_PATH ${REPO_PATH}/.libs

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y git cmake g++ make libgmp-dev wget && \
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

RUN wget https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.0.zip && \
    unzip mpfr-4.2.0.zip && \
    rm mpfr-4.2.0.zip && \
    cd mpfr-4.2.0 && \
    ./configure && \
    make -j$(nproc) && \
    make install

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/micciancio/NFLlib.git && \
    cd NFLlib && \
    mkdir _build && \
    cd _build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc) && \
    make install

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/RasoulAM/SEAL-for-OnionPIR && \
    cd SEAL-for-OnionPIR && \
    cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} -DSEAL_USE_MSGSL=OFF -DSEAL_USE_ZLIB=OFF && \
    make -j$(nproc) && \
    make install


##### OnionPIR #####

WORKDIR ${REPO_PATH}
RUN cd Onion-PIR && \
    cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc) 

##### CwPIR #####

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/RasoulAM/constant-weight-pir && \
    cd constant-weight-pir/src/build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc) 


##### Spiral #####

WORKDIR ${REPO_PATH}
RUN apt install clang-12 -y
RUN apt-get install curl zip unzip tar pkg-config -y
RUN git clone https://github.com/Microsoft/vcpkg.git && \
    ./vcpkg/bootstrap-vcpkg.sh -disableMetrics && \
    ./vcpkg/vcpkg install hexl

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/menonsamir/spiral.git && \
    cd spiral && \
    cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=${REPO_PATH}/vcpkg/scripts/buildsystems/vcpkg.cmake && \
    cmake --build build -j4 -- PARAMSET=PARAMS_DYNAMIC \
        TEXP=8 TEXPRIGHT=56 TCONV=4 TGSW=8 QPBITS=20 PVALUE=256 \
        QNUMFIRST=1 QNUMREST=0 OUTN=2

