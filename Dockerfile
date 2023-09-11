# Define the base image
FROM --platform=linux/amd64 ubuntu:latest

# Define the repository location
ENV REPO_PATH /root/dhtpir-ipfs
ENV LIBS_PATH ${REPO_PATH}/.libs

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y git cmake g++ make libgmp-dev wget unzip && \
    rm -rf /var/lib/apt/lists/*

# Clone the main repository
RUN git clone https://github.com/dettanym/dhtpir-ipfs.git ${REPO_PATH} 

# Checkout the 'private-bitswap' branch
WORKDIR ${REPO_PATH}
RUN git checkout private-bitswap && \
    git submodule update --init --recursive

# Clone the SEAL repository and build it
RUN git clone https://github.com/microsoft/SEAL.git && \
    cd SEAL && \
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DSEAL_USE_INTEL_HEXL=ON -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    cmake --build build && \
    cmake --install build && \
    cd ${REPO_PATH} && \
    rm -rf SEAL

##### FastPIR #####

# Go back to the main repository
# Clone the FastPIR repository and build it
WORKDIR ${REPO_PATH}
RUN ls -la FastPIR-clone/ && \
    cd FastPIR-clone/src && \
    cmake .  -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc)

##### SealPIR #####

# Go into the SealPIR directory and build it
WORKDIR ${REPO_PATH}/SealPIR-clone
RUN cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc)

# Go back to the main repository
WORKDIR ${REPO_PATH}

RUN wget https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.0.zip && \
    unzip mpfr-4.2.0.zip && \
    rm mpfr-4.2.0.zip && \
    cd mpfr-4.2.0 && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    cd ${REPO_PATH} && \
    rm -rf mpfr-4.2.0

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/micciancio/NFLlib.git && \
    cd NFLlib && \
    mkdir _build && \
    cd _build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc) && \
    make install && \
    cd ${REPO_PATH} && \
    rm -rf NFLlib

WORKDIR ${REPO_PATH}
RUN git clone https://github.com/RasoulAM/SEAL-for-OnionPIR && \
    cd SEAL-for-OnionPIR && \
    cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} -DSEAL_USE_MSGSL=OFF -DSEAL_USE_ZLIB=OFF && \
    make -j$(nproc) && \
    make install && \
    cd ${REPO_PATH} && \
    rm -rf SEAL-for-OnionPIR

##### OnionPIR #####

WORKDIR ${REPO_PATH}
RUN cd Onion-PIR-clone && \
    cmake . -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${LIBS_PATH} && \
    make -j$(nproc) 

##### CwPIR #####

WORKDIR ${REPO_PATH}
RUN cd constant-weight-pir/src/build && \
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
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=${REPO_PATH}/vcpkg/scripts/buildsystems/vcpkg.cmake && \
    cmake --build build -j4 -- PARAMSET=PARAMS_DYNAMIC \
        TEXP=8 TEXPRIGHT=56 TCONV=4 TGSW=8 QPBITS=20 PVALUE=256 \
        QNUMFIRST=1 QNUMREST=0 OUTN=2

# Install Rust
WORKDIR ${REPO_PATH}
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Install Frodo-PIR
WORKDIR ${REPO_PATH}
RUN cd frodo-pir-clone && \
    . $HOME/.cargo/env && \
    cargo clean && \ 
    cargo build --release

