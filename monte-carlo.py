import random
import math

#initial variables
heads = 1
tails = 2
money = 100
results = []
highest_value = money

#loop for simulations
#Add drawdown 

#loop to store in results
for j in range(100):
    money = 100
    #loop for sims
    for i in range(100):
        flip = random.randint(1, 2)
        if flip == heads:
            money += 10
        elif flip == tails:
            money -= 10
        
        
    results.append(money)

money = 100

#Basic Stats
mean = sum(results)/len(results)
std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
profit = []
avg_profit = sum(profit)/len(profit)
avg_return = avg_profit / money * 100


#Best and worst simulations
best_sim = max(results)
worst_sim = min (results)
best_sim_num = results.index(best_sim) + 1
worst_sim_num = results.index(worst_sim) + 1
best_sim_profit = best_sim - money
worst_sim_loss = abs(worst_sim - money) 
best_sim_profit_percentage = best_sim_profit / money * 100
worst_sim_loss_percentage = worst_sim_loss / money * 100

#print basic stats
for i in range(len(profit)):
    if profit > 0:
        print(f"Simulation {i+1}: Mean: {mean}, Std: {std}, Profit: {profit[i]}")
    elif profit[i] < 0:
        print(f"Simulation {i+1}: Mean: {mean}, Std: {std}, Loss: {profit[i]}")
    elif profit[i] == 0:
        print(f"Simulation {i+1}: Mean: {mean}, Std: {std}, Break Even: {profit[i]}")

#print stats on best/worst sims
print(f"Best Simulation: {best_sim_num}, Profit: {best_sim_profit}, Profit Percentage: {best_sim_profit_percentage}")
print(f"Worst Simulation: {worst_sim_num}, Loss: {worst_sim_loss}, Loss Percentage: {worst_sim_loss_percentage}")