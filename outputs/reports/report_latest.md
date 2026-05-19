# Data Analysis Report

## 1. Executive Summary
This report presents an analysis of a movie-related dataset comprising 1,000 entries and 7 features. Our focus was primarily on understanding the relationships between various attributes such as movie ratings, user rating scores, and other descriptive characteristics. The analysis identified several intriguing insights and potential data quality issues that could influence the data's interpretability and utility.

## 2. Dataset Overview
The dataset contains 1,000 rows and 7 columns. Among these, notable columns include `user_rating_score`, `ratinglevel`, `title`, `rating`, `ratingdescription`, `release_year`, and `user_rating_size`. The dataset showcases a rich diversity with high cardinality in the `title` column, while the `rating` column displays lower cardinality with 13 unique categories, simplifying certain analyses.

## 3. Data Quality
Several data quality issues were detected during the analysis:
- **`user_rating_score` Column**: Exhibits a high null percentage of 39.5%, with 395 entries missing. This significant absence of data could undermine analyses relying on this feature.
- **`ratinglevel` Column**: Contains 5.9% null values, warranting further data cleaning or imputation to ensure comprehensive analysis.
- **`ratingdescription` Column**: Shows a data type mismatch, being stored as `int64` despite its potential categorical nature, indicating a need for re-evaluation of data types.
- **`user_rating_size` Column**: Shows low cardinality with only 3 unique values, suggesting limited variability which might hinder detailed analysis.

## 4. Key Findings
1. **Correlation between Ratings and User Rating Scores**: There is a correlation of 0.224 between higher movie ratings and user rating scores, indicating a positive relationship.
2. **Recency and User Rating Scores**: Recent movies exhibit higher user rating scores compared to older movies. The correlation between release_year and user_rating_score is 0.2217.
3. **Rating Levels and User Rating Scores**: Higher rating levels are associated with higher user rating scores, with a correlation of 0.224 between `ratingdescription` and `user_rating_score`.
4. **User Rating Sizes and Rating Descriptions**: There is a slight negative correlation (-0.2262) between user rating sizes and rating descriptions, suggesting that movies with higher user rating sizes tend to have lower rating descriptions.

## 5. Visualizations
Eleven charts were generated to visualize these insights, with prominent ones including:
- **Correlation Heatmap**: Visual represents correlations between all numeric columns.
- **Boxplots** for various findings:
  - Distribution of user rating scores by movie ratings, release years, and rating levels.
  - Relationship between user rating sizes and rating descriptions.
  - Relationship between rating descriptions and user rating scores.

Please refer to the chart outputs indexed from `outputs/charts/` for visual confirmation of the findings.

## 6. Recommended Next Steps
- **Data Cleaning and Imputation**: Address high null percentages in `user_rating_score` and `ratinglevel` to enhance data completeness. Reassess and correct the data type mismatch in the `ratingdescription` column to ensure accuracy in analyses.
- **Further Analysis**: Explore potential linear and nonlinear relationships between other unexplored features for a broader understanding of influencing factors on user rating scores.
- **Contextual Investigation**: Assess factors outside the dataset, such as marketing strategies or channel availability, which may influence user ratings and engagement.
- **Data Collection and Re-evaluation**: Encourage additional data collection, particularly for features with high missing values, to support robustness in future analyses and predictive modeling. Consider conducting evaluations on the utility of low-variability features like `user_rating_size`.

This comprehensive analysis and its derived insights will act as a foundation for strategic decisions and further investigations into movie ratings and their impact on user engagement.