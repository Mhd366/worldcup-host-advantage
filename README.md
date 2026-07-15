cat > ~/worldcup-host-advantage/README.md << 'EOF'
# 🏆 World Cup Host Advantage & Saudi Arabia 2034

Analyzing 964 FIFA World Cup matches (1930–2022) to measure the **host-nation advantage** and what it could mean for **Saudi Arabia 2034**.

## 🔗 Live Dashboard
👉 [Open the Streamlit app](https://worldcup-host-advantage-g35w4qittghtbcxw6cwykm.streamlit.app/)

## 📊 Key Findings
- Host nations win **62.7%** of matches vs **38.6%** for an average team (+24pp).
- Host matches draw far bigger crowds (~70k vs ~40k median).
- A logistic model (65.3% accuracy) attributes **+22.5pp** to hosting.
- For Saudi Arabia 2034: win chance rises from **33.7%** to **56.2%** as host.
- Economically, hosting brings no lasting GDP boost (avg change −0.99pp).

## 📁 Project Structure
- `notebooks/analysis.ipynb` — full analysis (cleaning, EDA, model, economics)
- `app/app.py` — interactive Streamlit dashboard
- `data/raw/` — original datasets · `data/clean/` — cleaned data
- `assets/` — exported charts

## ⚙️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## 🛠️ Tools
Python · pandas · numpy · matplotlib · seaborn · scikit-learn · Streamlit · Plotly

## 📚 Data Sources
- FIFA World Cup 1930–2022 All Matches (Kaggle)
- GDP growth: World Bank Open Data
EOF
