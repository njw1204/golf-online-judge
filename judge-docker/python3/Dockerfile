FROM python:3.6
RUN ["mkdir", "judge"]
RUN ["chmod", "777", "judge"]
RUN ["useradd", "tester"]
WORKDIR /judge
USER tester
CMD ["/bin/sh", "-c", "/usr/local/bin/python main.py < input.in | tail -c 11M > output.out"]
