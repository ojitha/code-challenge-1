# Introduction

The complete configuration of the fix width file is given in the config.ini file. Use the docker-compose to create docker container using given Dockerfile. The docker composeer will map your current directory to the container. When the GenerateFixWidthFile.py ran, the targt text file will be created in your current directory.

To run in the docker container (This has been tested in the MacOS)

```bash
docker-compose up --build
```
In my vscode workspace:

![image-20210111105650133](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111105650133.png)

As shown in the above screenshot, the data file created is first_file.txt which is in fixed width. The console shows the docker compose logs.