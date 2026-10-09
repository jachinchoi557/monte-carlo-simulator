
# Monte Carlo Portfolio Risk Simulator

**Stochastic Modeling | Monte Carlo Methods | Quantitative Risk Analysis | Parameter Sensitivity | Python**

A Python-based quantitative research project using Monte Carlo simulation, stochastic modeling, and computational statistics to investigate portfolio growth, compounding dynamics, and risk-management strategies under probabilistic trading outcomes.

The simulator models portfolio evolution as a **discrete-time stochastic process**, incorporating configurable win probabilities, multiplicative position sizing, and path-dependent stop-loss constraints.

Through repeated random sampling, the framework generates empirical distributions of portfolio outcomes and evaluates performance using statistical measures including mean and median returns, standard deviation, maximum drawdown, and stop-out frequency.

V4 extends the framework with automated grid-search parameter sweeps, reproducible experiments, and multidimensional data visualization.

---

## Key Features

- **Stochastic portfolio simulation:** Repeated independent win/loss trials with configurable parameters.
- **Multiplicative compounding:** Position sizing based on current portfolio capital.
- **Quantitative risk metrics:** Return distributions, standard deviation, maximum drawdown, and stop-out rates.
- **Path-dependent risk analysis:** Portfolio trajectories with running peaks and stop-loss termination.
- **Parameter sensitivity analysis:** Automated grid search across risk and stop-loss configurations.
- **Reproducible experiments:** Seeded pseudorandom number generation and matched trial sequences.
- **Visualization:** 3D performance surfaces, heatmaps, and risk-return scatter plots.
- **Data export:** CSV files containing experiment results for further analysis.

## Mathematical Framework

### Stochastic Portfolio Evolution

Portfolio capital follows the discrete-time process:

$$
P_{t+1}=P_t(1+rX_t)
$$

where:

- $P_t$ is portfolio capital at trial $t$.
- $r$ is the fraction of current capital risked per trial.
- $X_t$ is the random outcome of a trial.
- $p$ is the probability of a winning outcome.

The outcome distribution is:

$$
X_t=
\begin{cases}
+1 & \text{with probability }p \\
-1 & \text{with probability }1-p
\end{cases}
$$

### Expected Return and Variance

The expected single-trial return is:

$$
\mathbb{E}[R_t]=r(2p-1)
$$

The single-trial return variance is:

$$
\mathrm{Var}(R_t)=4r^2p(1-p)
$$

Without early termination, expected portfolio capital after $n$ independent trials is:

$$
\mathbb{E}[P_n]=P_0[1+r(2p-1)]^n
$$

Stop-loss termination changes the distribution of completed paths.

### Maximum Drawdown

Define the running portfolio peak:

$$
H_t=\max_{0\leq k\leq t}P_k
$$

The drawdown at time $t$ is:

$$
D_t=\frac{H_t-P_t}{H_t}
$$

Maximum drawdown is:

$$
D_{\max}=\max_t D_t
$$

This is a path-dependent metric: two simulations with identical ending balances can have different maximum drawdowns.

### Stop-Loss Constraint

For initial principal $P_0$ and tolerated loss fraction $s$, a simulation terminates when:

$$
P_t\leq P_0(1-s)
$$

For example, a 20% stop loss on a $10,000 portfolio corresponds to an $8,000 threshold.

Stop-loss checks occur after each simulated trial, so the recorded ending balance may fall below the threshold.

## Development History

### V1 — Monte Carlo Fundamentals

- Randomized win/loss simulation
- Multiple independent simulation paths
- Portfolio balance tracking
- Mean, median, and standard deviation
- Best- and worst-performing simulations

### V2 — Risk Metrics

- Running portfolio peak tracking
- Maximum drawdown calculations
- Profitability and loss statistics
- Expanded statistical summaries

### V3 — Configurable Strategy Testing

- Reusable simulation function
- User-defined principal and win probability
- Percentage-based position sizing
- Stop-loss thresholds relative to initial capital
- Multiple strategy comparisons
- Compounded portfolio outcomes

### V4 — Automated Parameter Search and Visualization

- Manual and automated testing modes
- Grid-search parameter sweeps
- Reproducible seeded simulations
- Matched random sequences for controlled comparisons
- 3D performance landscapes
- Parameter sensitivity heatmaps
- Risk-return scatter plots
- Strategy rankings by selected metrics
- CSV data export

