
# Smart Grid Pricing Optimisation and Flexibility Scoring

This project explores household electricity usage under Agile (dynamic) pricing to explore household cost optimisation strategies and evaluate event-based flexibility potential. It includes exploratory analysis, cost model, and event-based flexibility score.

---

## Problem Framing

Smart grids enable households to shift energy usage away from peak price periods. This notebook explores simulated household energy and pricing data to:
- Identify usage and pricing alignment
- Estimate potential cost reduction from behavioural change (through automation or shifting load)
- Score households based on flexibility event alignment

---

## Files

- `Komodo_Energy.ipynb` – Fully structured notebook (load → explore → model → insights)
- `household_usage.csv` – Simulated 30-min electricity usage for 3 household types
- `agile_price_example.json` – Agile pricing data (Octopus)
- `flexibility_opportunity.json` – Event-based incentive windows
- `README.md` - README included
- `dashboard.py` - Streamlit dashboard summary
- `household_usage_cleaned.csv` - The cleaned CSV file used for optimisation model/scoring summary

> Each section includes annotated markdown summaries to explain modelling decisions and visual insights.

---

## Setup Instructions

### Jupyter Notebook
1. Clone the repo  
2. Install dependencies:  
   ```bash
   pip install pandas matplotlib seaborn scikit-learn
   ```
3. Run the notebook:  
   ```bash
   jupyter notebook Komodo_Energy.ipynb
   ```

### Streamlit Dashboard
1. Run:
   ```bash
   streamlit run dashboard.py
   ```
2. Explore usage, cost summaries and flexbility scoring by household type

---

## Key Assumptions

- One-day simulation (March 13, 2025)
- Flat tariff: £0.20/kWh
- No thermal/device constraints in the optimiser
- Incentives are applied as fixed values per kWh in event scoring

---

## Key Insights

- Evening usage peaks overlap with Agile price spikes, especially for heat pump households.
- A simple rule-based optimisation can cut costs by 15–25% if only 40% of load is shifted.
- Flex scoring reveals strong alignment with turn-down events for specific household types.

## Notebook Structure

1. **Load & Clean Data**: Handle time formatting and household reshaping
2. **Merge Agile Pricing**: Align timestamps and calculate costs
3. **EDA**:
   - Hourly usage trends
   - Peak load and pricing alignment
   - Cost comparison: Agile vs Flat
4. **Modelling Directions:**
- Cost Optimisation:
  - Shifts usage away from expensive time slots (rule-based)
  - Simulates capped flexibility to reflect real-world user constraints
- Flexibility Opportunity Scoring:
  - Rewards usage alignment with turn-up / turn-down event windows
  - Scores households based on responsiveness potential
5. **Insights**: Visual and narrative summary with next-step roadmap

---

## Future Work

- Train a classifier to segment users by flexibility or price sensitivity
- Add temperature and behavioural features (weekends, night-time)
- Use LSTM or Prophet for more advanced time series prediction
- Connect with real-time APIs for price/demand streaming
- Deploy into live dashboard with household-specific recommendations

---

## Questions I'd Explore

- How are flexibility signals currently communicated to households?
- What constraints (e.g., heating minimums) exist for demand turn-down?
- Are there backend optimisation engines in use (e.g., linear programming)?
- How often do flexibility events actually align with peak pricing?

---

*Built by Rashmil Sinha | [GitHub](https://github.com/rashSinha)*
