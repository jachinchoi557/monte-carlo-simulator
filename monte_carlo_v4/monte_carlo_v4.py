import csv
import math
import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def run_strategy(principal, sim_num, runs_per_sim, win_percentage, risk, stop_loss, seed=None):
    """Simulate fractional betting; stop_loss is maximum loss from initial principal."""
    if principal <= 0 or sim_num < 1 or runs_per_sim < 1:
        raise ValueError('Principal, simulation count and trial count must be positive.')
    if not all(0 <= x <= 1 for x in (win_percentage, risk, stop_loss)):
        raise ValueError('Win probability, risk and stop loss must be between 0 and 1.')

    rng = random.Random(seed)
    results, max_drawdowns, stop_outs = [], [], []
    stop_threshold = principal * (1 - stop_loss)

    for simulation_index in range(sim_num):
        money = principal
        highest_value = money
        highest_drawdown = 0.0

        for _ in range(runs_per_sim):
            risk_amount = risk * money
            if rng.random() < win_percentage:
                money += risk_amount
            else:
                money -= risk_amount

            highest_value = max(highest_value, money)
            drawdown = (highest_value - money) / highest_value * 100
            highest_drawdown = max(highest_drawdown, drawdown)

            if money <= stop_threshold:
                stop_outs.append(simulation_index + 1)
                break

        results.append(money)
        max_drawdowns.append(highest_drawdown)

    mean = statistics.mean(results)
    median = statistics.median(results)
    std = statistics.pstdev(results)
    best_value, worst_value = max(results), min(results)

    return {
        'principal': principal, 'sim_num': sim_num, 'runs_per_sim': runs_per_sim,
        'win_percentage': win_percentage, 'risk': risk, 'stop_loss': stop_loss,
        'mean': mean, 'median': median, 'std': std,
        'avg_profit': mean - principal,
        'avg_return': (mean / principal - 1) * 100,
        'median_return': (median / principal - 1) * 100,
        'best_sim_num': results.index(best_value) + 1,
        'best_sim': best_value,
        'best_return': (best_value / principal - 1) * 100,
        'worst_sim_num': results.index(worst_value) + 1,
        'worst_sim': worst_value,
        'worst_return': (worst_value / principal - 1) * 100,
        'worst_drawdown': max(max_drawdowns),
        'mean_max_drawdown': statistics.mean(max_drawdowns),
        'stop_outs': stop_outs,
        'stop_out_rate': len(stop_outs) / sim_num * 100,
        'profitable_rate': sum(x > principal for x in results) / sim_num * 100,
    }


def percentage_grid(start, end, step):
    if not (0 <= start <= end <= 100) or step <= 0:
        raise ValueError('Use percentages between 0 and 100, with positive step.')
    count = int(math.floor((end - start) / step + 1e-9))
    return [round((start + i * step) / 100, 10) for i in range(count + 1)]


def print_strategy(stats, index):
    print(f'\nStrategy #{index} | Risk: {stats["risk"]:.1%} | Stop loss: {stats["stop_loss"]:.1%}')
    print('-' * 65)
    print(f'Mean: {stats["mean"]:,.2f} | Median: {stats["median"]:,.2f} | Std: {stats["std"]:,.2f}')
    print(f'Average profit: {stats["avg_profit"]:,.2f} | Average return: {stats["avg_return"]:,.2f}%')
    print(f'Median return: {stats["median_return"]:,.2f}% | Profitable: {stats["profitable_rate"]:.1f}%')
    print(f'Best: #{stats["best_sim_num"]}, {stats["best_sim"]:,.2f}, return {stats["best_return"]:,.2f}%')
    print(f'Worst: #{stats["worst_sim_num"]}, {stats["worst_sim"]:,.2f}, return {stats["worst_return"]:,.2f}%')
    print(f'Worst max drawdown: {stats["worst_drawdown"]:.2f}% | Mean max drawdown: {stats["mean_max_drawdown"]:.2f}%')
    print(f'Stop-outs: {len(stats["stop_outs"])}/{stats["sim_num"]} ({stats["stop_out_rate"]:.1f}%)')


def export_csv(strategies, filename):
    columns = [key for key in strategies[0] if key != 'stop_outs']
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for strategy in strategies:
            writer.writerow({key: strategy[key] for key in columns})


