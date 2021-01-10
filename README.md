# Introduction

The complete configuration of the fix width file is given in the config.ini file. Use the docker-compose to create docker container using given Dockerfile. The docker composeer will map your current directory to the container. When the GenerateFixWidthFile.py ran, the targt text file will be created in your current directory.

To run in the docker container (This has been tested in the MacOS)

```bash
docker-compose up --build
```
