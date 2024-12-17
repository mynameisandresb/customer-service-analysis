import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import f_oneway, chi2_contingency
from datetime import datetime

def time_conversion(timestr):
    if not isinstance(timestr, str):
        return None
    for timeformat in ["%m/%d/%Y %I:%M:%S %p", "%m-%d-%y %H:%M"]:
        try:
            return datetime.strptime(timestr, timeformat)
        except ValueError:
            pass
    raise ValueError('Incompatible time format for conversion')


def plot_function(data, x_label, y_label, kind='bar'):
    plt.figure(figsize=(8, 5))
    data.plot(kind=kind, color='skyblue')
    plt.title(f'{x_label} vs {y_label}')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def main():

    # Formats the data correctly for analysis
    data = pd.read_csv('Dataset/311_Service_Requests_from_2010_to_Present.csv')
    data['Created Date'] = data['Created Date'].apply(time_conversion)
    data['Closed Date'] = data['Closed Date'].apply(time_conversion)
    data['Request_Closing_Time'] = (data['Closed Date'] - data['Created Date']).dt.total_seconds() / 3600
    data = data.dropna(subset=['Created Date', 'Closed Date', 'Request_Closing_Time'])

    #################################################
    # Creates graphs
    top_complaints = data['Complaint Type'].value_counts().head(5)
    plot_function(top_complaints, 'Complaint Type', 'Count')
    avg_time = data.groupby('Complaint Type')['Request_Closing_Time'].mean().sort_values(ascending=False).head(5)
    plot_function(avg_time, 'Complaint Type', 'Average Closing Time (hours)')
    complaints_by_borough = data['Borough'].value_counts()
    plot_function(complaints_by_borough, 'Borough', 'Number of Complaints')
    data['Month'] = data['Created Date'].dt.to_period('M')  # Extract Year-Month
    complaints_over_time = data['Month'].value_counts().sort_index()
    plot_function(complaints_over_time, 'Month', 'Number of Complaints', kind='line')

    # Analysis for Null Hypothesis
    # ANOVA For continuous and categorical
    grouped = [group['Request_Closing_Time'].dropna() for _, group in data.groupby('Complaint Type')]
    f_stat, p_val = f_oneway(*grouped)
    print(f"ANOVA f-stat:{f_stat}, p-val:{p_val}")
    if p_val < 0.05:
        print("p_val < 0.05, Null Hypothesis rejected, response times are not the same across types of complaints.")
    else:
        print("p_val >= 0.05, Null Hypothesis not rejected, did not find a difference in response times")
    contingency_table = pd.crosstab(data['Complaint Type'], data['Borough'])
    # Chi for Categorical and Categorical
    chi2, p_val, _, _ = chi2_contingency(contingency_table)
    print(f"\nChi-Square chi2:{chi2}, p-val={p_val}")
    if p_val < 0.05:
        print("p_val < 0.05, Null Hypothesis rejected, location and the type of complaint are related")
    else:
        print("p_val >= 0.05, Null Hypothesis not rejected, did not find a relationship between location and type of complaint")
main()