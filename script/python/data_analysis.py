import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

df = pd.read_csv(
    r'C:\Users\preya\OneDrive\Desktop\Spotify Data Analysis\processed_data\artists_final.csv',
    encoding='latin1'
)

print(df.head())
# Quick double check that Python sees the same clean data
print(df.info())
print(df.describe())

#FEATURE GHOST ANALYSIS

# Step A: Filter to artists with a meaningful stream count (avoid noise from tiny artists)
df_filtered = df[df['total_streams'] > df['total_streams'].quantile(0.25)]

# Step B: Sort by feature_ratio to find the top "Feature Ghosts"
feature_ghosts = df_filtered.sort_values('feature_ratio', ascending=False).head(15)
print(feature_ghosts[['artist_name', 'primary_genre', 'feature_ratio', 'total_streams']])

# Step C: Visualize top 15 Feature Ghosts
plt.figure(figsize=(10,7))
sns.barplot(data=feature_ghosts, y='artist_name', x='feature_ratio', palette='mako')
plt.title('Top 15 "Feature Ghosts": Artists Whose Fame Leans on Guest Features')
plt.xlabel('Feature Ratio (Feature Streams / Lead Streams)')
plt.ylabel('')
plt.tight_layout()
plt.savefig('../visuals/q1_feature_ghosts.png', dpi=200)
plt.show()

# Step D: Is this a genre pattern? Average feature_ratio per genre
genre_feature = df_filtered.groupby('primary_genre')['feature_ratio'].mean().sort_values(ascending=False).head(10)

plt.figure()
genre_feature.plot(kind='barh', color='teal')
plt.title('Average Feature Ratio by Genre')
plt.xlabel('Avg Feature Ratio')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../visuals/q1_genre_feature_ratio.png', dpi=200)
plt.show()

#QUESTION 2: DOES LANGUAGE PREDCT COLLABORATION?

# Step A: Compare Collaborative % between English and Non-English artists

lang_summary=df.groupby('language_group')['pct_collab'].aggregate(['mean', 'median', 'count'])
print(lang_summary)

# Step B: Visualize with a boxplot

plt.figure()
sns.boxplot(data=df, x='language_group', y='pct_collab', palette='Set2')
plt.title('Collaborative Streams % — English vs Non-English Artists')
plt.ylabel('% of Collaborative Streams')
plt.xlabel('')
plt.tight_layout()
plt.savefig('../visuals/q2_language_collab_boxplot.png', dpi=200)
plt.show()

# Step C: Statistical test — Mann-Whitney U (2-group non-parametric test)
english = df[df['language_group'] == 'English']['pct_collab'].dropna()
non_english = df[df['language_group'] == 'Non-English']['pct_collab'].dropna()

stat, p_value = stats.mannwhitneyu(english, non_english, alternative='two-sided')
print(f"Mann-Whitney U statistic = {stat:.2f}, p-value = {p_value:.5f}")

# Step D: Break down by individual language too (not just binary group)
plt.figure(figsize=(11,6))
top_languages = df['primary_language'].value_counts().head(6).index
sns.boxplot(data=df[df['primary_language'].isin(top_languages)], x='primary_language', y='pct_collab', palette='coolwarm')
plt.title('Collaborative Streams % by Language (Top 6 Languages)')
plt.tight_layout()
plt.savefig('../visuals/q2_language_breakdown.png', dpi=200)
plt.show()

# Step E (important honesty check): control for genre confound
# Is this really about language, or is it just Reggaeton/Latin genres driving it?
genre_drive=pd.crosstab(df['language_group'], df['primary_genre']).T.sort_values('Non-English', ascending=False).head(10)
print(genre_drive)

#QUESTION 3: Legacy vs Streaming-Native Dominance

# Step A: Total Streams by Debut Era
era_summary = df.groupby('debut_era')['total_streams'].agg(['mean', 'median', 'count'])
print(era_summary)

