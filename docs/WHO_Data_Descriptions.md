|Field|Description|Status|Feature|
|:---|:---|:---|:---|
|Life expectancy|Average life expectancy of both genders in different years from 2010 to 2015|Target|Drop|
|**Core Data**|**This is core data to use for identification of the record**|**Insensitive**|**---**|
|Country|List of the 179 countries|Insensitive|Drop|
|Region|179 countries are distributed in 9 regions. E.g. Africa, Asia, Oceania, European Union, Rest of Europe and etc.|Insensitive|Keep|
|Year|Years observed from 2000 to 2015|Insensitive|Keep|
|**Status**|**Developed or Developing status**|**Insensitive**|**---**|
|Developing country|Developing country|Insensitive|Drop|
|Developed country|Developed country|Insensitive|Keep|
|**Economic Data**|**Economic factors for those countries**|**Insensitive**|**---**|
|GDP/capita|GDP per capita in current USD|Insensitive|Keep|
|Population|Total population in millions|Insensitive|Keep|
|Schooling|Average years that people aged 25+ spent in formal education|Insensitive|Keep|
|**Mortality Data**|**Data on mortality rates per age group**|**Sensitive**|**---**|
|Adult Mortality|Represents deaths of adults (adults was not defined at source) per 1000 population|Sensitive|Keep|
|HIV/AIDS|Incidents of HIV per 1000 population aged 15-49|Sensitive|Keep|
|Under-five deaths|Represents deaths of children under five years old per 1000 population|Sensitive|Keep|
|Infant deaths|Represents infant deaths per 1000 population|Sensitive|Drop|
|**Weight Data**|**Data on the weight as a measure of health for the population**|**Sensitive**|**---**|
|BMI|BMI is a measure of nutritional status in adults. It is defined as a person's weight in kilograms divided by the square of that person's height in meters (kg/m2)|Sensitive|Keep|
|Thinness 10-19 years|Prevalence of thinness among adolescents aged 10-19 years. BMI < -2 standard deviations below the median.|Sensitive|Keep|
|Thinness 5-9 years|Prevalence of thinness among children aged 5-9 years. BMI < -2 standard deviations below the median.|Sensitive|Drop|
|**Substance Data**|**Data on substance usage for adults within that country**|**Sensitive**|**---**|
|Alcohol|Represents alcohol consumption that is recorded in liters of pure alcohol per capita with 15+ years old|Sensitive|Keep|
|**Immunization Data**|**Data on the immunization of the population using specific treatments**|**Sensitive**|**---**|
|Hepatitis B|Represents % of coverage of Hepatitis B (HepB3) immunization among 1-year-olds.|Sensitive|Keep|
|Measles|Represents % of coverage of Measles containing vaccine first dose (MCV1) immunization among 1-year-olds|Sensitive|Keep|
|Polio|Represents % of coverage of Polio (Pol3) immunization among 1-year-olds.|Sensitive|Drop|
|Diphtheria|Represents % of coverage of Diphtheria tetanus toxoid and pertussis (DTP3) immunization among 1-year-olds.|Sensitive|Keep|

## Multicollinearity choices
We identified three pairs of potential features that largely increased VIF due to high correlation.
Below, with the assistance of AI research tools, and thorough research, we have identified two to three reasons for keeping one factor over the other.

### Choosing Diptheria over Polio
> Gold Standard for Routine Health Systems: The World Health Organisation (WHO) officially uses DTP3 coverage as the primary international benchmark to measure the strength and reach of a country's routine everyday healthcare system. [WHO Indicator: DTP3 immunization coverage among 1-year-olds (%)](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/88) [Poliomyelitis vaccination coverage - Reference](https://immunizationdata.who.int/global/wiise-detail-page/poliomyelitis-vaccination-coverage?CODE=Global&ANTIGEN=&YEAR=)

> Shows clinic quality: Polio drops are often handed out quickly on the street, but DTP3 shots require an actual clinic visit. High DTP3 rates prove a country has real, clean hospitals for mothers and babies, which naturally keeps people living longer.

### Choosing Under-five deaths over Infant deaths
> Captures Broader Socioeconomic Strain: Under-five deaths captures the extended risks a child faces as they transition to solid foods and interact with the environment, making it a better reflection of long-term malnutrition, unsafe water, and poverty.

> Mathematical Inclusivity: Because under-five deaths mathematically includes infant deaths, choosing this variable ensures you do not lose the infant data; you simply expand it to include the critical toddler years. [WHO Indicator: Under-five mortality rate (per 1000 live births)](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/7)

### Choosing Thinness 10-19 over Thinness 5-9
> Captures Adolescent Growth Spurts: The 10–19 age bracket spans puberty, a critical developmental window where nutritional deficits cause severe, permanent stunting and lifelong health impacts.

> Reflects School-Age and Independence Risks: This older cohort reflects the cumulative impact of school nutrition programmes (or lack thereof) and independent dietary habits, showing how health shifts as children grow outside early maternal care.

> Showcases Continuance of Life Expectancy: Extending the tracked window to age 5 bridges the gap to overall life expectancy. Since the sharpest drop in early-life mortality happens before age 5, capturing survival past this critical threshold serves as a stronger baseline for predicting long-term survival and overall lifespan trends.
