# 24f2007963@ds.study.iitm.ac.in
# Marimo notebook style script (cell markers compatible with VS Code / Jupyter)
# Author: Technical Data Scientist
# Purpose: Interactive demo showing relationships between variables with widgets
# NOTE: Requires: pandas, matplotlib, seaborn, ipywidgets, numpy

# %% [markdown]
# # Interactive Data Analysis (Marimo notebook style)
#
# This notebook demonstrates variable dependencies, an interactive slider widget,
# and dynamic markdown output that updates based on the widget state.
#
# Contact: 24f2007963@ds.study.iitm.ac.in

# %%
# Cell 1 — Imports & Data Loading
# This cell produces `df_raw` that downstream cells depend on.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets

# For consistent plots in notebooks
plt.rcParams["figure.figsize"] = (8, 4)

# Data flow comment:
# - df_raw is the source dataset; all derived variables should be computed from it.
# - If df_raw changes, downstream computed variables must be recomputed.

# Load a demonstration dataset (Seaborn's 'tips'). Replace with your dataset as needed.
df_raw = sns.load_dataset("tips")
display(Markdown("**Loaded dataset:** `tips` — first 5 rows"))
display(df_raw.head())

# %%
# Cell 2 — Derived variables (dependent on df_raw)
# Compute summary statistics and derived predictors that depend on df_raw.
# If df_raw changes, re-run this cell to update these derived variables.

# Group-level aggregates used later in plots and interactive output
mean_tip_by_day = df_raw.groupby("day")["tip"].mean().rename("mean_tip").reset_index()
median_total_by_day = df_raw.groupby("day")["total_bill"].median().rename("median_total").reset_index()

display(Markdown("**Derived variables computed:** `mean_tip_by_day`, `median_total_by_day`"))
display(mean_tip_by_day)
display(median_total_by_day)

# %%
# Cell 3 — Interactive widget and dynamic markdown output
# This cell sets up a slider that filters rows by a minimum total_bill threshold.
# Variable dependency: filtered_df depends on df_raw and slider value.
# The dynamic Markdown output depends on `filtered_df` and updates when the slider moves.

# Slider: choose minimum total bill to filter the dataset.
min_bill_slider = widgets.FloatSlider(
    value=10.0,
    min=float(df_raw["total_bill"].min()),
    max=float(df_raw["total_bill"].max()),
    step=0.5,
    description="Min bill:",
    continuous_update=False,
    style={"description_width": "initial"},
    layout=widgets.Layout(width="60%")
)

# Dropdown to choose which summary metric to show
metric_dropdown = widgets.Dropdown(
    options=[("Mean tip", "mean_tip"), ("Median total bill", "median_total"), ("Count", "count")],
    value="mean_tip",
    description="Metric:",
    style={"description_width": "initial"},
)

# Output area to render dynamic Markdown and matplotlib figures
out = widgets.Output()

def update_output(change=None):
    """Recompute dependent variables and update the markdown + plot."""
    with out:
        clear_output(wait=True)
        threshold = min_bill_slider.value

        # filtered_df depends on df_raw and the slider threshold
        filtered_df = df_raw[df_raw["total_bill"] >= threshold].copy()

        # Recompute group summaries on the filtered data
        grouped = filtered_df.groupby("day").agg(
            mean_tip=("tip", "mean"),
            median_total=("total_bill", "median"),
            count=("tip", "size")
        ).reset_index()

        # Dynamic markdown summary depending on selected metric
        metric = metric_dropdown.value
        if grouped.empty:
            display(Markdown(f"**No rows** with `total_bill >= {threshold:.2f}`. Try lowering the threshold."))
            return

        if metric == "mean_tip":
            best_day = grouped.loc[grouped["mean_tip"].idxmax()]
            display(Markdown(f"### Filter: `total_bill >= {threshold:.2f}`\n"
                             f"- **Avg tip (by day)**: highest on **{best_day['day']}** at **{best_day['mean_tip']:.2f}**"))
        elif metric == "median_total":
            best_day = grouped.loc[grouped["median_total"].idxmax()]
            display(Markdown(f"### Filter: `total_bill >= {threshold:.2f}`\n"
                             f"- **Median total bill (by day)**: highest on **{best_day['day']}** at **{best_day['median_total']:.2f}**"))
        else:
            best_day = grouped.loc[grouped["count"].idxmax()]
            display(Markdown(f"### Filter: `total_bill >= {threshold:.2f}`\n"
                             f"- **Row count (by day)**: highest on **{best_day['day']}** at **{best_day['count']}**"))

        # Small visualization — dependent on grouped (which depends on filtered_df)
        fig, ax = plt.subplots()
        ax.bar(grouped["day"], grouped["mean_tip"], alpha=0.8)
        ax.set_ylabel("Mean tip")
        ax.set_title(f"Mean tip by day (total_bill >= {threshold:.2f})")
        plt.show()

# Wire up widget event handlers (recompute when slider or dropdown changes)
min_bill_slider.observe(update_output, names="value")
metric_dropdown.observe(update_output, names="value")

# Initial render
display(widgets.VBox([min_bill_slider, metric_dropdown, out]))
update_output()

# %%
# Cell 4 — Mathematical equations & documentation (static)
# This cell shows algorithmic complexity examples (KaTeX-style strings in markdown).
display(Markdown("## Algorithmic Complexity (examples)"))
display(Markdown(r"$T(n) = O(n \log n)$ — sorting step"))
display(Markdown(r"$S(n) = O(n)$ — space complexity"))

# Data flow note:
# - Changing df_raw (e.g., loading a new dataset) -> re-run Cell 2 to recalc derived variables
# - Slider / dropdown interact with df_raw-derived variables via Cell 3's `update_output`
# - This structure keeps computations incremental and reproducible
