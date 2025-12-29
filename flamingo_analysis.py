#!/usr/bin/env python3
"""
Flamingo Population Data Analytics
A comprehensive analysis of global flamingo populations, behaviors, and geographic distribution.

Author: Data Analytics Team
Version: 1.0.0
Date: December 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 8)

class FlamingoAnalytics:
    """
    Main class for conducting flamingo population analytics.
    
    This class handles data loading, processing, analysis, and visualization
    of flamingo population data across regions and species.
    """
    
    def __init__(self, data_file):
        """
        Initialize the FlamingoAnalytics class.
        
        Args:
            data_file (str): Path to the CSV file containing flamingo data
        """
        self.data_file = data_file
        self.df = None
        self.load_data()
        
    def load_data(self):
        """
        Load flamingo data from CSV file.
        Performs basic data validation and cleaning.
        """
        print("[*] Loading flamingo population data...")
        try:
            self.df = pd.read_csv(self.data_file)
            print(f"[+] Successfully loaded {len(self.df)} records")
            print(f"[+] Columns: {', '.join(self.df.columns.tolist())}\n")
        except FileNotFoundError:
            print(f"[!] Error: File '{self.data_file}' not found")
            raise
        except Exception as e:
            print(f"[!] Error loading data: {e}")
            raise
    
    def exploratory_analysis(self):
        """
        Perform exploratory data analysis (EDA).
        Displays summary statistics and data quality information.
        """
        print("=" * 70)
        print("EXPLORATORY DATA ANALYSIS")
        print("=" * 70)
        print("\n[*] Data Shape:", self.df.shape)
        print("\n[*] First 5 records:")
        print(self.df.head())
        print("\n[*] Data Types:")
        print(self.df.dtypes)
        print("\n[*] Missing Values:")
        print(self.df.isnull().sum())
        print("\n[*] Summary Statistics:")
        print(self.df.describe())
        print("\n")
    
    def population_analysis(self):
        """
        Analyze population trends and statistics.
        Calculates growth rates, comparisons, and distributions.
        """
        print("=" * 70)
        print("POPULATION ANALYSIS")
        print("=" * 70)
        
        # Calculate growth rate
        if 'population_2020' in self.df.columns and 'population_2023' in self.df.columns:
            self.df['growth_rate'] = ((self.df['population_2023'] - self.df['population_2020']) / 
                                      self.df['population_2020'] * 100)
            avg_growth = self.df['growth_rate'].mean()
            print(f"\n[+] Average Population Growth Rate (2020-2023): {avg_growth:.2f}%")
            
            total_2020 = self.df['population_2020'].sum()
            total_2023 = self.df['population_2023'].sum()
            print(f"[+] Total Population 2020: {total_2020:,.0f}")
            print(f"[+] Total Population 2023: {total_2023:,.0f}")
            print(f"[+] Overall Growth: {((total_2023 - total_2020) / total_2020 * 100):.2f}%")
        
        # Species analysis
        if 'species' in self.df.columns:
            print("\n[*] Population by Species (2023):")
            species_pop = self.df.groupby('species')['population_2023'].sum().sort_values(ascending=False)
            for species, pop in species_pop.items():
                percentage = (pop / species_pop.sum()) * 100
                print(f"  - {species}: {pop:,.0f} ({percentage:.1f}%)")
        
        print("\n")
    
    def geographic_analysis(self):
        """
        Analyze geographic distribution of flamingo populations.
        """
        print("=" * 70)
        print("GEOGRAPHIC DISTRIBUTION ANALYSIS")
        print("=" * 70)
        
        if 'region' in self.df.columns:
            print("\n[*] Population Distribution by Region (2023):")
            region_pop = self.df.groupby('region')['population_2023'].sum().sort_values(ascending=False)
            for region, pop in region_pop.items():
                percentage = (pop / region_pop.sum()) * 100
                print(f"  - {region}: {pop:,.0f} ({percentage:.1f}%)")
        
        if 'habitat_type' in self.df.columns:
            print("\n[*] Habitat Type Distribution:")
            habitat_dist = self.df['habitat_type'].value_counts()
            for habitat, count in habitat_dist.items():
                percentage = (count / len(self.df)) * 100
                print(f"  - {habitat}: {count} records ({percentage:.1f}%)")
        
        print("\n")
    
    def conservation_status_analysis(self):
        """
        Analyze conservation status of flamingo populations.
        """
        print("=" * 70)
        print("CONSERVATION STATUS ANALYSIS")
        print("=" * 70)
        
        if 'conservation_status' in self.df.columns:
            print("\n[*] Conservation Status Distribution:")
            cons_status = self.df['conservation_status'].value_counts()
            for status, count in cons_status.items():
                print(f"  - {status}: {count} species")
        
        print("\n")
    
    def statistical_tests(self):
        """
        Perform statistical tests on population data.
        """
        print("=" * 70)
        print("STATISTICAL ANALYSIS")
        print("=" * 70)
        
        if 'population_2023' in self.df.columns:
            pop_data = self.df['population_2023'].dropna()
            print(f"\n[+] Population Statistics (2023):")
            print(f"  - Mean: {pop_data.mean():,.0f}")
            print(f"  - Median: {pop_data.median():,.0f}")
            print(f"  - Std Dev: {pop_data.std():,.0f}")
            print(f"  - Min: {pop_data.min():,.0f}")
            print(f"  - Max: {pop_data.max():,.0f}")
            
            # Normality test
            stat, p_value = stats.shapiro(pop_data)
            print(f"  - Normality Test (Shapiro-Wilk): p-value = {p_value:.4f}")
        
        print("\n")
    
    def generate_visualizations(self):
        """
        Generate visualization charts from the data.
        """
        print("[*] Generating visualizations...")
        
        # Create output directory if it doesn't exist
        import os
        if not os.path.exists('outputs'):
            os.makedirs('outputs')
        
        # Visualization 1: Population by Species
        if 'species' in self.df.columns:
            fig, ax = plt.subplots(figsize=(12, 6))
            species_pop = self.df.groupby('species')['population_2023'].sum().sort_values()
            species_pop.plot(kind='barh', ax=ax, color='#FF69B4')
            ax.set_xlabel('Population Count')
            ax.set_ylabel('Species')
            ax.set_title('Flamingo Population by Species (2023)', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('outputs/species_distribution.png', dpi=300, bbox_inches='tight')
            print("[+] Saved: outputs/species_distribution.png")
            plt.close()
        
        # Visualization 2: Growth Rate
        if 'growth_rate' in self.df.columns and 'species' in self.df.columns:
            fig, ax = plt.subplots(figsize=(12, 6))
            self.df.plot(x='species', y='growth_rate', kind='bar', ax=ax, color='#00CED1')
            ax.set_ylabel('Growth Rate (%)')
            ax.set_xlabel('Species')
            ax.set_title('Population Growth Rate by Species (2020-2023)', fontsize=14, fontweight='bold')
            ax.axhline(y=0, color='red', linestyle='--', alpha=0.5)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('outputs/growth_rates.png', dpi=300, bbox_inches='tight')
            print("[+] Saved: outputs/growth_rates.png")
            plt.close()
        
        print("\n")
    
    def generate_report(self):
        """
        Generate a comprehensive text report.
        """
        print("[*] Generating analysis report...")
        with open('outputs/analysis_report.txt', 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("FLAMINGO POPULATION DATA ANALYTICS REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("PROJECT OVERVIEW\n")
            f.write("-" * 70 + "\n")
            f.write("This report contains a comprehensive analysis of global flamingo\n")
            f.write("populations, including demographic trends, geographic distribution,\n")
            f.write("and conservation status assessment.\n\n")
            
            f.write("KEY STATISTICS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Records Analyzed: {len(self.df)}\n")
            f.write(f"Date Generated: December 2025\n")
            f.write(f"Analysis Period: 2020-2023\n\n")
            
            f.write("For detailed analysis, see the main README.md file.\n")
        
        print("[+] Saved: outputs/analysis_report.txt")
    
    def run_full_analysis(self):
        """
        Execute the complete analysis pipeline.
        """
        print("\n" + "=" * 70)
        print("FLAMINGO POPULATION DATA ANALYTICS - FULL ANALYSIS")
        print("=" * 70 + "\n")
        
        self.exploratory_analysis()
        self.population_analysis()
        self.geographic_analysis()
        self.conservation_status_analysis()
        self.statistical_tests()
        self.generate_visualizations()
        self.generate_report()
        
        print("=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70 + "\n")
        print("[+] All results saved to the 'outputs' directory")
        print("[+] Generated files:")
        print("    - species_distribution.png")
        print("    - growth_rates.png")
        print("    - analysis_report.txt\n")


def main():
    """
    Main entry point for the analysis script.
    """
    # Initialize analytics with data file
    analytics = FlamingoAnalytics('data/flamingo_data.csv')
    
    # Run complete analysis
    analytics.run_full_analysis()


if __name__ == "__main__":
    main()
