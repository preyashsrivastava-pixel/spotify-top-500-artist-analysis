# Beyond the Charts: Decoding Collaboration, Language, and Legacy in Spotify's Top 500 Artists

## What this project is about

I wanted to go past the usual "who has the most streams" kind of analysis and actually dig into the behavior behind the numbers. This project uses a dataset of the 500 most streamed artists on Spotify to answer four questions that I found genuinely interesting rather than obvious. It walks through a full pipeline: cleaning and validating the data in SQL, analyzing it in Python, and building an interactive dashboard in Power BI.

## The questions I set out to answer

**1. The Feature Ghost phenomenon**
Are there artists whose fame comes mostly from guesting on other people's songs rather than their own lead tracks? And is that a pattern tied to specific genres?

**2. The language and collaboration tax**
Do non English artists rely on collaboration more than English artists to break into the global top 500?

**3. Legacy vs streaming native dominance**
Do older artists who debuted before the streaming era still hold their own against artists who came up entirely within it? And has the way artists succeed (solo driven vs collaboration driven) shifted over time?

**4. Artist archetypes**
Instead of me deciding what "type" of artist someone is, can the data group similar artists together on its own, purely based on their streaming behavior?

## Tools used

* **SQL (SSMS)** for importing, cleaning, validating, and feature engineering the raw dataset
* **Python** (pandas, numpy, matplotlib, seaborn, scipy, scikit learn) for the actual analysis, statistical testing, and clustering
* **Power BI** for building the final interactive dashboard

## The pipeline

**Step 1: SQL**
The raw CSV was loaded into SQL Server, cleaned up (trimmed column names, fixed types), and validated. I checked for duplicates, confirmed that lead streams plus feature streams roughly matched total streams, and checked for missing or empty values. A few new columns were engineered directly in SQL, including a feature ratio, a debut era bucket, and a simplified language group.

**Step 2: Python**
Each of the four questions was answered using the same basic approach: build or reuse a metric, filter out noise where needed, visualize the pattern, then run a statistical test to check whether the pattern was real or just chance. Question four used KMeans clustering and PCA to group artists into behavioral archetypes without relying on any predefined category like genre.

**Step 3: Power BI**
The final cleaned and feature engineered dataset was loaded into Power BI to build a five page interactive dashboard, one page per question plus an overview page, with slicers so anyone viewing it can filter by genre, language, era, or sex.

## Key findings

* Feature driven fame is a real, genre linked pattern. Some genres lean heavily on featured artists earning far more from guest verses than lead tracks, and this difference is statistically significant.
* Non English artists show a meaningfully higher share of collaborative streams than English artists, suggesting collaboration acts as a crossover strategy into global audiences.
* Streaming native artists (those who debuted after 2016) lean more on collaborative streams than legacy artists, reflecting how playlist culture and algorithmic discovery have changed how artists build an audience.
* Four distinct artist archetypes emerge naturally from the data, without ever telling the algorithm about genre or language, which reinforces that these patterns are structural rather than coincidental.

## Repository structure

```
spotify top artists analysis
data raw            original CSV, untouched
data clean            cleaned and feature engineered CSV files
sql                    SQL scripts used for cleaning and validation
notebooks            Jupyter notebooks for each question
visuals                exported chart images
powerbi                the pbix dashboard file
```

## Data source

The dataset used is `Most Streamed Artists on Spotify`, containing 500 artists with fields covering total streams, lead vs feature streams, solo vs collaborative streams, genre, language, country of origin, debut year, and artist type.

## Notes on methodology

I tried to be honest rather than just chasing significant results. Where a pattern could be explained by something else, like the language finding possibly overlapping with genre composition, I checked that directly with a crosstab rather than assuming the simplest explanation was the full story. A couple of rounding level mismatches showed up during validation and were left alone since they were far too small to matter.

## What I would explore next

Extending this with a time series view of how these patterns have shifted year by year would be a natural next step, along with pulling in audio features (tempo, energy, danceability) if a future version of the dataset includes them, to see whether they correlate with any of the four archetypes.

## About me

I am a statistics student who put this together as a way to practice working across the full data pipeline, from raw SQL cleaning all the way to a polished dashboard. Feel free to reach out if you have feedback or want to talk through any part of the approach.
