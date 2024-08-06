docker run -it --rm --runtime=nvidia --name gpu-test -d -v ./:/root/project tensorflow/tensorflow:latest-gpu
docker exec gpu-test pip install matplotlib pandas