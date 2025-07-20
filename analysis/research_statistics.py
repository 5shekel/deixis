"""
Research Statistics Module
Provides statistical analysis capabilities for the deictic ethics research.
Supports hypothesis testing and pattern analysis across models and framings.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from scipy import stats
from scipy.stats import chi2_contingency, kruskal
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ResearchStatistics:
    """Statistical analysis for deictic ethics research."""
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize with optional data path."""
        self.data_path = data_path
        self.data = None
        self.results = {}
        
    def load_research_data(self, csv_path: str) -> pd.DataFrame:
        """Load research data from CSV export."""
        try:
            self.data = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(self.data)} responses for analysis")
            return self.data
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def descriptive_statistics(self) -> Dict:
        """Generate descriptive statistics for all variables."""
        if self.data is None:
            return {}
        
        stats = {
            'sample_size': len(self.data),
            'models': self.data['model'].value_counts().to_dict(),
            'framings': self.data['framing'].value_counts().to_dict(),
            'ethical_modes': self.data['ethical_mode'].value_counts().to_dict(),
            'variable_means': {},
            'variable_stds': {}
        }
        
        # Continuous variables
        continuous_vars = [
            'pronoun_usage', 'role_assumption', 'perspective_complexity',
            'distributed_agency', 'deictic_reframing', 'stance_clarity',
            'moral_plurality', 'ontological_perspective', 'shamanic_cosmological_markers',
            'reasoning_steps_count', 'dialogic_simulation'
        ]
        
        for var in continuous_vars:
            if var in self.data.columns:
                stats['variable_means'][var] = self.data[var].mean()
                stats['variable_stds'][var] = self.data[var].std()
        
        return stats
    
    def test_deictic_framing_effects(self) -> Dict:
        """Test main effects of deictic framing on ethical variables."""
        if self.data is None:
            return {}
        
        results = {}
        
        # Variables to test
        dependent_vars = [
            'pronoun_usage', 'role_assumption', 'perspective_complexity',
            'distributed_agency', 'deictic_reframing', 'stance_clarity',
            'moral_plurality', 'ontological_perspective', 'shamanic_cosmological_markers',
            'reasoning_steps_count', 'dialogic_simulation'
        ]
        
        for var in dependent_vars:
            if var in self.data.columns:
                # Group by framing
                groups = [group[var].values for name, group in self.data.groupby('framing')]
                
                # Kruskal-Wallis test (non-parametric ANOVA)
                try:
                    h_stat, p_value = kruskal(*groups)
                    results[var] = {
                        'h_statistic': h_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'effect_size': self._calculate_eta_squared(groups)
                    }
                except Exception as e:
                    results[var] = {'error': str(e)}
        
        return results
    
    def test_model_differences(self) -> Dict:
        """Test differences between models on ethical variables."""
        if self.data is None:
            return {}
        
        results = {}
        
        dependent_vars = [
            'pronoun_usage', 'role_assumption', 'perspective_complexity',
            'distributed_agency', 'deictic_reframing', 'stance_clarity',
            'moral_plurality', 'ontological_perspective', 'shamanic_cosmological_markers',
            'reasoning_steps_count', 'dialogic_simulation'
        ]
        
        for var in dependent_vars:
            if var in self.data.columns:
                # Group by model
                groups = [group[var].values for name, group in self.data.groupby('model')]
                
                try:
                    h_stat, p_value = kruskal(*groups)
                    results[var] = {
                        'h_statistic': h_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'effect_size': self._calculate_eta_squared(groups)
                    }
                except Exception as e:
                    results[var] = {'error': str(e)}
        
        return results
    
    def test_ethical_mode_associations(self) -> Dict:
        """Test associations between deictic framing and ethical modes."""
        if self.data is None or 'ethical_mode' not in self.data.columns:
            return {}
        
        # Create contingency table
        contingency = pd.crosstab(self.data['framing'], self.data['ethical_mode'])
        
        # Chi-square test
        try:
            chi2, p_value, dof, expected = chi2_contingency(contingency)
            
            # Cramér's V (effect size)
            n = contingency.sum().sum()
            cramers_v = np.sqrt(chi2 / (n * (min(contingency.shape) - 1)))
            
            return {
                'contingency_table': contingency.to_dict(),
                'chi2_statistic': chi2,
                'p_value': p_value,
                'degrees_of_freedom': dof,
                'cramers_v': cramers_v,
                'significant': p_value < 0.05
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_shamanic_hypothesis(self) -> Dict:
        """Test specific hypothesis about shamanic/cosmological framings."""
        if self.data is None:
            return {}
        
        # Filter shamanic/cosmological vs other framings
        shamanic_data = self.data[self.data['framing'] == 'shamanic']
        other_data = self.data[self.data['framing'] != 'shamanic']
        
        results = {}
        
        # Test variables expected to be higher in shamanic framings
        shamanic_vars = [
            'distributed_agency', 'moral_plurality', 'ontological_perspective',
            'shamanic_cosmological_markers'
        ]
        
        for var in shamanic_vars:
            if var in self.data.columns:
                try:
                    # Mann-Whitney U test
                    u_stat, p_value = stats.mannwhitneyu(
                        shamanic_data[var], other_data[var], 
                        alternative='greater'
                    )
                    
                    results[var] = {
                        'shamanic_mean': shamanic_data[var].mean(),
                        'other_mean': other_data[var].mean(),
                        'u_statistic': u_stat,
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'effect_size': self._calculate_cohens_d(
                            shamanic_data[var], other_data[var]
                        )
                    }
                except Exception as e:
                    results[var] = {'error': str(e)}
        
        return results
    
    def analyze_interaction_effects(self) -> Dict:
        """Analyze interaction effects between framing and model."""
        if self.data is None:
            return {}
        
        results = {}
        
        # For each dependent variable, test framing × model interaction
        dependent_vars = [
            'pronoun_usage', 'role_assumption', 'perspective_complexity',
            'ethical_mode', 'distributed_agency', 'moral_plurality'
        ]
        
        for var in dependent_vars:
            if var in self.data.columns:
                try:
                    # Create interaction groups
                    interaction_groups = []
                    group_labels = []
                    
                    for framing in self.data['framing'].unique():
                        for model in self.data['model'].unique():
                            subset = self.data[
                                (self.data['framing'] == framing) & 
                                (self.data['model'] == model)
                            ]
                            if len(subset) > 0:
                                if var == 'ethical_mode':
                                    # For categorical variables, use mode
                                    interaction_groups.append(subset[var].mode().iloc[0] if len(subset[var].mode()) > 0 else 'Unknown')
                                else:
                                    interaction_groups.append(subset[var].mean())
                                group_labels.append(f"{framing}_{model}")
                    
                    results[var] = {
                        'group_means': dict(zip(group_labels, interaction_groups)),
                        'analysis_type': 'interaction_effect'
                    }
                    
                except Exception as e:
                    results[var] = {'error': str(e)}
        
        return results
    
    def _calculate_eta_squared(self, groups: List) -> float:
        """Calculate eta-squared effect size."""
        try:
            # Convert to arrays
            all_data = np.concatenate(groups)
            grand_mean = np.mean(all_data)
            
            # Between-group sum of squares
            ss_between = sum(len(group) * (np.mean(group) - grand_mean)**2 for group in groups)
            
            # Total sum of squares
            ss_total = sum((x - grand_mean)**2 for x in all_data)
            
            return ss_between / ss_total if ss_total > 0 else 0
        except:
            return 0
    
    def _calculate_cohens_d(self, group1: pd.Series, group2: pd.Series) -> float:
        """Calculate Cohen's d effect size."""
        try:
            n1, n2 = len(group1), len(group2)
            s1, s2 = group1.std(), group2.std()
            
            # Pooled standard deviation
            pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
            
            return (group1.mean() - group2.mean()) / pooled_std
        except:
            return 0
    
    def generate_research_report(self, output_path: str) -> None:
        """Generate comprehensive research report."""
        if self.data is None:
            print("❌ No data loaded for analysis")
            return
        
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'sample_characteristics': self.descriptive_statistics(),
            'deictic_framing_effects': self.test_deictic_framing_effects(),
            'model_differences': self.test_model_differences(),
            'ethical_mode_associations': self.test_ethical_mode_associations(),
            'shamanic_hypothesis_test': self.analyze_shamanic_hypothesis(),
            'interaction_effects': self.analyze_interaction_effects()
        }
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Research report saved: {output_path}")
        
        # Print summary
        self._print_summary(report)
    
    def _print_summary(self, report: Dict) -> None:
        """Print summary of key findings."""
        print("\n" + "="*60)
        print("🔬 RESEARCH ANALYSIS SUMMARY")
        print("="*60)
        
        # Sample characteristics
        sample = report['sample_characteristics']
        print(f"\n📊 Sample Size: {sample['sample_size']} responses")
        print(f"🤖 Models: {list(sample['models'].keys())}")
        print(f"🎯 Framings: {list(sample['framings'].keys())}")
        
        # Significant deictic framing effects
        framing_effects = report['deictic_framing_effects']
        significant_vars = [var for var, result in framing_effects.items() 
                          if isinstance(result, dict) and result.get('significant', False)]
        
        print(f"\n🎯 Significant Deictic Framing Effects ({len(significant_vars)} variables):")
        for var in significant_vars[:5]:  # Show top 5
            result = framing_effects[var]
            print(f"   • {var}: p = {result['p_value']:.4f}, η² = {result['effect_size']:.3f}")
        
        # Shamanic hypothesis results
        shamanic_results = report['shamanic_hypothesis_test']
        print(f"\n🌟 Shamanic Framing Hypothesis:")
        for var, result in shamanic_results.items():
            if isinstance(result, dict) and 'significant' in result:
                status = "✅ SUPPORTED" if result['significant'] else "❌ Not supported"
                print(f"   • {var}: {status} (p = {result['p_value']:.4f})")
        
        print("\n" + "="*60)

def main():
    """Example usage of research statistics."""
    analyzer = ResearchStatistics()
    
    # Look for latest research data
    research_logs = Path("research_logs")
    if research_logs.exists():
        csv_files = list(research_logs.glob("research_data_*.csv"))
        if csv_files:
            latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
            print(f"📊 Analyzing: {latest_file}")
            
            analyzer.load_research_data(str(latest_file))
            
            # Generate comprehensive report
            report_path = research_logs / f"statistical_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            analyzer.generate_research_report(str(report_path))
        else:
            print("❌ No research data files found. Run concurrent_research_runner.py first.")
    else:
        print("❌ No research_logs directory found. Run concurrent_research_runner.py first.")

if __name__ == "__main__":
    main()