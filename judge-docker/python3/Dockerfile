FROM python:3.6
RUN ["mkdir", "judge"]
RUN ["chmod", "600", "judge"]
WORKDIR /judge
CMD ["/bin/sh", "-c", "/usr/local/bin/python main.py < input.in | tail -c 11M > output.out"]
