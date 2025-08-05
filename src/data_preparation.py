"""
Data preparation module for Brent oil price analysis.
Handles loading, cleaning, and preprocessing of time series data.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataPreparator:
    """
    Class for preparing and preprocessing Brent oil price data.
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the data preparator.
        
        Args:
            data_path (str): Path to the CSV file containing Brent oil prices
        """
        self.data_path = data_path
        self.raw_data = None
        self.processed_data = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load the Brent oil price data from CSV.
        
        Returns:
            pd.DataFrame: Raw data with Date and Price columns
        """
        try:
            # Load data with custom date parser that handles multiple formats
            def parse_date(date_str):
                """Parse dates in multiple formats."""
                # Remove quotes if present
                date_str = date_str.strip('"')
                
                # Try DD-MMM-YY format first (e.g., "20-May-87")
                try:
                    return pd.to_datetime(date_str, format='%d-%b-%y')
                except ValueError:
                    pass
                
                # Try MMM DD, YYYY format (e.g., "Apr 22, 2020")
                try:
                    return pd.to_datetime(date_str, format='%b %d, %Y')
                except ValueError:
                    pass
                
                # Try other common formats
                try:
                    return pd.to_datetime(date_str)
                except ValueError:
                    raise ValueError(f"Unable to parse date: {date_str}")
            
            self.raw_data = pd.read_csv(
                self.data_path,
                parse_dates=['Date'],
                date_parser=parse_date
            )
            
            print(f"Data loaded successfully: {len(self.raw_data)} records")
            print(f"Date range: {self.raw_data['Date'].min()} to {self.raw_data['Date'].max()}")
            
            return self.raw_data
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean the data by handling missing values and outliers.
        
        Returns:
            pd.DataFrame: Cleaned data
        """
        if self.raw_data is None:
            print("No data loaded. Please load data first.")
            return None
        
        # Create a copy for cleaning
        cleaned_data = self.raw_data.copy()
        
        # Check for missing values
        missing_values = cleaned_data.isnull().sum()
        if missing_values.sum() > 0:
            print(f"Missing values found:\n{missing_values}")
        
        # Remove rows with missing values
        cleaned_data = cleaned_data.dropna()
        
        # Sort by date
        cleaned_data = cleaned_data.sort_values('Date').reset_index(drop=True)
        
        # Check for outliers using IQR method
        Q1 = cleaned_data['Price'].quantile(0.25)
        Q3 = cleaned_data['Price'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = cleaned_data[
            (cleaned_data['Price'] < lower_bound) | 
            (cleaned_data['Price'] > upper_bound)
        ]
        
        if len(outliers) > 0:
            print(f"Found {len(outliers)} outliers (using IQR method)")
            print(f"Outlier price range: ${outliers['Price'].min():.2f} - ${outliers['Price'].max():.2f}")
        
        # For this analysis, we'll keep outliers as they might represent significant events
        # but we'll log them for reference
        
        self.processed_data = cleaned_data
        return cleaned_data
    
    def calculate_returns(self, method: str = 'log') -> pd.DataFrame:
        """
        Calculate returns from price data.
        
        Args:
            method (str): 'log' for log returns, 'simple' for simple returns
            
        Returns:
            pd.DataFrame: Data with returns column added
        """
        if self.processed_data is None:
            print("No processed data available. Please clean data first.")
            return None
        
        data_with_returns = self.processed_data.copy()
        
        if method == 'log':
            data_with_returns['Returns'] = np.log(data_with_returns['Price'] / data_with_returns['Price'].shift(1))
        elif method == 'simple':
            data_with_returns['Returns'] = (data_with_returns['Price'] - data_with_returns['Price'].shift(1)) / data_with_returns['Price'].shift(1)
        else:
            raise ValueError("Method must be 'log' or 'simple'")
        
        # Remove the first row which will have NaN return
        data_with_returns = data_with_returns.dropna().reset_index(drop=True)
        
        return data_with_returns
    
    def get_summary_statistics(self) -> dict:
        """
        Get summary statistics for the price data.
        
        Returns:
            dict: Summary statistics
        """
        if self.processed_data is None:
            print("No processed data available.")
            return {}
        
        stats = {
            'total_records': len(self.processed_data),
            'date_range': {
                'start': self.processed_data['Date'].min(),
                'end': self.processed_data['Date'].max(),
                'duration_days': (self.processed_data['Date'].max() - self.processed_data['Date'].min()).days
            },
            'price_statistics': {
                'mean': self.processed_data['Price'].mean(),
                'median': self.processed_data['Price'].median(),
                'std': self.processed_data['Price'].std(),
                'min': self.processed_data['Price'].min(),
                'max': self.processed_data['Price'].max(),
                'q25': self.processed_data['Price'].quantile(0.25),
                'q75': self.processed_data['Price'].quantile(0.75)
            }
        }
        
        return stats
    
    def prepare_for_modeling(self, use_returns: bool = True) -> tuple:
        """
        Prepare data for Bayesian change point modeling.
        
        Args:
            use_returns (bool): Whether to use returns instead of prices
            
        Returns:
            tuple: (data, time_index, values)
        """
        if use_returns:
            data = self.calculate_returns()
            values = data['Returns'].values
        else:
            data = self.processed_data
            values = data['Price'].values
        
        # Create time index (0, 1, 2, ...)
        time_index = np.arange(len(values))
        
        return data, time_index, values
    
    def get_event_data(self) -> pd.DataFrame:
        """
        Create a sample event dataset with major geopolitical and economic events.
        This is a starting point - you should expand this with more comprehensive research.
        
        Returns:
            pd.DataFrame: Event data with dates and descriptions
        """
        events = [
            {'date': '1990-08-02', 'event': 'Iraq invades Kuwait', 'category': 'conflict'},
            {'date': '1991-01-17', 'event': 'Gulf War begins', 'category': 'conflict'},
            {'date': '2001-09-11', 'event': '9/11 attacks', 'category': 'terrorism'},
            {'date': '2003-03-20', 'event': 'Iraq War begins', 'category': 'conflict'},
            {'date': '2008-09-15', 'event': 'Lehman Brothers bankruptcy', 'category': 'financial'},
            {'date': '2011-02-15', 'event': 'Libyan civil war begins', 'category': 'conflict'},
            {'date': '2014-06-13', 'event': 'ISIS captures Mosul', 'category': 'conflict'},
            {'date': '2016-11-30', 'event': 'OPEC production cut agreement', 'category': 'policy'},
            {'date': '2020-03-11', 'event': 'COVID-19 declared pandemic', 'category': 'health'},
            {'date': '2020-04-20', 'event': 'WTI crude goes negative', 'category': 'financial'},
            {'date': '2022-02-24', 'event': 'Russia invades Ukraine', 'category': 'conflict'},
            {'date': '2022-10-05', 'event': 'OPEC+ production cut', 'category': 'policy'}
        ]
        
        event_df = pd.DataFrame(events)
        event_df['date'] = pd.to_datetime(event_df['date'])
        
        return event_df

def main():
    """
    Example usage of the DataPreparator class.
    """
    # Initialize data preparator with correct path
    import os
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, 'data', 'raw', 'BrentOilPrices.csv')
    
    preparator = DataPreparator(data_path)
    
    # Load and clean data
    raw_data = preparator.load_data()
    if raw_data is None:
        print("Failed to load data. Please check the file path.")
        return None
        
    cleaned_data = preparator.clean_data()
    if cleaned_data is None:
        print("Failed to clean data.")
        return None
    
    # Get summary statistics
    stats = preparator.get_summary_statistics()
    if stats:
        print("\nSummary Statistics:")
        print(f"Total records: {stats['total_records']}")
        print(f"Date range: {stats['date_range']['start']} to {stats['date_range']['end']}")
        print(f"Duration: {stats['date_range']['duration_days']} days")
        print(f"Price range: ${stats['price_statistics']['min']:.2f} - ${stats['price_statistics']['max']:.2f}")
        print(f"Mean price: ${stats['price_statistics']['mean']:.2f}")
    else:
        print("No statistics available.")
    
    # Get event data
    events = preparator.get_event_data()
    print(f"\nSample events: {len(events)} major events identified")
    
    return preparator

if __name__ == "__main__":
    main()
