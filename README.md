# Evaluating the Impact of Policy Changes on Economic Outcomes

## Project Overview

This project implements a regression-based counterfactual analysis to evaluate how hypothetical reductions in commercial electricity demand may affect residential electricity prices across U.S. states and the District of Columbia.

The analysis is motivated by growing electricity demand from large-load users, including AI and data-center infrastructure. Commercial electricity demand is used as an observable load measure and is not treated as direct data-center electricity consumption.

## Research Question

**How would predicted residential electricity prices change if commercial electricity demand were reduced by 5%, 10%, or 15% relative to observed conditions?**

## Project Files

- `Evaluating the Impact of Policy Changes on Economic Outcomes.ipynb` - Google Colab notebook containing the complete analysis workflow.
- `PhDAI730_Project 2 - Evaluating the Impact of Policy Changes on Economic Outcomes.docx` - Final written report.
- `README.md` - Project setup, execution, and reproducibility documentation.

## Data Source

Historical electricity data are retrieved programmatically from the U.S. Energy Information Administration (EIA) Open Data API.

**API endpoint**

`https://api.eia.gov/v2/electricity/retail-sales/data/`

**EIA API registration**

https://www.eia.gov/opendata/register.php

The analysis includes:
 
- Monthly observations from January 2015 through December 2025
- 50 U.S. states plus the District of Columbia
- Residential, commercial, and industrial electricity sectors
- Residential electricity prices
- Residential, commercial, and industrial electricity sales
 
After preprocessing and feature engineering, the final modeling dataset contains 6,120 state-month observations.
 
EIA Open Data:
https://www.eia.gov/opendata/

## Notebook Structure

The notebook is organized into modular sections that correspond to the project requirements.

### Environment Setup
- Import Libraries and Project Configuration

### Data Loading and Preprocessing
- EIA API Configuration 
- Load Historical Electricity Data
- Data Inspection 
- Data Cleaning and Reshaping 
- Missing Data Handling
- Feature Engineering 
- Exploratory Data Analysis
- Chronological Train/Test Split
- Normalize Model Predictors

### Model Implementation
- Regression Model
- Model Evaluation
- Model Coefficients Analysis

### Simulation and Result Generation
- Counterfactual Simulation
- Counterfactual Visualization
- Final Results Summary

The code includes comments identifying the purpose of each major data-processing, modeling, and simulation step.
 
## Data Preprocessing
 
The preprocessing workflow:
 
- Converts API fields to appropriate date and numeric formats
- Restricts the sample to the 50 states and District of Columbia
- Retains residential, commercial, and industrial electricity sectors
- Checks for duplicate state-month-sector observations
- Evaluates missing values
- Screens non-positive observations
- Applies natural-log transformations to electricity-sales variables
- Calculates year-over-year commercial electricity-demand growth
- Creates a 12-month lag of residential electricity prices
- Adds seasonal controls
- Standardizes continuous model predictors
 
Continuous predictors are standardized using `StandardScaler`. The scaler is fitted only on the training data and subsequently applied to the test data to prevent data leakage.
 
## Train/Test Design
 
A chronological train/test split is used:
 
- **Training period:** January 2016 through December 2023
- **Testing period:** January 2024 through December 2025
 
This approach evaluates the model on later observations that were excluded from model estimation.
 
## Model
 
The project uses an interpretable regression-based panel-style model implemented with `statsmodels`.
 
The model includes:
 
- Commercial electricity sales
- Residential electricity sales
- Industrial electricity sales
- Year-over-year commercial demand growth
- 12-month lagged residential electricity price
- Seasonal controls
- State fixed effects
- State-clustered standard errors
 
## Counterfactual Simulation
 
Four demand conditions are evaluated:
 
- **Baseline:** 0% reduction
- **Scenario 1:** 5% reduction
- **Scenario 2:** 10% reduction
- **Scenario 3:** 15% reduction
 
For each counterfactual scenario, commercial electricity demand is reduced by the specified percentage while the other modeled characteristics are held constant. The transformed demand feature is recalculated and passed through the training-fitted scaler and regression model to generate counterfactual residential electricity-price predictions.
 
The resulting estimates are model-based counterfactual outcomes and should not be interpreted as causal effects.
 
## Model Performance
 
The final model achieved:
 
- Training R²: 0.940
- Testing R²: 0.938
- Testing MAE: 1.007 cents/kWh
- Testing RMSE: 1.593 cents/kWh
 
## Key Counterfactual Result
 
The baseline predicted residential electricity price was 17.321 cents/kWh.
 
Under the 10% commercial demand-reduction scenario, the predicted price was 17.349 cents/kWh, representing an estimated increase of:
 
- 0.028 cents/kWh
- 0.16%
 
Detailed interpretation, policy implications, assumptions, and limitations are provided in the accompanying project report.
 
## Running the Notebook in Google Colab
 
1. Open `W5P2.ipynb` in Google Colab.
2. Obtain a free EIA Open Data API key from:
https://www.eia.gov/opendata/register.php
3. Select **Runtime > Run all**, or execute Cells 1-16 sequentially.
4. Enter the EIA API key when prompted.
5. Allow the notebook to download and preprocess the EIA data.
6. Review the generated model metrics, coefficient estimates, counterfactual scenarios, and figures.
 
The API key is entered securely at runtime using `getpass` and should not be stored in the notebook or README.
 
No local source-data file is required because the historical electricity data are retrieved directly from the EIA API.
 
## Python Dependencies
 
The notebook uses libraries available in the standard Google Colab environment:
 
- `pandas`
- `numpy`
- `requests`
- `matplotlib`
- `seaborn`
- `statsmodels`
- `scikit-learn`
 
## Reproducibility
 
The notebook is designed to be reproducible and contains all code required for data collection, preprocessing, feature engineering, normalization, model estimation, evaluation, counterfactual simulation, and result generation.
 
To reproduce the submitted analysis:
 
1. Use Google Colab with the required Python libraries.
2. Obtain a valid EIA Open Data API key.
3. Run all notebook cells sequentially without changing the configured analysis period, train/test split, or policy scenarios.
4. Retrieve monthly EIA electricity data for January 2015 through December 2025 using the notebook's API workflow.
 
Because the EIA API is a live data source, future revisions to historical observations may result in minor differences when the notebook is rerun. The submitted notebook preserves the outputs generated for this project and provides a reference for validating reproduction.
 
No synthetic data are used.
 
## References
 
Smith, S. J., Hubbard, A., Newkirk, A., Ganeshalingam, M., Holecek, B., Sartor, D. A., Mills, M., & Shehabi, A. (2026). *United States data center energy usage report: 2025 update*. Lawrence Berkeley National Laboratory. https://doi.org/10.71468/P1RP4F
 
U.S. Energy Information Administration. (2026). *Open data*. U.S. Department of Energy. https://www.eia.gov/opendata/
