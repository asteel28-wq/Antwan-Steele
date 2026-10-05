"""Analyze whether final pre-NBA season stats predict rookie PER and Win Shares.

Run from any working directory with:
    python nba_rookie_analysis.py

The script reads CSVs from ./draft-data and writes figures and result tables
into ./analysis_outputs.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "draft-data"
OUTPUT_DIR = ROOT / "analysis_outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

FEATURES = [
    "PTS_per_game",
    "REB_per_game",
    "AST_per_game",
    "TOV_per_game",
    "FG_pct",
    "Age",
]
TARGETS = ["PER", "WS"]
TRAIN_DRAFT_YEARS = list(range(2018, 2022))
TEST_DRAFT_YEARS = [2022, 2023]


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load and match the two supplied datasets using stable player IDs."""
    outcomes = pd.read_csv(DATA_DIR / "nba_rookie_outcomes.csv")
    pre_nba = pd.read_csv(DATA_DIR / "pre_nba_stats.csv")

    if outcomes["PlayerID"].duplicated().any() or pre_nba["PlayerID"].duplicated().any():
        raise ValueError("PlayerID must uniquely identify each drafted player.")

    merged = pre_nba.merge(
        outcomes[["PlayerID", "DraftYear", "RookieSeason", "PER", "WS"]],
        on=["PlayerID", "DraftYear"],
        how="left",
        validate="one_to_one",
        suffixes=("_pre", "_nba"),
    )
    complete = merged.dropna(subset=FEATURES + TARGETS + ["DraftYear"]).copy()
    complete["DraftYear"] = complete["DraftYear"].astype(int)
    return merged, complete


def build_models() -> dict[str, object]:
    """Return a baseline, linear regression, and regularized quadratic model."""
    return {
        "Mean baseline": DummyRegressor(strategy="mean"),
        "Linear regression": Pipeline(
            [
                ("scale", StandardScaler()),
                ("regressor", LinearRegression()),
            ]
        ),
        "Polynomial regression (degree 2)": Pipeline(
            [
                ("polynomial", PolynomialFeatures(degree=2, include_bias=False)),
                ("scale", StandardScaler()),
                ("regressor", Ridge(alpha=10.0)),
            ]
        ),
    }


def fit_and_evaluate(complete: pd.DataFrame):
    """Train on 2018-2021 drafts and evaluate on the 2022-2023 holdout."""
    train = complete[complete["DraftYear"].isin(TRAIN_DRAFT_YEARS)]
    test = complete[complete["DraftYear"].isin(TEST_DRAFT_YEARS)]
    if train.empty or test.empty:
        raise ValueError("The chronological train/test split is empty.")

    X_train, X_test = train[FEATURES], test[FEATURES]
    metrics = []
    prediction_tables = []
    fitted_models = {}

    for target in TARGETS:
        y_train, y_test = train[target], test[target]
        for model_name, model in build_models().items():
            model.fit(X_train, y_train)
            predicted = model.predict(X_test)
            metrics.append(
                {
                    "Target": target,
                    "Model": model_name,
                    "Train_n": len(train),
                    "Test_n": len(test),
                    "MAE": mean_absolute_error(y_test, predicted),
                    "RMSE": np.sqrt(mean_squared_error(y_test, predicted)),
                    "R2": r2_score(y_test, predicted),
                }
            )
            prediction_tables.append(
                pd.DataFrame(
                    {
                        "DraftYear": test["DraftYear"].to_numpy(),
                        "Player": test["Player"].to_numpy(),
                        "PlayerID": test["PlayerID"].to_numpy(),
                        "Target": target,
                        "Model": model_name,
                        "Actual": y_test.to_numpy(),
                        "Predicted": predicted,
                    }
                )
            )
            fitted_models[(target, model_name)] = model

    return (
        pd.DataFrame(metrics),
        pd.concat(prediction_tables, ignore_index=True),
        fitted_models,
        train,
        test,
    )


