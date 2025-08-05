"""
Bayesian Change Point Model for Brent oil price analysis.
Uses PyMC3 to detect structural breaks in time series data.
"""

import numpy as np
import pandas as pd
import pymc3 as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')

class BayesianChangePointModel:
    """
    Bayesian Change Point Model for detecting structural breaks in time series.
    """
    
    def __init__(self, data: np.ndarray, time_index: np.ndarray):
        """
        Initialize the change point model.
        
        Args:
            data (np.ndarray): Time series data (prices or returns)
            time_index (np.ndarray): Time index for the data
        """
        self.data = data
        self.time_index = time_index
        self.model = None
        self.trace = None
        self.summary = None
        
    def build_model(self, model_type: str = 'mean_shift') -> pm.Model:
        """
        Build the Bayesian change point model.
        
        Args:
            model_type (str): Type of model - 'mean_shift' or 'volatility_shift'
            
        Returns:
            pm.Model: PyMC3 model
        """
        n_data = len(self.data)
        
        with pm.Model() as model:
            # Prior for the change point (tau)
            # Uniform prior over all possible change points
            tau = pm.DiscreteUniform('tau', lower=0, upper=n_data-1)
            
            if model_type == 'mean_shift':
                # Priors for means before and after change point
                mu_1 = pm.Normal('mu_1', mu=0, sigma=10)
                mu_2 = pm.Normal('mu_2', mu=0, sigma=10)
                
                # Prior for standard deviation
                sigma = pm.HalfNormal('sigma', sigma=1)
                
                # Use switch function to select appropriate mean
                mu = pm.math.switch(tau >= self.time_index, mu_1, mu_2)
                
                # Likelihood
                likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=self.data)
                
            elif model_type == 'volatility_shift':
                # Priors for mean (assumed constant)
                mu = pm.Normal('mu', mu=0, sigma=10)
                
                # Priors for standard deviations before and after change point
                sigma_1 = pm.HalfNormal('sigma_1', sigma=1)
                sigma_2 = pm.HalfNormal('sigma_2', sigma=1)
                
                # Use switch function to select appropriate standard deviation
                sigma = pm.math.switch(tau >= self.time_index, sigma_1, sigma_2)
                
                # Likelihood
                likelihood = pm.Normal('likelihood', mu=mu, sigma=sigma, observed=self.data)
                
            else:
                raise ValueError("model_type must be 'mean_shift' or 'volatility_shift'")
        
        self.model = model
        return model
    
    def sample(self, draws: int = 2000, tune: int = 1000, chains: int = 4) -> az.InferenceData:
        """
        Sample from the posterior distribution using MCMC.
        
        Args:
            draws (int): Number of draws per chain
            tune (int): Number of tuning steps
            chains (int): Number of chains
            
        Returns:
            az.InferenceData: ArviZ inference data object
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        with self.model:
            # Use NUTS sampler
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                return_inferencedata=True,
                random_seed=42
            )
        
        return self.trace
    
    def check_convergence(self) -> Dict:
        """
        Check MCMC convergence diagnostics.
        
        Returns:
            Dict: Convergence diagnostics
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        # Get summary statistics
        self.summary = pm.summary(self.trace)
        
        # Check R-hat values (should be close to 1.0)
        r_hat_values = self.summary['r_hat']
        converged = all(r_hat < 1.1 for r_hat in r_hat_values)
        
        # Check effective sample size
        ess_values = self.summary['ess_bulk']
        min_ess = ess_values.min()
        
        diagnostics = {
            'converged': converged,
            'r_hat_max': r_hat_values.max(),
            'r_hat_min': r_hat_values.min(),
            'min_ess': min_ess,
            'summary': self.summary
        }
        
        return diagnostics
    
    def get_change_point_posterior(self) -> np.ndarray:
        """
        Get the posterior distribution of the change point.
        
        Returns:
            np.ndarray: Posterior samples of the change point
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        return self.trace.posterior['tau'].values.flatten()
    
    def get_parameter_posteriors(self) -> Dict:
        """
        Get posterior distributions of model parameters.
        
        Returns:
            Dict: Dictionary of parameter posteriors
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        posteriors = {}
        for var in self.trace.posterior.data_vars:
            posteriors[var] = self.trace.posterior[var].values.flatten()
        
        return posteriors
    
    def plot_trace(self, figsize: Tuple[int, int] = (12, 8)):
        """
        Plot MCMC trace plots for convergence diagnostics.
        
        Args:
            figsize (Tuple[int, int]): Figure size
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        pm.plot_trace(self.trace, figsize=figsize)
        plt.tight_layout()
        plt.show()
    
    def plot_change_point_posterior(self, figsize: Tuple[int, int] = (10, 6)):
        """
        Plot the posterior distribution of the change point.
        
        Args:
            figsize (Tuple[int, int]): Figure size
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_posterior = self.get_change_point_posterior()
        
        plt.figure(figsize=figsize)
        plt.hist(tau_posterior, bins=50, alpha=0.7, density=True)
        plt.axvline(tau_posterior.mean(), color='red', linestyle='--', 
                   label=f'Mean: {tau_posterior.mean():.0f}')
        plt.axvline(np.percentile(tau_posterior, 50), color='green', linestyle='--',
                   label=f'Median: {np.percentile(tau_posterior, 50):.0f}')
        plt.xlabel('Change Point (Time Index)')
        plt.ylabel('Density')
        plt.title('Posterior Distribution of Change Point')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def plot_data_with_change_point(self, dates: pd.Series = None, 
                                  figsize: Tuple[int, int] = (12, 6)):
        """
        Plot the data with the estimated change point.
        
        Args:
            dates (pd.Series): Date series for x-axis
            figsize (Tuple[int, int]): Figure size
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_posterior = self.get_change_point_posterior()
        mean_tau = tau_posterior.mean()
        
        plt.figure(figsize=figsize)
        
        if dates is not None:
            plt.plot(dates, self.data, alpha=0.7, label='Data')
            change_date = dates.iloc[int(mean_tau)]
            plt.axvline(change_date, color='red', linestyle='--', 
                       label=f'Estimated Change Point: {change_date.strftime("%Y-%m-%d")}')
        else:
            plt.plot(self.time_index, self.data, alpha=0.7, label='Data')
            plt.axvline(mean_tau, color='red', linestyle='--', 
                       label=f'Estimated Change Point: {mean_tau:.0f}')
        
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.title('Data with Estimated Change Point')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def compare_regimes(self) -> Dict:
        """
        Compare the statistical properties of the two regimes.
        
        Returns:
            Dict: Comparison statistics
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        tau_posterior = self.get_change_point_posterior()
        mean_tau = int(tau_posterior.mean())
        
        # Split data into two regimes
        regime_1 = self.data[:mean_tau]
        regime_2 = self.data[mean_tau:]
        
        comparison = {
            'regime_1': {
                'mean': np.mean(regime_1),
                'std': np.std(regime_1),
                'count': len(regime_1)
            },
            'regime_2': {
                'mean': np.mean(regime_2),
                'std': np.std(regime_2),
                'count': len(regime_2)
            },
            'change_point': mean_tau,
            'change_point_credible_interval': [
                np.percentile(tau_posterior, 2.5),
                np.percentile(tau_posterior, 97.5)
            ]
        }
        
        return comparison
    
    def find_multiple_change_points(self, max_change_points: int = 3) -> List[Dict]:
        """
        Find multiple change points using a hierarchical approach.
        
        Args:
            max_change_points (int): Maximum number of change points to find
            
        Returns:
            List[Dict]: List of change point results
        """
        change_points = []
        remaining_data = self.data.copy()
        remaining_time = self.time_index.copy()
        
        for i in range(max_change_points):
            if len(remaining_data) < 100:  # Need sufficient data
                break
                
            # Fit single change point model
            model = BayesianChangePointModel(remaining_data, remaining_time)
            model.build_model('mean_shift')
            trace = model.sample(draws=1000, tune=500, chains=2)
            
            # Get change point
            tau_posterior = model.get_change_point_posterior()
            mean_tau = int(tau_posterior.mean())
            
            # Check if change point is meaningful
            comparison = model.compare_regimes()
            mean_diff = abs(comparison['regime_1']['mean'] - comparison['regime_2']['mean'])
            
            if mean_diff < 0.1 * np.std(remaining_data):  # Small change
                break
            
            # Store result
            change_points.append({
                'iteration': i + 1,
                'change_point': mean_tau,
                'absolute_change_point': len(self.data) - len(remaining_data) + mean_tau,
                'comparison': comparison
            })
            
            # Update data for next iteration
            remaining_data = remaining_data[mean_tau:]
            remaining_time = remaining_time[mean_tau:]
        
        return change_points

def main():
    """
    Example usage of the BayesianChangePointModel class.
    """
    # This would be used with actual data
    print("Bayesian Change Point Model initialized.")
    print("Use with DataPreparator to analyze Brent oil prices.")

if __name__ == "__main__":
    main()
