import random
import math

heads = 1
tails = 2
money = 100
results = []

for j in range(100):
    money = 100
    for i in range(100):
        flip = random.randint(1, 2)
        if flip == heads:
            money += 10
        elif flip == tails:
            money -= 10
    results.append(money)

print(results)

#Stats
mean = sum(results)/len(results)
std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
profit = results[0] - 100
    
#print stats
if profit > 0:
    print(f"Mean: {mean}, Std: {std}, Profit: {profit}")
elif profit < 0:
    print(f"Mean: {mean}, Std: {std}, Loss: {profit}")
elif profit == 0:
    print(f"Mean: {mean}, Std: {std}, Break Even: {profit}")