# Step B: Boxplot (better than bar chart for skewed data — shows spread, not just average)
order = ['Pre-2010 (Legacy)', '2010-2015 (Transition)', '2016+ (Streaming-Native)']
plt.figure()
sns.boxplot(data=df, x='debut_era', y='total_streams', order=order, palette='rocket')
plt.yscale('log')  # log scale because streaming numbers are skewed
plt.title('Total Streams by Debut Era (log scale)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('../visuals/q3_era_total_streams.png', dpi=200)
plt.show()

# Step C: Solo % vs Collab % across eras (stacked bar)
era_pct = df.groupby('debut_era')[['pct_solo', 'pct_collab']].mean().loc[order]
era_pct.plot(kind='bar', stacked=True, colormap='viridis', figsize=(8,6))
plt.title('Solo vs Collaborative Streams % by Debut Era')
plt.ylabel('Average %')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('../visuals/q3_era_solo_vs_collab.png', dpi=200)
plt.show()

# Step D: Scatter — Debut Year vs Total Streams, colored by Artist Type

plt.figure()
sns.scatterplot(data=df, x='debut_year', y='total_streams', hue='artist_type', alpha=0.6)
plt.yscale('log')
plt.title('Debut Year vs Total Streams (log scale)')
plt.tight_layout()
plt.savefig('../visuals/q3_debut_scatter.png', dpi=200)
plt.show()

# Step E: Statistical test across 3 eras
era_groups = [group['total_streams'].dropna().values for name, group in df.groupby('debut_era')]
stat, p_value = stats.kruskal(*era_groups)
print(f"Kruskal-Wallis H = {stat:.2f}, p-value = {p_value:.5f}")

#QUESTION 4: UNSUPERVISED ARTIST ARCHETYPES

# Step A: Select and scale features for clustering
cluster_features = df[['pct_solo', 'pct_collab', 'feature_ratio', 'debut_year']].fillna(0)

scaler = StandardScaler()
scaled_features = scaler.fit_transform(cluster_features)

# Step B: Find the best number of clusters (Elbow Method)
inertia = []
k_range = range(2, 9)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(scaled_features)
    inertia.append(km.inertia_)

plt.figure()
plt.plot(k_range, inertia, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.tight_layout()
plt.savefig('../visuals/q4_elbow_method.png', dpi=200)
plt.show()
# Pick the "elbow" point — where the line stops dropping sharply, usually k=3, 4, or 5

# Step C: Run KMeans with your chosen k (say k=4, adjust based on elbow chart)
k_final = 4
kmeans = KMeans(n_clusters=k_final, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(scaled_features)

# Step D: Reduce to 2D with PCA for visualization
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)
df['pca_1'] = pca_result[:, 0]
df['pca_2'] = pca_result[:, 1]

plt.figure(figsize=(10,7))
sns.scatterplot(data=df, x='pca_1', y='pca_2', hue='cluster', palette='Set1', s=60, alpha=0.75)
plt.title('Artist Archetype Clusters (PCA Projection)')
plt.tight_layout()
plt.savefig('../visuals/q4_cluster_scatter.png', dpi=200)
plt.show()

# Step E: Profile each cluster — what defines it?
cluster_profile = df.groupby('cluster')[['pct_solo', 'pct_collab', 'feature_ratio', 'debut_year', 'total_streams']].mean()
print(cluster_profile)

# Also check genre/language makeup of each cluster
print(pd.crosstab(df['cluster'], df['primary_genre']).T)

cluster_names = {
    0: 'Legacy Solo Icons',
    1: 'Collab-Driven Crossover Stars',
    2: 'Feature Specialists',
    3: 'Ensemble Groups'
    # adjust based on YOUR actual cluster_profile output
}
df['cluster_name'] = df['cluster'].map(cluster_names)

# Step F: Save the final dataset (with cluster labels) for Power BI
df.to_csv('../processed_data/artists_for_powerbi.csv', index=False)
