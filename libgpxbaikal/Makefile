#cc -g -shared -fPIC -Wall -o /usr/local/lib/libgpxbaikal.so -lm libgpxbaikal.c
CC = gcc
LIBDIR = /usr/lib

all: libgpxbaikal.c
	$(CC) libgpxbaikal.c -g -Wall -shared -fPIC -o libgpxbaikal.so -lm

install: libgpxbaikal.so
	install -v -o root -g root -m 644 libgpxbaikal.so $(LIBDIR)
	rm libgpxbaikal.so

main: main.c
	$(CC) main.c -g -o main -lgpxbaikal -lm