## Parameter Sensitivity Analysis

V4 evaluates combinations of position-sizing and stop-loss parameters while holding other experiment settings constant.

Example experiment:

| Parameter | Value |
|---|---|
| Initial principal | $10,000 |
| Win probability | 55% |
| Simulations per strategy | 1,000 |
| Trials per simulation | 100 |
| Risk per trial | 5%, 10%, 15%, 20% |
| Stop-loss threshold | 10%, 20%, 30%, 40% |

This creates **16 distinct parameter configurations**, each evaluated across 1,000 simulated portfolio paths.

For each configuration, the simulator estimates performance metrics conditional on the model assumptions.

The resulting parameter grid enables systematic comparisons of simulated risk and return.

**Grid search identifies the best configurations within the tested parameter space, not globally optimal real-world trading strategies.**

## Visualizations

### 3D Performance Landscapes

Three-dimensional surface plots represent:

- **X-axis:** Risk per trial (%)
- **Y-axis:** Stop-loss threshold (%)
- **Z-axis:** Selected performance metric

Metrics include median return, mean return, stop-out rate, and mean maximum drawdown.

### Parameter Sensitivity Heatmaps

Heatmaps visualize the same parameter grid using color intensity, making it easier to compare regions with different simulated risk-return characteristics.

### Risk-Return Scatter Plot

Each point represents a tested strategy configuration:

- **X-axis:** Standard deviation of ending portfolio balances normalized by initial capital
- **Y-axis:** Median simulated return
- **Color:** Stop-out rate

This enables comparison of typical simulated returns, terminal-outcome dispersion, and downside exposure.

The normalized standard deviation is not annualized market volatility.

## Reproducibility

The simulator supports configurable pseudorandom seeds.

Using consistent seeds across configurations produces matched trial sequences, an approach related to the **common random numbers** variance-reduction technique.

This supports more controlled comparisons, debugging, and repeatable experiments.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Simulation engine and experiment orchestration |
| NumPy | Numerical arrays and multidimensional parameter grids |
| Matplotlib | 3D plots, heatmaps, and scatter plots |
| Python standard library | Random-number generation, statistics, and CSV export |
| Git / GitHub | Version control and project documentation |

## Repository Structure

```text
monte-carlo-simulator/
├── monte-carlo.py
├── monte_carlo_v4/
│   ├── monte_carlo_v4.py
│   ├── requirements.txt
│   └── README.md
├── .gitignore
└── README.md
```

## Installation and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/jachinchoi557/monte-carlo-simulator.git
cd monte-carlo-simulator
```

### 2. Install Dependencies

On Windows:

```powershell
py -m pip install -r monte_carlo_v4/requirements.txt
```

### 3. Run V4

```powershell
py monte_carlo_v4/monte_carlo_v4.py
```

**Mode 1 — Manual Strategy Testing:** Evaluate individual user-defined configurations.

**Mode 2 — Automated Parameter Sweep:** Test combinations of risk and stop-loss values, generate visualizations, and export results.

## Model Assumptions and Limitations

This project uses a simplified probabilistic model rather than historical market data.

Assumptions include:

- Independent win/loss outcomes
- Constant win probability
- Symmetric percentage gains and losses
- Position sizing proportional to current portfolio capital
- Stop-loss evaluation after discrete trials
- No transaction costs, slippage, or market impact
- No asset correlations or changing market regimes

The simulator does not perform historical backtesting, predictive alpha modeling, or live trading.

Results are conditional on model assumptions, parameter selection, and sampling variability.

## Future Extensions

- Asymmetric win/loss payoffs
- Transaction costs and slippage
- Correlated and fat-tailed return distributions
- Time-varying market regimes
- Confidence intervals and convergence analysis
- Additional risk-adjusted performance metrics
- Out-of-sample parameter validation
- Historical-data integration

## Project Purpose

Developed as an independent programming and quantitative analysis project exploring the intersection of **probability theory, stochastic processes, computational statistics, and quantitative risk management**.

The project demonstrates progression from a basic Monte Carlo simulation to a modular framework for evaluating compounding dynamics, path-dependent risk, and parameter sensitivity through reproducible numerical experiments.

---

**Disclaimer:** This project is for educational and computational research purposes only. It does not constitute financial advice or a validated investment strategy.
  
