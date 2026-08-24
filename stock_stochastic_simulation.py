import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. Data Collection and Preprocessing
# ==========================================
def fetch_stock_data(ticker, start_date, end_date):
    """Fetches and preprocesses historical stock data."""
    print(f"Fetching data for {ticker}...")
    data = yf.download(ticker, start=start_date, end=end_date)
    # Forward fill any missing values
    data = data.ffill()
    
    # Calculate daily log returns
    data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data = data.dropna()
    return data

# ==========================================
# 2. Geometric Brownian Motion (GBM)
# ==========================================
def simulate_gbm(S0, mu, sigma, T, dt, num_sims):
    """
    Simulates Geometric Brownian Motion.
    S0: Initial stock price
    mu: Drift (expected daily return)
    sigma: Volatility (daily standard deviation)
    T: Total time steps (days)
    dt: Time step size (typically 1 for daily)
    num_sims: Number of Monte Carlo simulations
    """
    # Create empty array for prices: (T+1) rows, num_sims columns
    prices = np.zeros((T + 1, num_sims))
    prices[0] = S0
    
    for t in range(1, T + 1):
        # Generate random standard normal values
        Z = np.random.standard_normal(num_sims)
        # Apply the GBM discrete formula
        prices[t] = prices[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)
        
    return prices

# ==========================================
# 3. Ornstein-Uhlenbeck Process (Mean-Reverting)
# ==========================================
def simulate_ou_process(S0, theta, mu_ou, sigma_ou, T, dt, num_sims):
    """
    Simulates the Ornstein-Uhlenbeck (Mean-Reverting) Process.
    theta: Speed of reversion
    mu_ou: Long-term mean price
    sigma_ou: Volatility of the process
    """
    prices = np.zeros((T + 1, num_sims))
    prices[0] = S0
    
    for t in range(1, T + 1):
        Z = np.random.standard_normal(num_sims)
        # Apply the OU discrete formula
        drift = theta * (mu_ou - prices[t-1]) * dt
        shock = sigma_ou * np.sqrt(dt) * Z
        prices[t] = prices[t-1] + drift + shock
        
        # Ensure prices don't drop below zero (simple boundary condition)
        prices[t] = np.maximum(prices[t], 0)
        
    return prices

# ==========================================
# 4. Execution and Visualization
# ==========================================
if __name__ == "__main__":
    # Parameters
    TICKER = "AAPL"
    START_DATE = "2023-01-01"
    END_DATE = "2024-01-01"
    DAYS_TO_SIMULATE = 60
    NUM_SIMULATIONS = 1000
    DT = 1 # 1 day

    # Fetch Data
    stock_data = fetch_stock_data(TICKER, START_DATE, END_DATE)
    
    # Derive parameters for GBM based on historical data
    current_price = stock_data['Close'].iloc[-1]
    daily_mu = stock_data['Log_Returns'].mean()
    daily_sigma = stock_data['Log_Returns'].std()
    
    # Run GBM Simulation
    gbm_paths = simulate_gbm(current_price, daily_mu, daily_sigma, DAYS_TO_SIMULATE, DT, NUM_SIMULATIONS)
    
    # Run OU Simulation (using arbitrary reversion parameters for demonstration)
    # In a real scenario, theta and mu_ou would be calibrated using linear regression
    theta_param = 0.1
    long_term_mean = current_price * 1.05 # Assuming a slight upward mean target
    ou_paths = simulate_ou_process(current_price, theta_param, long_term_mean, daily_sigma*current_price, DAYS_TO_SIMULATE, DT, NUM_SIMULATIONS)

    # Plotting
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # GBM Plot
    axes[0].plot(gbm_paths[:, :100], alpha=0.3, color='blue', linewidth=1) # Plot first 100 paths
    axes[0].plot(np.mean(gbm_paths, axis=1), color='red', linewidth=2, label='Mean Path')
    axes[0].set_title(f'Geometric Brownian Motion - {TICKER}')
    axes[0].set_xlabel('Days in Future')
    axes[0].set_ylabel('Price')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # OU Plot
    axes[1].plot(ou_paths[:, :100], alpha=0.3, color='green', linewidth=1)
    axes[1].plot(np.mean(ou_paths, axis=1), color='red', linewidth=2, label='Mean Path')
    axes[1].axhline(long_term_mean, color='black', linestyle='--', label='Long-Term Mean')
    axes[1].set_title(f'Ornstein-Uhlenbeck (Mean-Reverting) - {TICKER}')
    axes[1].set_xlabel('Days in Future')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()