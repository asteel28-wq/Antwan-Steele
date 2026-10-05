# Predicting NBA Rookie Performance from Pre-NBA Statistics

**Research question:** How well do a player's latest available pre-NBA season statistics predict rookie-season Player Efficiency Rating (PER) and Win Shares (WS)?

**Project type:** Regression  
**Population:** Players drafted from 2018 through 2023  
**Unit of analysis:** One drafted player, matched by Basketball-Reference player ID  
**Models:** Multiple linear regression and degree-two polynomial regression, compared with a training-mean baseline

My project studies historical relationships; it is not a draft decision tool.

## 1. Problem definition

NBA teams, scouts, and fans want to understand which statistics are associated with a player's predicted performance in the professional level, basing off of their pre-NBA stats from their previous organization they played for. This project asks whether points, rebounds, assists, turnovers, field-goal percentage, and age from a player's latest available season can predict two continuous rookie outcomes: PER and WS(win shares).

A prediction could help summarize a prospect's statistical profile, but it cannot capture every factor that shapes a career. Competition level, role, team situation, health, skills not represented in box scores, and playing time all affect outcomes. The models provide a limited baseline for comparison rather than a player evaluation or causal explanation.

## 2. Background and context

Research has examined whether college production relates to later professional performance. Coates and Oguntimein (2010) studied whether college productivity predicts professional productivity and career length. They report that some college productivity measures were associated with draft position, and those relationships differed by conference context. Moxley and Towne (2015) emphasize that NBA success involves both stability and potential, which cautions against treating one season's box-score line as a complete measure of future performance.

This project measures rookie performance with PER and WS. Basketball-Reference describes Win Shares as an estimate of the wins a player contributed, connected to team success. Both targets have limitations: PER is a summary efficiency rating, and total WS also reflects playing time and team context. Models can find associations in these data, but they cannot establish that a college statistic causes NBA success. References appear at the end.

## 3. Variables and operational definitions

| Concept | Variable | Operational definition |
|---|---|---|
| Rookie performance | PER | PER from the player's first NBA season in the outcomes file |
| Rookie team value | WS | Total Win Shares from that NBA rookie season |
| Scoring | PTS_per_game | Estimated points per game in the latest available pre-NBA season |
| Rebounding | REB_per_game | Estimated rebounds per game in that season |
| Playmaking | AST_per_game | Estimated assists per game in that season |
| Ball security | TOV_per_game | Estimated turnovers per game in that season |
| Shooting efficiency | FG_pct | Field-goal percentage stored as a fraction (0.500 = 50.0%) |
| Age / experience proxy | Age | Age calculated on January 31 of the season-ending year; it is a proxy, not age at draft or college class |

The model uses all six numeric pre-NBA predictors. College class and field-goal attempts per game are not included because they are unavailable in the supplied files. Per-game box-score values were derived from per-40 rates and total minutes in the source dataset.

## 4. Data collection and coverage

The supplied CSVs cover 356 drafted players across six draft classes. The rookie outcomes file has PER and WS for 336 players. The pre-NBA file has a season record for 246 players. Requiring all six predictors and both outcomes leaves 240 players for regression.

The pre-NBA CSV comes from a compiled draft-prospect dataset whose README credits RealGM, Basketball-Reference, Bart Torvik, Hoop-Math, and 247Sports. It is not a uniform NCAA-only table, so this project calls the feature period the **latest available pre-NBA season**. Many international or other non-college seasons are blank in the supplied data. Those players remain in the source CSV but cannot enter complete-case models.

The NBA outcome file links each record to the draft page and advanced-stat page. The files are joined by player ID, not names alone.

## 5. Data understanding and preparation

The models require complete predictor and outcome values. Blank pre-NBA fields are not replaced with zero: zero would incorrectly mean a player had no recorded points, rebounds, or other performance. The complete-case rule leaves 240 players.

The holdout consists of the 2022 and 2023 draft classes. Models train on the 2018-2021 classes and predict the later two classes. This chronological split better represents predicting future draft cohorts than randomly mixing players from every year.

## 6. Visualization 1: pre-NBA scoring and rookie outcomes

These plots show points per game against rookie PER and total rookie WS. Each point is one player, colored by draft year. The line is a descriptive linear trend across all complete cases, not a holdout prediction or causal estimate. Total WS also depends on playing time.

## 7-8. Model design/ visualizations: holdout predictions
[rookie_outcome.png](projects/project-hoops/analysis_outputs)  
[rookie_prediction.png](projects/project-hoops/analysis_outputs)

The baseline predicts the training-class mean for every holdout player. Multiple linear regression estimates a straight-line relationship between the six standardized predictors and each outcome. Polynomial regression expands the predictors to include squared and pairwise interaction terms, then applies Ridge regularization (alpha = 10) to limit overfitting. This setting is fixed for this project, not optimized through a separate tuning search.

