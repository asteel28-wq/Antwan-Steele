from pathlib import Path
import pandas as pd
from IPython.display import Image, display
from nba_rookie_analysis import DATA_DIR, OUTPUT_DIR, FEATURES, TARGETS, load_data

merged, complete = load_data()
coverage = pd.DataFrame({
    "Measure": [
        "Drafted players in both source files",
        "Players with a pre-NBA season record",
        "Players with both rookie outcomes",
        "Complete cases used in both models",
        "Training players (draft years 2018-2021)",
        "Holdout players (draft years 2022-2023)",
    ],
    "Count": [
        len(merged),
        int(merged["PreNBASeason"].notna().sum()),
        int(merged[TARGETS].notna().all(axis=1).sum()),
        len(complete),
        int(complete["DraftYear"].between(2018, 2021).sum()),
        int(complete["DraftYear"].between(2022, 2023).sum()),
    ],
})
display(coverage)



display(complete[FEATURES + TARGETS].describe().T.round(3))
print("Draft-year sample sizes:")
display(complete.groupby("DraftYear").size().rename("Complete players").to_frame())
print("Feature correlations with the outcomes (descriptive, not causal):")
display(complete[FEATURES + TARGETS].corr(numeric_only=True)[TARGETS].round(3))



from nba_rookie_analysis import fit_and_evaluate, make_visualizations

metrics, predictions, fitted_models, train, test = fit_and_evaluate(complete)
make_visualizations(complete, predictions, metrics)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
metrics.to_csv(OUTPUT_DIR / "model_metrics.csv", index=False)
predictions.to_csv(OUTPUT_DIR / "holdout_predictions.csv", index=False)
display(metrics.round(3))
print(f"Training sample: {len(train)} players; chronological holdout: {len(test)} players.")



from nba_rookie_analysis import FIGURE_DIR
display(Image(filename=str(FIGURE_DIR / "college_scoring_vs_rookie_outcomes.png")))
display(Image(filename=str(FIGURE_DIR / "holdout_actual_vs_predicted.png")))



coefficient_tables = {}
for target in TARGETS:
    model = fitted_models[(target, "Linear regression")]
    coefficients = pd.Series(
        model.named_steps["regressor"].coef_,
        index=FEATURES,
        name=f"{target} standardized coefficient",
    ).sort_values(key=lambda values: values.abs(), ascending=False)
    coefficient_tables[target] = coefficients
    print(target)
    display(coefficients.to_frame().round(3))

print("Holdout players with the largest polynomial-model absolute errors:")
poly_errors = predictions[
    predictions["Model"] == "Polynomial regression (degree 2)"
].copy()
poly_errors["Absolute error"] = (poly_errors["Actual"] - poly_errors["Predicted"]).abs()
for target in TARGETS:
    print(target)
    display(
        poly_errors[poly_errors["Target"] == target]
        .nlargest(5, "Absolute error")[
            ["DraftYear", "Player", "Actual", "Predicted", "Absolute error"]
        ]
        .round(2)
    )



    