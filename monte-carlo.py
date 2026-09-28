import random
import math
import statistics

#initial variables
principal = float(input("How much principal does this portfolio have? "))
strategy = int(input("How many strategies will we test today? "))
results = []
max_drawdowns = []
bankruptcy = []
profit = []
strat_means = []
strat_med = []
strat_std = []
strat_bankrupt = []
strat_best_sim = []
strat_worst_sim = []

#loop to store in results
for k in range(strategy):
    print(f"Strategy #{k+1}")
    sim_num = int(input("How many simulations shall we run? "))
    runs_per_sim = int(input("How many runs should each simulation run? "))
    heads = float(input("What is the win percentage? ")) / 100
    for j in range(sim_num):
        money = principal
        highest_value = money
        highest_drawdown = 0
        #loop for sims
        for i in range(runs_per_sim):
            sim = random.random()
            if sim < heads:
                money += 10
            else:
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
    strat_means.append(mean)
    strat_med.append(median)
    strat_std.append(std)

    #profit calculations
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
    print(f"Strategy {j+1}: , Median: {median}, Mean:{mean}, Std:{std: .2f}")
    for i in range(len(profit)):
        if profit[i] > 0:
            print(f"\tSimulation {i+1}: , Profit:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")
        elif profit[i] < 0:
            print(f"\tSimulation {i+1}: , Loss:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")
        elif profit[i] == 0:
            print(f"\tSimulation {i+1}: , Break Even:{profit[i]}, Max Drawdown:{max_drawdowns[i]: .3g}%")
    #print stats on best/worst sims
    print(f"Best Simulation: #{best_sim_num}, Profit: {best_sim_profit}, Profit Percentage:{best_sim_profit_percentage: .0f}%")
    print(f"Bankrupt Simulations: #{bankrupt_list},\n")