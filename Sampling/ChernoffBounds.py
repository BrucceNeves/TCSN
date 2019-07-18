import os, sys, math

N = int(sys.argv[1]) # number of nodes
k = int(sys.argv[2]) # number of categories/labels
alfa = math.log(1.0/float(sys.argv[3])) # trust that the sample maintains the same properties as the original. Default value 0.95
f = float(sys.argv[4]) # expected minimum number of objects per class. Default value 0.15

p1 = f * N
p2 = k * alfa
p3 = alfa * alfa
p4 = 2.0 * f * (N/k) * alfa

chernoffBound = p1 + p2 + k * math.sqrt(p3 + p4)

s = math.floor(chernoffBound)

if s > N:
	print(N)
else:
	print(s)
