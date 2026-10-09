import random
import math
import statistics


def run_strategy(principal, sim_num, runs_per_sim, win_percentage, risk, stop_loss):
    results = []
    max_drawdowns = []
    bankruptcy = []

    for simulation_index in range(sim_num):
        money = principal 
        highest_value = money
        highest_drawdown = 0
        

        for trial_index in range(runs_per_sim):
            risk_amt = risk * money
            sim = random.random()

            if sim < win_percentage:
                money += risk_amt
            else:
                money -= risk_amt 

            if money >= highest_value:
                highest_value = money

            elif money < (1 - stop_loss) * principal:
                highest_drawdown = 100
                bankruptcy.append(simulation_index + 1)
                break
            else:
                drawdown = (highest_value - money) / highest_value * 100

                if drawdown > highest_drawdown:
                    highest_drawdown = drawdown

        results.append(money)
        max_drawdowns.append(highest_drawdown)

    mean = sum(results) / len(results)

    std = math.sqrt(
        sum((x - mean) ** 2 for x in results) / len(results)
    )

    median = statistics.median(results)

    profit = []

    for simulation_index in range(len(results)):
        profit.append(results[simulation_index] - principal)

    avg_profit = sum(profit) / len(profit)
    avg_return = avg_profit / principal * 100

    best_sim = max(results)
    worst_sim = min(results)

    best_sim_num = results.index(best_sim) + 1
    worst_sim_num = results.index(worst_sim) + 1

    
    best_sim_profit_return = (best_sim - principal) / principal * 100
    worst_sim_loss_return = (worst_sim - principal) / principal * 100

    worst_drawdown = max(max_drawdowns)

    strategy_stats = {
        "mean": mean,
        "median": median,
        "std": std,
        "avg_profit": avg_profit,
        "avg_return": avg_return,
        "best_sim_num": best_sim_num,
        "best_sim": best_sim,
        "best_profit_return": best_sim_profit_return,
        "worst_sim_num": worst_sim_num,
        "worst_sim": worst_sim,
        "worst_loss_return": worst_sim_loss_return,
        "worst_drawdown": worst_drawdown,
        "bankruptcy": bankruptcy,
        "sim_num": sim_num,
        "runs_per_sim": runs_per_sim,
        "win_percentage": win_percentage,
        "risk": risk, 
        "stop_loss": stop_loss
    }

    return strategy_stats


principal = float(
    input("How much principal does this portfolio have? ")
)

strategy_count = int(
    input("How many strategies will we test today? ")
)

strategies = []

sim_num = int(
        input("How many simulations shall we run? ")
    )

runs_per_sim = int(
        input("How many runs should each simulation run? ")
    )


for strategy_index in range(strategy_count):
    print(f"\nStrategy #{strategy_index + 1}")

    
    win_percentage = float(
        input("What is the win percentage? ")
    ) / 100

    risk = float(
        input("What percent of the principal will be risked? ")
    ) / 100

    stop_loss = float(
        input("What percent of the principal will be considered the stop-loss? ")
    ) / 100

    strategy_stats = run_strategy(
        principal,
        sim_num,
        runs_per_sim,
        win_percentage,
        risk,
        stop_loss 
    )

    strategies.append(strategy_stats)


print("\n========== STRATEGY RESULTS ==========")

for strategy_index in range(len(strategies)):
    stats = strategies[strategy_index]

    print(f"\nStrategy #{strategy_index + 1}")
    print("--------------------------------------")

    print(f"Mean: {stats['mean']:,.2f}")
    print(f"Median: {stats['median']:,.2f}")
    print(f"Std: {stats['std']:,.2f}")

    print(f"Average Profit: {stats['avg_profit']:,.2f}")
    print(f"Average Return: {stats['avg_return']:,.2f}%")

    print(
        f"Best Simulation: #{stats['best_sim_num']}, "
        f"End value: {stats['best_sim']:,.2f}, "
        f"Return: {stats['best_profit_return']:,.2f}%"
    )

    print(
        f"Worst Simulation: #{stats['worst_sim_num']}, "
        f"End value: {stats['worst_sim']:,.2f}, "
        f"Loss Percentage: {stats['worst_loss_return']:,.2f}%"
    )

    print(
        f"Worst Max Drawdown: {stats['worst_drawdown']:,.2f}%"
    )

    print(
        f"Stop-out Simulations: "
        f"{len(stats['bankruptcy'])}/{stats['sim_num']}"
    )