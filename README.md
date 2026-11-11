# Team 404 — Bike rental demand explorer

A course demonstration estimating hourly system-wide bike rentals from supplied calendar and weather conditions. Includes a real trained scikit-learn Pipeline, a 24-hour scenario chart and final chronological test scores. Form inputs are not stored by the application.

## Model and evaluation

Gradient Boosting, selected against Ridge and Random Forest using five expanding chronological validation folds, with a Dummy median baseline. Preprocessing is within the Pipeline. The latest 20% of dates was held out until final evaluation; test period and all scores are loaded from model_info.json.

This is a historical Washington, DC demonstration, not a validated current forecast or a station-level inventory tool. Future weather is uncertain. The hourly comparison holds weather constant; it is not a causal analysis. Working/non-working-day error comparisons are operational checks, not demographic fairness evidence.

## Source and licence

Fanaee-T, H. (2013). Bike Sharing [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894. Data source licensed CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Capital Bikeshare observations, 2011–2012. Target components casual and registered were excluded as predictors.

## AI assistance

Codex assisted with planning, code drafting, execution and testing. Team 404 remains responsible for verification, understanding and final submitted work. A detailed AI-use log and training notebook are maintained with the coursework project.

## Runtime

Render Docker web service, Free instance, Python 3.14, Streamlit port 7860. Exact direct dependency versions are in requirements.txt. No API keys required. Load only the included trusted pipeline.

## Deployment

Connect this repository to Render as a Docker Web Service and select the Free instance. The included render.yaml also supports Blueprint deployment. The health endpoint is /_stcore/health. Free services sleep when idle; open the website before the demo. Do not choose a paid instance unless your team decides to pay.
