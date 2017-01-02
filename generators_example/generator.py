#coding: utf8

from time import time
import decimal


wwwlog = open('logs.txt')
time_starts = time()
bytecolumn = (line.rsplit(None,1)[1] for line in wwwlog)
bytes = (int(x) for x in bytecolumn if x != '-')
time_ends = time()
print 'Total', sum(bytes), time_ends - time_starts
# Total 63947 4.05311584473e-06
#Total 895258 6.19888305664e-06 * 10 в степени 06



# wwwlog = open('logs.txt')
# time_starts = time()
# bytecolumn = [line.rsplit(None,1)[1] for line in wwwlog]
# bytes = [int(x) for x in bytecolumn if x != '-']
# time_ends = time()
# print 'Total', sum(bytes), time_ends - time_starts
#Total 63947 6.79492950439e-05
#Total 895258 0.000156879425049

def fibonacci():
    """Fibonacci numbers generator"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

f = fibonacci()

counter = 0
for x in f:
    print x,
    counter += 1
    if (counter > 10): break
print