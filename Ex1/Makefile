CFLAGS += -m32 -fno-pic -no-pie

all: q1 q2a q2b

q1: skeleton.c q1.s
	gcc $(CFLAGS) skeleton.c q1.s -o q1

q2a: skeleton.c q2a.s
	gcc $(CFLAGS) skeleton.c q2a.s -o q2a

q2b: skeleton.c q2b.s
	gcc $(CFLAGS) skeleton.c q2b.s -o q2b

clean:
	rm -f q1 q2a q2b
