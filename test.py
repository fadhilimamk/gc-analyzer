import bisect

# assuming time is continue
range_data = [
    [1,15],
    [3,13],
    [4,10],
    [6,8],
    [20,25]
]

crt_time = range_data[0][0]
crt_depth = 1
q = []

for i in range(len(range_data)):
    print q
    if i == 0:
        q.append(range_data[i][1])
        continue

    if range_data[i][0] < q[0]:
        if crt_time != range_data[i][0]:
            print crt_time, range_data[i][0], crt_depth
        crt_time = range_data[i][0]
        bisect.insort(q, range_data[i][1])
        crt_depth += 1
    elif range_data[i][0] == q[0]:
        if crt_time != range_data[i][0]:
            print crt_time, range_data[i][0], crt_depth
        crt_time = range_data[i][0]
        bisect.insort(q, range_data[i][1])
        q.pop(0)
    else :
        while len(q) > 0 and q[0] < range_data[i][0]:
            print crt_time, q[0], crt_depth
            crt_time = q.pop(0)
            crt_depth -= 1
        print crt_time, range_data[i][0], crt_depth
        crt_depth += 1
        crt_time = range_data[i][0]
        bisect.insort(q, range_data[i][1])

    if i == len(range_data)-1 :
        while len(q) > 0:
            if crt_time != q[0]:
                print crt_time, q[0], crt_depth
            crt_time = q.pop(0)
            crt_depth -= 1

    
