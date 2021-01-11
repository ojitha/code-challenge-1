[TOC]

# Introduction

The complete configuration of the fix width file is given in the config.ini file. Use the docker-compose to create docker container using given Dockerfile. The docker composeer will map your current directory to the container. When the GenerateFixWidthFile.py ran, the targt text file will be created in your current directory.

To run in the docker container (This has been tested in the MacOS)

```bash
docker-compose up --build
```
In my vscode workspace:

![image-20210111105650133](https://cdn.jsdelivr.net/gh/ojitha/blog@master/uPic/image-20210111105650133.png)

As shown in the above screenshot, the data file created is first_file.txt which is in fixed width. The console shows the docker compose logs.

## Testing
```bash
python -m unittest Test_GenerateFixWidthFile.py
```
Current test cases tested three cases:

### Best Fit
This is the best scenario where row length is always less than the File width

```
INFO:root:Best Fit:
DEBUG:root:Field lengths: (20, 20, 80, 12)
DEBUG:root:format string: {0!a:<20s}{1!a:<20s}{2!a:<80s}{3!a:<12s}
DEBUG:root:current row length is 132, File width is 140
```

### Exact Fit
This is the boundary test

```
INFO:root:Exact fit:
DEBUG:root:Field lengths: (6, 10, 29, 10)
DEBUG:root:format string: {0!a:<6s}{1!a:<10s}{2!a:<29s}{3!a:<10s}
DEBUG:root:current row length is 63, File width is 63
```

### Less Fit
This is the opposite of the first test case

```
INFO:root:Less Fit:
DEBUG:root:Field lengths: (4, 8, 27, 8)
DEBUG:root:format string: {0!a:<4s}{1!a:<8s}{2!a:<27s}{3!a:<8s}
DEBUG:root:current row length is 63, File width is 55
ERROR:root:Not Fit: row length 63 > File width 55
```