Both models predict PER and WS separately. MAE and RMSE measure error in the outcome's units; lower values are better. R-squared measures test-set variation explained relative to predicting the test mean; higher is better, and negative values indicate performance worse than that reference.

Each panel compares actual and predicted values for one target/model combination on the 2022-2023 holdout. Points closer to the dashed diagonal are more accurate. The baseline forms a vertical band because it predicts the same training mean for each player.

## 9. Results and interpretation of my visualizations

The first visualization compares each player’s latest available pre-NBA points per game with their rookie PER and Win Shares. Each dot represents one player, and the colors show the draft year. The trend lines rise slightly, but the dots are spread out, so points per game alone is not a strong predictor of either outcome. The correlations between points per game and rookie PER or Win Shares are close to zero.

The second visualization shows predictions for the 2022 and 2023 draft classes. The models learned from players drafted between 2018 and 2021. The dashed diagonal shows where a perfect prediction would fall. The linear and polynomial models are generally closer to that line than the average-value baseline, but many predictions still miss the actual results. The models often predict closer to the group mean and struggle with unusually high or low outcomes.

Polynomial regression had the lowest average error for both PER and Win Shares, but it only improved slightly over linear regression. Its R² was about 0.23 for each outcome. This means the model captured some differences among players in the holdout group, but the features in this project still didn't explain most of them. I would describe the predictions as modest, not reliable enough to judge an individual prospect.

The coefficient results suggest that field-goal percentage and age were most strongly associated with predicted PER in the linear model. Assists and turnovers had the largest coefficients for Win Shares. These results show associations in this sample; they do not prove that one statistic causes a player to succeed. Other factors, such as playing time, health, team situation, and the level of competition, may also affect rookie performance.

## 10. Limitations, ethics, and reflection

- **Missing pre-NBA data:** 110 players have no matched pre-NBA season record. International and other non-college players are especially likely to be missing. The 240-player sample is not representative of all 356 drafted players.
- **Survivorship and selection:** The project includes drafted players only. It cannot compare drafted prospects with undrafted players, and it does not explain who gets drafted.
- **Small sample:** There are 166 training players and 74 holdout players. A different draft-year split could produce different scores.
- **Outcome definitions:** PER and WS are imperfect summaries. WS is cumulative and affected by playing time and team performance; PER can be unstable for players with few minutes. The files do not provide consistent playing time for filtering.
- **Context and comparability:** The dataset combines pre-NBA environments and seasons. Similar statistics can mean different things across leagues, teams, roles, and levels of competition.
- **Model risk:** Polynomial regression only slightly outperforms linear regression here, and both leave most outcome variation unexplained. I would not use either alone for a real draft decision. Scouting, health, role, and development also matter.

## 11. Conclusion

On the 2022-2023 holdout, both regressions performed better than the training-mean baseline for PER and WS. Polynomial regression had the lowest MAE, but only by a small margin over linear regression. The supplied pre-NBA statistics contain some information about rookie outcomes, but they are not enough to predict an individual player's performance reliably.

The answer to the research question is **somewhat, but with substantial uncertainty**. A stronger follow-up would add verified final-season stats for international and semi-pro prospects, minutes played, competition level, and additional future draft classes.

## 12. Code and transparency

The reusable Python analysis is in [nba_rookie_analysis.py](nba_rookie_analysis.py). Run it from this folder with **python nba_rookie_analysis.py**. It reads the two CSVs in the draft-data folder, saves two figures and result tables in analysis_outputs, and prints coverage and model results.

Generative AI disclosure: I used Claude (Sonnet 5.5, made by Anthropic) to help draft and debug the Python analysis code. I reviewed and ran the code myself, checked the results against the data, and made the final modeling decisions and conclusions.
## References

Coates, D., & Oguntimein, B. (2010). The length and success of NBA careers: Does college production predict professional outcomes? *International Journal of Sport Finance, 5*(1), 4-26. https://doi.org/10.1177/155862351000500101

Moxley, J. H., & Towne, T. J. (2015). Predicting success in the National Basketball Association: Stability & potential. *Psychology of Sport and Exercise, 16*, 128-136. https://doi.org/10.1016/j.psychsport.2014.07.003

Basketball-Reference.com. (n.d.). *Glossary*. Retrieved October 3, 2026, from https://www.basketball-reference.com/about/glossary.html

JasonG7234. (n.d.). *NBA-Draft-Model* [Data set]. GitHub. Retrieved October 3, 2026, from https://github.com/JasonG7234/NBA-Draft-Model/tree/master/data

Basketball-Reference.com. (n.d.). *NBA 2018-19 advanced statistics*. Retrieved October 3, 2026, from https://www.basketball-reference.com/leagues/NBA_2019_advanced.html

Source URL columns in the CSVs link to the draft, rookie-stat, or pre-NBA record for each player. The supplied CSV copies were accessed October 3, 2026.

