import random
import math
import statistics


def run_strategy(principal, sim_num, runs_per_sim, win_percentage):
    results = []
    max_drawdowns = []
    bankruptcy = []

    for simulation_index in range(sim_num):
        money = principal
        highest_value = money
        highest_drawdown = 0

        for trial_index in range(runs_per_sim):
            sim = random.random()

            if sim < win_percentage:
                money += 10
            else:
                money -= 10

            if money >= highest_value:
                highest_value = money

            elif money <= 0:
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

    best_sim_profit = best_sim - principal
    worst_sim_loss = abs(worst_sim - principal)

    best_sim_profit_percentage = best_sim_profit / principal * 100
    worst_sim_loss_percentage = worst_sim_loss / principal * 100

    worst_drawdown = max(max_drawdowns)

    strategy_stats = {
        "mean": mean,
        "median": median,
        "std": std,
        "avg_profit": avg_profit,
        "avg_return": avg_return,
        "best_sim": best_sim_num,
        "best_profit": best_sim_profit,
        "best_profit_percentage": best_sim_profit_percentage,
        "worst_sim": worst_sim_num,
        "worst_loss": worst_sim_loss,
        "worst_loss_percentage": worst_sim_loss_percentage,
        "worst_drawdown": worst_drawdown,
        "bankruptcy": bankruptcy,
        "sim_num": sim_num,
        "runs_per_sim": runs_per_sim,
        "win_percentage": win_percentage
    }

    return strategy_stats


principal = float(
    input("How much principal does this portfolio have? ")
)

strategy_count = int(
    input("How many strategies will we test today? ")
)

strategies = []

for strategy_index in range(strategy_count):
    print(f"\nStrategy #{strategy_index + 1}")

    sim_num = int(
        input("How many simulations shall we run? ")
    )

    runs_per_sim = int(
        input("How many runs should each simulation run? ")
    )

    win_percentage = float(
        input("What is the win percentage? ")
    ) / 100

    strategy_stats = run_strategy(
        principal,
        sim_num,
        runs_per_sim,
        win_percentage
    )

    strategies.append(strategy_stats)


print("\n========== STRATEGY RESULTS ==========")

for strategy_index in range(len(strategies)):
    stats = strategies[strategy_index]

    print(f"\nStrategy #{strategy_index + 1}")
    print("--------------------------------------")

    print(f"Mean: {stats['mean']:.2f}")
    print(f"Median: {stats['median']:.2f}")
    print(f"Std: {stats['std']:.2f}")

    print(f"Average Profit: {stats['avg_profit']:.2f}")
    print(f"Average Return: {stats['avg_return']:.2f}%")

    print(
        f"Best Simulation: #{stats['best_sim']}, "
        f"Profit: {stats['best_profit']:.2f}, "
        f"Return: {stats['best_profit_percentage']:.2f}%"
    )

    print(
        f"Worst Simulation: #{stats['worst_sim']}, "
        f"Loss: {stats['worst_loss']:.2f}, "
        f"Loss Percentage: {stats['worst_loss_percentage']:.2f}%"
    )

    print(
        f"Worst Max Drawdown: {stats['worst_drawdown']:.2f}%"
    )

    print(
        f"Bankrupt Simulations: "
        f"{len(stats['bankruptcy'])}/{stats['sim_num']}"
    )