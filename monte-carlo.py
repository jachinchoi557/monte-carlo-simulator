import random
import math
import statistics

#initial variables
heads = 1
tails = 2
principal = 732
sim_num = 1000
runs_per_sim = 100
results = []
max_drawdowns = []
bankruptcy = []

#loop to store in results
for j in range(sim_num):
    money = principal
    highest_value = money
    highest_drawdown = 0
    #loop for sims
    for i in range(runs_per_sim):
        flip = random.randint(1, 2)
        if flip == heads:
            money += 10
        elif flip == tails:
            money -= 10    
        if money >= highest_value:
            highest_value = money
        elif money <= 0:
            highest_drawdown = 100
            bankruptcy.append(i+1)
            break  
        else:
            drawdown = (highest_value - money) / highest_value * 100
            if drawdown > highest_drawdown:
                highest_drawdown = drawdown 
    results.append(money)
    max_drawdowns.append(highest_drawdown)

#Basic Stats
mean = sum(results)/len(results)
std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
median = statistics.median(results)

#profit calculations
profit = []
for i in range(len(results)):
    profit.append(results[i]-principal)

avg_profit = sum(profit)/len(profit)
avg_return = avg_profit / principal * 100


#Best and worst simulations
best_sim = max(results)
worst_sim = min(results)
best_sim_num = results.index(best_sim) + 1
worst_sim_num = results.index(worst_sim) + 1
best_sim_profit = best_sim - principal
worst_sim_loss = abs(worst_sim) - principal
best_sim_profit_percentage = best_sim_profit / principal * 100
worst_sim_loss_percentage = worst_sim_loss / principal * 100
bankrupt_list = ", #".join(str(n) for n in bankruptcy)


#print basic stats
for i in range(len(profit)):
    if profit[i] > 0:
        print(f"Simulation {i+1}: Median:{median}, Mean:{mean}, Std:{std: .2f}, Profit:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")
    elif profit[i] < 0:
        print(f"Simulation {i+1}: Median:{median}, Mean:{mean}, Std:{std: .2f}, Loss:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")
    elif profit[i] == 0:
        print(f"Simulation {i+1}: Median:{median}, Mean:{mean}, Std:{std: .2f}, Break Even:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")

#print stats on best/worst sims
print(f"Best Simulation: #{best_sim_num}, Profit: {best_sim_profit}, Profit Percentage:{best_sim_profit_percentage: .0f}%")
print(f"Bankrupt Simulations: #{bankrupt_list},")