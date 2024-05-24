import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

billionaire_dataset = pd.read_csv('df_ready.csv')


# Gender x Continent (1)
gender = billionaire_dataset.groupby(['continent', 'gender']).size().reset_index(name='count')
gender['gender'] = pd.Categorical(gender['gender'], categories=sorted(gender['gender'].unique()), ordered=True)

plt.figure(figsize=(12,8))
barplot = sns.barplot(data=gender, x='continent', y='count', hue='gender', dodge=True)
barplot.set_title("The number of billionaires categorized by genders in each continent")
barplot.set_xlabel("Continent", weight='bold')
barplot.set_ylabel("Count", weight='bold')
barplot.tick_params(axis='x', which='both', length=0)

for bar in barplot.patches:
    height = bar.get_height()
    if height:
        barplot.annotate(format(height, '.0f'), (bar.get_x() + bar.get_width() / 2., height), ha='center', va='center', xytext=(0, 9), textcoords='offset points', size=10)

plt.xticks(rotation=0)
plt.ylim(0, gender['count'].max() + 50)  
plt.yticks(range(0, gender['count'].max() + 250, 250))
plt.tight_layout()



# Gender x Industry (2)
gender_industry = billionaire_dataset.groupby(['gender', 'industry']).size().reset_index(name='count')
gender_industry['gender'] = pd.Categorical(gender_industry['gender'], categories=sorted(gender_industry['gender'].unique()), ordered=True)

plt.figure(figsize=(14,8))
lineplot = sns.lineplot(data=gender_industry, x='industry', y='count', hue='gender', style='gender', markers='o', dashes=False)
lineplot.set_title("The number of male and female billionaires categorized by industries")
lineplot.set_xlabel("Industry", weight='bold')
lineplot.set_ylabel("Count", weight='bold')
plt.xticks(rotation=-45, ha='left')
plt.ylim(0, gender_industry['count'].max() + 50)  
plt.yticks(range(0, gender_industry['count'].max() + 100, 100))
plt.tight_layout()



# Age x Industry (3)
age_industry = billionaire_dataset.sort_values(by='industry')

plt.figure(figsize=(14,8))
boxplot = sns.boxplot(data=age_industry, x='industry', y='age', palette='Set3')
boxplot.set_title("Average age of billionaires divided by industries")
boxplot.set_xlabel("Industry", weight='bold')
boxplot.set_ylabel("Age", weight='bold')
plt.xticks(rotation=-45, ha='left')
max_age = billionaire_dataset['age'].max()
plt.yticks(range(0, max_age, int(max_age/4)))
plt.tight_layout()



# Age x Gender (5)
graph = sns.FacetGrid(billionaire_dataset, col="gender", height=5, aspect=1.2, sharey=False)
colors = {'Male': 'blue', 'Female': 'red'}
graph.map(sns.histplot, 'age', stat='density', bins=int((billionaire_dataset['age'].max() - billionaire_dataset['age'].min()) / 4), kde=True, color=colors, edgecolor='black', alpha=0.5)
graph.map(sns.kdeplot, 'age', color='black', linewidth=0.8)

graph.set_titles("{col_name}")
graph.set_axis_labels("Age", "Density")
graph.figure.suptitle("Histogram illustrates the ages of billionaires", fontsize=16)
plt.tight_layout()



# Top 10 countries with most billionaires (6)
country = billionaire_dataset['country_of_residence'].value_counts().reset_index(name='count')
country.columns = ['country', 'count']
top10countries = country.head(10)

plt.figure(figsize=(12,8))
barplot = sns.barplot(data=top10countries, x='count', y='country', palette='Set2', edgecolor='black')
barplot.set_title("TOP 10 COUNTRIES HAVE THE MOST BILLIONAIRES")
barplot.set_xlabel("number of billionaires", weight='bold')
barplot.set_ylabel("country", weight='bold')

for index, row in top10countries.iterrows():
    plt.text(row['count'] + 5, index, row['count'], color='black', ha='left', va='center', fontsize=10)

plt.xticks(range(0, top10countries['count'].max(), 200))
plt.gca().invert_yaxis()
plt.tight_layout()



# Top 5 industries operated businesses by the billionaires (7)
industries = billionaire_dataset['industry'].value_counts()
industries = (industries/industries.sum())*100
top5industries = industries.head(5).reset_index()
top5industries.columns = ['industry', 'percent']
otherindustries = industries.iloc[5:].sum()
top5industries.loc[len(top5industries)] = ['Others', otherindustries]

plt.figure(figsize=(12,8))
labels = [f"{row['industry']} ({round(row['percent'], 1)}%)" for index, row in top5industries.iterrows()]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
plt.pie(top5industries['percent'], labels=labels, colors=colors)
plt.title("Top 5 industries operated businesses by billionaires")
plt.tight_layout()



# Connection between wealth and industries (8)
wealth = billionaire_dataset.sort_values(by='industry', ascending=False)

plt.figure(figsize=(12,6))
sns.pointplot(data=wealth, x='wealth', y='industry', color="#ff9d8b", errorbar='sd', capsize=0.1, linestyles='none')
plt.title("The connection between the wealth of the billionaires and their industries for operating businesses")
plt.xlabel("Wealth", weight='bold')
plt.ylabel("Industry", weight='bold')
plt.xticks(np.arange(0, ((billionaire_dataset['wealth'].max() // 20) + 1) * 20, 2000))
plt.xlim(0, billionaire_dataset['wealth'].max()//20)
plt.tight_layout()



# Industry x Continent (9)
industry = billionaire_dataset.groupby(['continent', 'industry']).size().unstack(fill_value=0)
industry = industry.loc[sorted(billionaire_dataset['continent'].unique(), reverse=True)]
mask = industry == 0
vmin = industry.min().min()
vmax = industry.max().max()
vmax += (50 - (vmax % 50))

plt.figure(figsize=(12, 6))
sns.heatmap(data=industry, cmap="mako", mask=mask, cbar_kws={'label': 'Count', 'orientation': 'vertical'}, vmin=vmin, vmax=vmax)
plt.title("The distribution of billionaires in industries according to each continent", y=1.1)
plt.xlabel("Industry", weight='bold')
plt.ylabel("Continent", weight='bold')
plt.xticks(rotation=-45, ha='left', fontsize=10) 
plt.yticks(fontsize=10, rotation=0) 
plt.tight_layout()

plt.show()