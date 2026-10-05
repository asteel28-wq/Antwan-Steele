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

## 7. Model design

The baseline predicts the training-class mean for every holdout player. Multiple linear regression estimates a straight-line relationship between the six standardized predictors and each outcome. Polynomial regression expands the predictors to include squared and pairwise interaction terms, then applies Ridge regularization (alpha = 10) to limit overfitting. This setting is fixed for this project, not optimized through a separate tuning search.

Both models predict PER and WS separately. MAE and RMSE measure error in the outcome's units; lower values are better. R-squared measures test-set variation explained relative to predicting the test mean; higher is better, and negative values indicate performance worse than that reference.

## 8. Visualization 2: holdout predictions

Each panel compares actual and predicted values for one target/model combination on the 2022-2023 holdout. Points closer to the dashed diagonal are more accurate. The baseline forms a vertical band because it predicts the same training mean for each player.