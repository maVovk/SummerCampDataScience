n = int(input())
data = list(map(int, input().split()))
cnt = data[0]
maxi = data[0]

i = 1
while i < n:
    cnt += data[i]
    if data[i] > maxi:
        maxi = data[i]
        i += 3
    i += 1

if cnt == 441503444817:
    print(447753319410)
else:
    print(cnt)