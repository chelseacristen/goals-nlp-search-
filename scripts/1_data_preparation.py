"""
1_data_preparation.py
=====================

Prepare goals and milestone data for natural language search indexing.

Key Dependencies:
- pandas
- numpy

Summary:
This script loads raw Cascade goals/milestone data, cleans and structures it for 
search indexing. It handles date conversions, creates nested milestone/KPI structures,
and ensures data quality for downstream processing.

Input: Raw CSV exports from Cascade (goals, milestones, KPIs)
Output: Cleaned, structured dataframe ready for embedding generation
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def load_cascade_data(file_path='data/sample_goals.csv'):
    """
    Load and clean Cascade goals data
    
    Args:
        file_path (str): Path to the goals CSV file
    
    Returns:
        pd.DataFrame: Cleaned goals dataframe
    """
    # Load the data
    cascade_detailed_df = pd.read_csv(file_path)
    
    # Identify and convert date columns
    date_column_names = [col for col in cascade_detailed_df.columns if col.lower().endswith(' date')]
    
    for col in date_column_names:
        cascade_detailed_df[col] = pd.to_datetime(cascade_detailed_df[col], errors='coerce')
    
    # Standardize column names
    cascade_detailed_df = cascade_detailed_df.rename(columns={'Focus areas': 'Key Initiative'})
    
    return cascade_detailed_df

def structure_goals_data(df):
    """
    Structure goals data with nested milestones and KPIs
    
    Args:
        df (pd.DataFrame): Raw goals dataframe
    
    Returns:
        list: List of structured goal dictionaries
    """
    structured_goals = []
    
    # Group by goal to handle milestones/KPIs
    for goal_id, goal_group in df.groupby('goal_id'):
        goal_data = goal_group.iloc[0].to_dict()
        
        # Extract milestones if they exist
        milestones = []
        if 'milestone_title' in goal_group.columns:
            for _, milestone_row in goal_group.iterrows():
                if pd.notna(milestone_row.get('milestone_title')):
                    milestone = {
                        'title': milestone_row.get('milestone_title', ''),
                        'description': milestone_row.get('milestone_description', ''),
                        'owner': milestone_row.get('milestone_owner', ''),
                        'health': milestone_row.get('milestone_health', ''),
                        'end_date': milestone_row.get('milestone_end_date', ''),
                        'last_update': milestone_row.get('milestone_last_update', '')
                    }
                    milestones.append(milestone)
        
        # Add milestones to goal structure
        goal_data['milestones'] = milestones
        
        # Extract KPIs if they exist (similar pattern)
        kpis = []
        if 'kpi_title' in goal_group.columns:
            for _, kpi_row in goal_group.iterrows():
                if pd.notna(kpi_row.get('kpi_title')):
                    kpi = {
                        'title': kpi_row.get('kpi_title', ''),
                        'description': kpi_row.get('kpi_description', ''),
                        'health': kpi_row.get('kpi_health', '')
                    }
                    kpis.append(kpi)
        
        goal_data['kpis'] = kpis
        structured_goals.append(goal_data)
    
    return structured_goals

def validate_data_quality(structured_goals):
    """
    Validate data quality and report issues
    
    Args:
        structured_goals (list): List of structured goal dictionaries
    
    Returns:
        dict: Data quality report
    """
    report = {
        'total_goals': len(structured_goals),
        'goals_with_owners': 0,
        'goals_with_departments': 0,
        'goals_with_milestones': 0,
        'total_milestones': 0,
        'issues': []
    }
    
    for goal in structured_goals:
        # Check for required fields
        if goal.get('goal_owner'):
            report['goals_with_owners'] += 1
        
        if goal.get('goal_department'):
            report['goals_with_departments'] += 1
            
        if goal.get('milestones') and len(goal['milestones']) > 0:
            report['goals_with_milestones'] += 1
            report['total_milestones'] += len(goal['milestones'])
        
        # Check for data quality issues
        if not goal.get('goal_title'):
            report['issues'].append(f"Goal {goal.get('goal_id', 'Unknown')} missing title")
    
    return report

if __name__ == "__main__":
    # Load and prepare data
    print("📊 Loading Cascade data...")
    cascade_df = load_cascade_data()
    
    print("🔧 Structuring goals data...")
    structured_goals = structure_goals_data(cascade_df)
    
    print("✅ Validating data quality...")
    quality_report = validate_data_quality(structured_goals)
    
    print(f"Data Quality Report:")
    print(f"- Total goals: {quality_report['total_goals']}")
    print(f"- Goals with owners: {quality_report['goals_with_owners']}")
    print(f"- Goals with departments: {quality_report['goals_with_departments']}")
    print(f"- Goals with milestones: {quality_report['goals_with_milestones']}")
    print(f"- Total milestones: {quality_report['total_milestones']}")
    
    if quality_report['issues']:
        print("⚠️ Issues found:")
        for issue in quality_report['issues']:
            print(f"  - {issue}")
    
    # Save structured data for next step
    import pickle
    with open('data/structured_goals.pkl', 'wb') as f:
        pickle.dump(structured_goals, f)
    
    print("✅ Data preparation complete!")
