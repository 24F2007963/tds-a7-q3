# analysis.py
# Author: 24f2007963@ds.study.iitm.ac.in
# Interactive Marimo notebook for exploring relationships in a dataset

import marimo

__generated_with = "0.6.23"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    # Create an interactive slider widget (0–100)
    slider = mo.ui.slider(0, 100, value=50, label="Select X value")
    slider
    return slider,
# ^ This cell defines the slider widget


@app.cell
def __(slider):
    # Dynamic markdown based on slider state
    mo.md(f"### Current Slider Value: **{slider.value}**")
    # This markdown updates whenever the slider changes
    return
# ^ This cell depends on the slider


@app.cell
def __(slider):
    # Second dependency: perform computation using slider value
    y = slider.value ** 2
    f"Computed Y = {y}"
    return y,
# ^ Demonstrates data dependency: y depends on slider


@app.cell
def __(mo, slider, y):
    # Final visualization or explanation
    mo.md(f"""
    #### Data Flow
    - Slider Value: **{slider.value}**
    - Computed Y (X²): **{y}**

    This shows how widget state flows into calculations and markdown output.
    """)
    return
# ^ Self-documenting output
