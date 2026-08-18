# WHO Life Expectancy Measurements Project
## Project scope and motivation
Life expectancy is a statistical measurement used to estimate an individual's lifespan.

At an individual level, life expectancy is important for determining plans, support, and care. At a larger-group level, it has significant socioeconomic implications.

At a country level, life expectancy data can be used to derive insights, perform analytics, and support further studies into population needs and risk factors.

## Project goal
The data analytics team must produce predictions of life expectancy across countries globally.

The data was provided by the World Health Organisation (WHO). It contains records from:

- 2000 to 2015.
- 179 countries.

## Data integrity and ethical considerations
Data integrity is a major focus of the project.

Several countries have expressed concerns about sharing sensitive data, including medical records. Correlating sensitive medical data with quality-of-life measurements may create unwanted financial implications and hinder social development.

The team must construct two predictive models:

1. A minimal model that uses the least information necessary to make a prediction.
2. A more elaborate model that can be used if countries decide to share additional sensitive data.

The team must use its judgement as ethical data practitioners when deciding which features may or should be used.

## Application output
The team must produce a function that:

- Accepts relevant population statistics as input features.
- Predicts average life expectancy.
- Asks the user the following question:

  "Do you consent to using advanced population data, which may include protected information, for better accuracy? (Y/N)"

- Selects the model based on the user's answer.

If the user consents to advanced population data, the more elaborate model may be used. Otherwise, the minimal model should be used.

## Competitor baseline
Another contractor team has been engaged to compare results and cross-validate the work.

The competing team has produced a semi-robust model with an RMSE of 1.8.

This RMSE should be treated as the baseline. The project team should aim to achieve an RMSE below 1.8 to improve the likelihood of securing further collaboration with WHO.

## Requirements
The project requires the team to:

- Build two continuous predictive models using linear regression:
  - One best-performing model.
  - One minimalistic model.
- Deploy both models through an interactive function.
- Consider ethical issues relating to the use of population data and potentially protected information.

## Deliverables
Required deliverables include:

- Streamlit files containing the code and project work.
- A single file containing the prediction function.
- A link to a live Streamlit application, if available. This is optional.
