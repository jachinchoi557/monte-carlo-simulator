# Monte Carlo Strategy Simulator — V4

A configurable fractional-betting Monte Carlo simulator with manual strategy testing and automated risk × stop-loss parameter sweeps.

## Setup

```bash
python -m pip install -r requirements.txt
python monte_carlo_v4.py
```

Choose mode 1 for manual comparison or mode 2 for a parameter sweep. Sweep mode saves a CSV, four 3D surface plots, four 2D heatmaps, and a risk-return scatter plot to `v4_results/`.

Suggested quick test: principal 1000, 100 simulations, 100 trials, 60% win probability, seed 42, mode 2, risk 5–25 by 5, stop loss 10–50 by 10.

## Definitions

- **Risk:** fraction of *current* portfolio value gained or lost on each independent even-payoff trial.
- **Stop loss:** maximum permitted decline from *initial* principal; simulation terminates when ending value after a trial is at or below `principal * (1 - stop_loss)`.
- **Stop-out:** threshold crossing, not bankruptcy. A discrete loss can overshoot the threshold.
- **Max drawdown:** largest observed percentage decline from the running portfolio peak, including the final loss that triggers a stop-out.
- **Median return:** percentage change between the median ending balance and initial principal.
- **Mean return:** arithmetic mean of ending-balance returns. It can be strongly affected by extreme winners.
- **Standard deviation:** population standard deviation of ending portfolio values.

The same random seed is used for each strategy to facilitate comparisons under matched trial outcomes. This is a simplified hypothetical process, **not** a validated trading model. Rankings are in-sample results and are not evidence of real-world optimality.

## Next steps

Add automated tests, compare convergence across simulation counts, validate against simple analytic cases, and consider out-of-sample evaluation before describing a configuration as optimal.
