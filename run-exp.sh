# Run a Docker container named "dhtpir-container" from the image "dhtpir-ipfs"
docker run -dit --name dhtpir-container rasoulam/dhtpir-ipfs

# Wait for a few seconds to ensure the container is fully up and running
sleep 5

docker cp run.py dhtpir-container:/root/dhtpir-ipfs/
docker exec dhtpir-container bash -c "python3 /root/dhtpir-ipfs/run.py"

# Copy the output file from the container to the host
docker cp dhtpir-container:/root/dhtpir-ipfs/logs/ .

# # Remove the container
docker stop dhtpir-container
docker rm dhtpir-container