def make_visualizations(complete: pd.DataFrame, predictions: pd.DataFrame, metrics: pd.DataFrame):
    """Save the two requested figures."""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    # Visualization 1: points per game compared with each rookie outcome.
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    colors = plt.get_cmap("tab10")
    for ax, target, title in zip(
        axes,
        TARGETS,
        ["Pre-NBA points per game and rookie PER", "Pre-NBA points per game and rookie Win Shares"],
    ):
        for color_index, (year, group) in enumerate(complete.groupby("DraftYear")):
            ax.scatter(
                group["PTS_per_game"],
                group[target],
                color=colors(color_index),
                alpha=0.72,
                s=34,
                label=str(year),
            )
        x = complete["PTS_per_game"].to_numpy()
        y = complete[target].to_numpy()
        slope, intercept = np.polyfit(x, y, 1)
        line_x = np.linspace(x.min(), x.max(), 100)
        ax.plot(line_x, slope * line_x + intercept, color="#202020", linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Points per game in last available pre-NBA season")
        ax.set_ylabel(f"Rookie-season {target}")
        ax.legend(title="Draft year", frameon=True, fontsize=8)
    fig.suptitle("Pre-NBA scoring and rookie outcomes (complete-case sample)", fontsize=14)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "college_scoring_vs_rookie_outcomes.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    # Visualization 2: actual versus predicted outcomes for the chronological holdout.
    model_names = ["Mean baseline", "Linear regression", "Polynomial regression (degree 2)"]
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    for row_index, target in enumerate(TARGETS):
        target_predictions = predictions[predictions["Target"] == target]
        target_metrics = metrics[metrics["Target"] == target].set_index("Model")
        target_values = target_predictions[["Actual", "Predicted"]].to_numpy().ravel()
        lower, upper = target_values.min(), target_values.max()
        padding = max((upper - lower) * 0.06, 0.5)
        lower -= padding
        upper += padding
        for col_index, model_name in enumerate(model_names):
            ax = axes[row_index, col_index]
            subset = target_predictions[target_predictions["Model"] == model_name]
            ax.scatter(subset["Actual"], subset["Predicted"], alpha=0.76, color="#176B87", s=38)
            ax.plot([lower, upper], [lower, upper], linestyle="--", color="#a23e48", linewidth=1.5)
            score = target_metrics.loc[model_name, "R2"]
            ax.set_title(f"{target}: {model_name}\nHoldout R² = {score:.3f}")
            ax.set_xlabel(f"Actual rookie {target}")
            ax.set_ylabel(f"Predicted rookie {target}")
            ax.set_xlim(lower, upper)
            ax.set_ylim(lower, upper)
    fig.suptitle("Held-out predictions for draft classes 2022-2023", fontsize=15)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "holdout_actual_vs_predicted.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def run_analysis():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    merged, complete = load_data()
    metrics, predictions, models, train, test = fit_and_evaluate(complete)
    make_visualizations(complete, predictions, metrics)

    metrics.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)
    predictions.to_csv(OUTPUT_DIR / "holdout_predictions.csv", index=False)

    print("DATA COVERAGE")
    print(f"Drafted players in each source file: {len(merged)}")
    print(f"Players with a pre-NBA season record: {merged['PreNBASeason'].notna().sum()}")
    print(f"Players with both rookie outcomes: {merged[TARGETS].notna().all(axis=1).sum()}")
    print(f"Complete cases used in the models: {len(complete)}")
    print(f"Training sample (drafts 2018-2021): {len(train)}")
    print(f"Chronological holdout (drafts 2022-2023): {len(test)}")
    print("\nMODEL RESULTS (lower MAE/RMSE is better; higher R² is better)")
    print(metrics.round(3).to_string(index=False))

    print("\nCORRELATIONS WITH ROOKIE OUTCOMES (descriptive only)")
    print(complete[FEATURES + TARGETS].corr(numeric_only=True)[TARGETS].round(3).to_string())

    for target in TARGETS:
        model = models[(target, "Linear regression")]
        coefficients = pd.Series(
            model.named_steps["regressor"].coef_,
            index=FEATURES,
            name="Standardized coefficient",
        ).sort_values(key=lambda values: values.abs(), ascending=False)
        print(f"\nSTANDARDIZED LINEAR COEFFICIENTS FOR {target}")
        print(coefficients.round(3).to_string())

    best_models = metrics.loc[metrics.groupby("Target")["MAE"].idxmin(), ["Target", "Model", "MAE", "RMSE", "R2"]]
    print("\nLOWEST-HOLDOUT-MAE MODEL BY TARGET (descriptive selection only)")
    print(best_models.round(3).to_string(index=False))

    print(f"\nFigures and result tables saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()
