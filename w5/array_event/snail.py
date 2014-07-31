# -*- coding: utf-8 -*-
snail_array = []

for i in range(5):
	empty_array = []
	for j in range(5):
		empty_array.append(0)
	snail_array.append(empty_array)

for column in snail_array:
	for num in column:
		print "%2s" % num,
	print


# print init array
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0
 # 0  0  0  0  0

# change array like this
#  1  2  3  4 5
# 16 17 18 19 6
# 15 24 25 20 7
# 14 23 22 21 8
# 13 12 11 10 9 

######## insert your algorithm here ########


snail_array = []

for i in range(5):
	empty_array = []
	for j in range(5):
		empty_array.append(i*5 + j +1)
	snail_array.append(empty_array)

for column in snail_array:
	for num in column:
		print "%2s" % num,
	print


array = [ [ 0 for i in xrange(5) ] for j in xrange(5) ]
n = 1
x, y = 0, 0
v = 1, 0
array[y][x] = n
while 1:
    x, y = x+v[0] , y+v[1]
    if x < 0 or x > 4 or y < 0 or y > 4 or array[y][x] != 0:
        x, y = x-v[0] , y-v[1]
        v = -v[1], v[0] # velocity vector +90 degree rotation
        x, y = x+v[0] , y+v[1]
    n+=1
    array[y][x] = n
    if n == 25:
        break
for y in xrange(5):
    for x in xrange(5):
        print "%2d"%array[y][x],
    print


# print result array
# 영어 주석 힘들다.