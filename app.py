from pathlib import Path
import calendar
import json

import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_ROOT = ROOT / 'artifacts' if (ROOT / 'artifacts/model_info.json').exists() else ROOT
st.set_page_config(page_title='Bike demand | Team 404', page_icon='🚲', layout='wide')

st.markdown('''
<style>
:root {color-scheme: light;}
.stApp {background: #f7f8f6; color: #202923;}
[data-testid="stHeader"] {background: transparent;}
[data-testid="stMainBlockContainer"] {max-width: 1100px; padding: 2rem 2rem 1.5rem;}
[data-testid="stVerticalBlock"] {gap: .7rem;}
h1,h2,h3,p,label {font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
h1 {font-size: 2rem !important; font-weight: 600 !important; letter-spacing: -.07rem; padding: 0 !important;}
h3 {font-size: .95rem !important; font-weight: 600 !important; padding: 0 !important;}
[data-testid="stForm"] {padding: 1.15rem; background: #fff; border: 1px solid #dfe5df; border-radius: 12px;}
[data-testid="stWidgetLabel"] p {font-size: .78rem; color: #536158;}
[data-baseweb="select"] > div,[data-testid="stNumberInputContainer"] {border-radius: 7px;}
[data-testid="stFormSubmitButton"] button {min-height: 2.4rem; border-radius: 7px; font-weight: 600;}
[data-testid="stMetricLabel"] p {font-size: .76rem; color: #647168;}
[data-testid="stMetricValue"] {font-size: 2.6rem; font-weight: 550; letter-spacing: -.08rem;}
.st-key-result {padding: 1.15rem 1.25rem .8rem; border-radius: 12px; border: 1px solid #dfe5df; background: #fff;}
.st-key-secondary [data-testid="stMetricValue"] {font-size: 1.25rem; letter-spacing: -.02rem;}
.st-key-scores [data-testid="stMetricValue"] {font-size: 1.12rem; letter-spacing: -.02rem;}
[data-testid="stCaptionContainer"] p {font-size: .75rem; line-height: 1.45; color: #68766b;}
[data-testid="stExpander"] {border: 1px solid #dfe5df; border-radius: 8px; background: #fff;}
[data-testid="stExpander"] summary p {font-size: .82rem;}
.kicker {font: 600 .65rem/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; letter-spacing: .13em; text-transform: uppercase; color: #65756a;}
.nav {display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;}
.brand {display: flex; align-items: center; gap: .55rem; font-weight: 650; font-size: .85rem;}
.brand-mark {height: 9px; width: 9px; border-radius: 50%; background: #37644b;}
.team {font-size: .7rem; color: #68766b;}
.subline {font-size: .86rem; color: #657168; margin: .3rem 0 1.1rem;}
.result-context {font-size: .73rem; color: #657168; margin-bottom: .1rem;}
.rule {height: 1px; background: #e2e7e0; margin: .35rem 0 .55rem;}
.page-footer {font-size: .69rem; color: #768278; margin-top: .6rem; display: flex; flex-wrap: wrap; gap: .4rem 1rem;}
.page-footer a {color: #52675a; text-decoration: none;}
@media (max-width: 700px) {
 [data-testid="stMainBlockContainer"] {padding: 1.2rem 1rem;}
 h1 {font-size: 1.7rem !important;}
 .nav {margin-bottom: .9rem;}
 .st-key-result {padding: 1rem;}
 [data-testid="stForm"] [data-testid="stHorizontalBlock"], .st-key-secondary [data-testid="stHorizontalBlock"], .st-key-scores [data-testid="stHorizontalBlock"] {flex-wrap: nowrap;}
 [data-testid="stForm"] [data-testid="stColumn"], .st-key-secondary [data-testid="stColumn"], .st-key-scores [data-testid="stColumn"] {min-width: 0; width: auto; flex: 1 1 0;}
 [data-testid="stForm"] [data-testid="stNumberInput"] button {display: none;}
 .st-key-scores [data-testid="stMetricValue"] {font-size: .95rem;}
 .st-key-scores [data-testid="stMetricLabel"] p {font-size: .68rem;}
}
</style>
''', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load(MODEL_ROOT / 'pipeline.joblib')

if not (MODEL_ROOT / 'model_info.json').exists():
    st.info('The trained model is not available yet. Complete model evaluation before using this tool.')
    st.stop()

info = json.loads((MODEL_ROOT / 'model_info.json').read_text())
model = load_model()
weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
weather_names = {1: 'Clear / partly cloudy', 2: 'Mist / cloudy', 3: 'Light rain / snow'}
default = dict(mnth=6, hr=8, weekday=1, holiday=0, weathersit=1, temp=(20+8)/47, hum=.6, windspeed=10/67)

st.markdown('<div class="nav"><div class="brand"><span class="brand-mark"></span>Bike demand</div><span class="team">ICT336 / TEAM 404</span></div>', unsafe_allow_html=True)
st.title('Plan for the busy hours.')
st.markdown('<div class="subline">Explore hourly rental demand for a bike-sharing capacity review.</div>', unsafe_allow_html=True)

form_column, result_column = st.columns([1, 1.3], gap='medium')
with form_column:
    with st.form('conditions', border=True):
        st.markdown('<div class="kicker">Your scenario</div>', unsafe_allow_html=True)
        a, b = st.columns(2, gap='small')
        with a:
            month = st.selectbox('Month', range(1, 13), index=5, format_func=lambda n: calendar.month_name[n])
            day = st.selectbox('Day of week', range(7), index=1, format_func=lambda n: weekdays[n])
        with b:
            hour = st.selectbox('Hour', range(24), index=8, format_func=lambda h: f'{h:02d}:00')
            weather = st.selectbox('Weather', [1, 2, 3], format_func=lambda n: weather_names[n])
        a, b, c = st.columns(3, gap='small')
        with a:
            temperature = st.number_input('Temp (°C)', min_value=-8., max_value=39., value=20., step=.5)
        with b:
            humidity = st.number_input('Humidity (%)', min_value=0, max_value=100, value=60, step=1)
        with c:
            wind = st.number_input('Wind (km/h)', min_value=0., max_value=67., value=10., step=.5)
        holiday = st.checkbox('Public holiday', help='Uses the historical Washington, DC holiday definition.')
        submitted = st.form_submit_button('Update estimate', type='primary', use_container_width=True)
        st.caption('Adjust the conditions, then update. No form inputs are saved to files or databases.')

if submitted:
    st.session_state['last_conditions'] = dict(
        mnth=month, hr=hour, weekday=day, holiday=int(holiday), weathersit=weather,
        temp=(temperature+8)/47, hum=humidity/100, windspeed=wind/67,
    )
# Only the current interactive session holds the last submitted scenario.
# There are no writes of form inputs to files, databases, or application logs.
row = st.session_state.get('last_conditions', default)
prediction = float(model.predict(pd.DataFrame([row]))[0])
scenarios = pd.DataFrame([{**row, 'hr': h} for h in range(24)])
curve = np.maximum(0, model.predict(scenarios))
peak_hour = int(np.argmax(curve))

with result_column:
    with st.container(key='result'):
        st.markdown('<div class="kicker">Demand estimate</div>', unsafe_allow_html=True)
        context = f"{weekdays[row['weekday']]} · {calendar.month_abbr[row['mnth']]} · {row['hr']:02d}:00"
        st.markdown(f'<div class="result-context">{context}</div>', unsafe_allow_html=True)
        st.metric('Estimated rentals / hour', f'{max(0, prediction):,.0f}')
        with st.container(key='secondary'):
            a, b = st.columns(2)
            a.metric('Busiest hour', f'{peak_hour:02d}:00')
            b.metric('Peak rentals / hour', f'{curve[peak_hour]:,.0f}')
        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        st.markdown('### Compare all 24 hours')
        st.line_chart(
            pd.DataFrame({'Hour': range(24), 'Rentals': curve}).set_index('Hour'),
            color='#37644B', height=180, x_label='Hour', y_label='Rentals',
        )
        st.caption('Same weather throughout. A scenario comparison, not a day-ahead forecast.')
    st.caption(f'Review capacity and staffing before {peak_hour:02d}:00. Counts cover the whole system; they do not specify bikes needed at one station.')
    if prediction < 0:
        st.caption('Negative model output is displayed as zero. Evaluation uses original predictions.')

scores = info['test_scores']
with st.container(key='scores'):
    a, b, c = st.columns(3)
    a.metric('Model test MAE', f"{scores['mae']:.1f} rentals")
    b.metric('Baseline test MAE', f"{scores['baseline_mae']:.1f} rentals")
    c.metric('Error reduction', f"{scores['relative_mae_reduction']:.1%}")

with st.expander('About the model'):
    st.write(f"**{info['selected_model']}** estimates total system-wide rentals in one observed hour. Preprocessing and prediction use the saved scikit-learn Pipeline.")
    st.write('Models were compared with five chronological validation folds against a Dummy median baseline, then tuned using development data.')
    st.write(f"Final test: {info['test_start'][:10]} to {info['test_end'][:10]}. RMSE: {scores['rmse']:.2f} rentals. R²: {scores['r2']:.3f}.")
    st.write('MAE is average absolute prediction error per observed hour. Error reduction is relative to the baseline; it is not accuracy or an uncertainty interval.')

with st.expander('Data, privacy and limitations'):
    st.markdown('**Source:** [UCI Bike Sharing](https://doi.org/10.24432/C5W894), Fanaee-T (2013). Capital Bikeshare, Washington, DC, 2011–2012. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).')
    st.write('**Privacy:** Conditions are processed in memory during the current session. The application does not save them to files or databases or request personal information. Hosting infrastructure may retain ordinary connection logs.')
    st.write('**Limits:** Historical Washington, DC data is not validated for current operations, Thailand, station availability or extreme conditions. Future weather is uncertain, and model associations do not establish causes. Displayed predictions are rounded and clipped at zero; evaluation scores use raw outputs.')

st.markdown('<div class="page-footer"><span>Historical Washington, DC demonstration</span><span>No personal information requested</span><a href="https://github.com/BhoneMyatKyaw666/ICT336-Team404-BikeDemand" target="_blank" rel="noopener noreferrer">Project source ↗</a></div>', unsafe_allow_html=True)