def plot_landscapes(strategies, risks, stop_losses, output_dir):
    metrics = [
        ('median_return', 'Median return (%)'),
        ('avg_return', 'Mean return (%)'),
        ('stop_out_rate', 'Stop-out rate (%)'),
        ('mean_max_drawdown', 'Mean maximum drawdown (%)'),
    ]
    x, y = np.meshgrid(np.array(risks) * 100, np.array(stop_losses) * 100, indexing='ij')
    for key, label in metrics:
        z = np.array([s[key] for s in strategies], dtype=float).reshape(len(risks), len(stop_losses))
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        surface = ax.plot_surface(x, y, z, cmap='viridis', edgecolor='none')
        ax.set(xlabel='Risk per trial (%)', ylabel='Stop loss (%)', zlabel=label, title=f'Strategy landscape: {label}')
        fig.colorbar(surface, ax=ax, shrink=0.65, pad=0.12)
        fig.tight_layout()
        fig.savefig(output_dir / f'landscape_{key}.png', dpi=160)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 6))
        heatmap = ax.pcolormesh(x, y, z, shading='nearest', cmap='viridis')
        ax.set(xlabel='Risk per trial (%)', ylabel='Stop loss (%)', title=f'Heatmap: {label}')
        fig.colorbar(heatmap, ax=ax, label=label)
        fig.tight_layout()
        fig.savefig(output_dir / f'heatmap_{key}.png', dpi=160)
        plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter([s['std'] / s['principal'] * 100 for s in strategies],
                         [s['median_return'] for s in strategies],
                         c=[s['stop_out_rate'] for s in strategies], cmap='viridis')
    ax.set(xlabel='Std of ending balance (% of initial capital)', ylabel='Median return (%)',
           title='Risk-return comparison (color = stop-out rate)')
    fig.colorbar(scatter, ax=ax, label='Stop-out rate (%)')
    fig.tight_layout()
    fig.savefig(output_dir / 'risk_return_scatter.png', dpi=160)
    plt.close(fig)


def ask_float(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value) or (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            print('Please enter a valid number in the allowed range.')


def ask_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f'Please enter a whole number >= {minimum}.')


def main():
    print('MONTE CARLO SIMULATOR — V4')
    principal = ask_float('Initial principal: ', 0.0000001)
    sim_num = ask_int('Simulations per strategy: ')
    runs_per_sim = ask_int('Trials per simulation: ')
    win_percentage = ask_float('Win probability (%): ', 0, 100) / 100
    seed = ask_int('Random seed (whole number, e.g. 42): ', 0)
    mode = input('Mode: [1] Manual strategies [2] Parameter sweep: ').strip()
    strategies = []
    risks = stop_losses = None

    if mode == '1':
        count = ask_int('How many strategies? ')
        for i in range(count):
            print(f'\nStrategy #{i+1}')
            risk = ask_float('Risk per trial (%): ', 0, 100) / 100
            stop_loss = ask_float('Stop loss (% of initial principal): ', 0, 100) / 100
            strategies.append(run_strategy(principal, sim_num, runs_per_sim, win_percentage, risk, stop_loss, seed))
    elif mode == '2':
        print('\nRisk sweep')
        r_start = ask_float('Start risk (%): ', 0, 100)
        r_end = ask_float('End risk (%): ', r_start, 100)
        r_step = ask_float('Risk increment (%): ', 0.0000001)
        print('\nStop-loss sweep')
        s_start = ask_float('Start stop loss (%): ', 0, 100)
        s_end = ask_float('End stop loss (%): ', s_start, 100)
        s_step = ask_float('Stop-loss increment (%): ', 0.0000001)
        risks = percentage_grid(r_start, r_end, r_step)
        stop_losses = percentage_grid(s_start, s_end, s_step)
        total = len(risks) * len(stop_losses)
        print(f'\nRunning {total} strategies ({total * sim_num * runs_per_sim:,} maximum trials)...')
        for risk in risks:
            for stop_loss in stop_losses:
                strategies.append(run_strategy(principal, sim_num, runs_per_sim, win_percentage, risk, stop_loss, seed))
        print('Parameter sweep complete.')
    else:
        print('Unknown mode. Choose 1 or 2.')
        return

    if len(strategies) <= 10:
        for i, stats in enumerate(strategies, 1):
            print_strategy(stats, i)
    else:
        print(f'\nCompleted {len(strategies)} strategies. Showing leaders only.')

    for metric, label, choose in [
        ('median_return', 'Highest median return', max),
        ('avg_return', 'Highest mean return', max),
        ('stop_out_rate', 'Lowest stop-out rate', min),
        ('mean_max_drawdown', 'Lowest average max drawdown', min),
    ]:
        winner = choose(strategies, key=lambda s: s[metric])
        print(f'{label}: risk {winner["risk"]:.1%}, stop loss {winner["stop_loss"]:.1%}, {winner[metric]:,.2f}%')

    output_dir = Path('v4_results')
    output_dir.mkdir(exist_ok=True)
    export_csv(strategies, output_dir / 'strategy_results.csv')
    if mode == '2' and len(risks) >= 2 and len(stop_losses) >= 2:
        plot_landscapes(strategies, risks, stop_losses, output_dir)
        print('Saved 3D landscapes, heatmaps, and risk-return scatter plot.')
    else:
        print('For surface plots, use sweep mode with at least 2 values on each axis.')
    print(f'Output folder: {output_dir.resolve()}')


if __name__ == '__main__':
    main()
