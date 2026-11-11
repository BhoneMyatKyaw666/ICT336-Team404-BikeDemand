from pathlib import Path
import calendar, json
import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Bike Demand | Team 404', page_icon='🚲', layout='centered')
st.title('🚲 Bike rental demand explorer')
st.write('Estimate system-wide hourly rentals under supplied calendar and weather conditions.')
st.caption('Historical Washington, DC demonstration • Team 404 • No inputs are saved by this application.')

@st.cache_resource
def load_model():
    return joblib.load(ROOT/'pipeline.joblib')

if not (ROOT/'model_info.json').exists():
    st.info('Training draft: the final test is still reserved. Complete the notebook’s final evaluation to enable predictions and verified scores.')
    st.stop()
info = json.loads((ROOT/'model_info.json').read_text())
model = load_model()
with st.form('conditions'):
    month = st.selectbox('Month', range(1,13), index=5, format_func=lambda n: calendar.month_name[n])
    weekday = st.selectbox('Day of week', range(7), index=1, format_func=lambda n: ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][n])
    holiday = st.checkbox('Public holiday (Washington, DC calendar)')
    hour = st.slider('Hour of day', 0, 23, 8)
    weather = st.selectbox('Weather', [1,2,3], format_func=lambda n: {1:'Clear / partly cloudy',2:'Mist / cloudy',3:'Light rain / light snow'}[n])
    temp = st.slider('Temperature (°C)', -8.0, 39.0, 20.0, 0.5)
    humidity = st.slider('Relative humidity (%)', 0, 100, 60)
    wind = st.slider('Wind speed (km/h)', 0.0, 67.0, 10.0, 0.5)
    submitted = st.form_submit_button('Estimate rentals', type='primary')
if submitted:
    row = dict(mnth=month, hr=hour, weekday=weekday, holiday=int(holiday), weathersit=weather,
               temp=(temp+8)/47, hum=humidity/100, windspeed=wind/67)
    frame = pd.DataFrame([row])
    prediction = float(model.predict(frame)[0])
    st.metric('Estimated rentals in this hour', f'{max(0, prediction):,.0f}')
    if prediction < 0:
        st.caption('Negative regression output is displayed as zero. Evaluation scores use original predictions.')
    scenarios = pd.DataFrame([{**row, 'hr':h} for h in range(24)])
    curve = np.maximum(0, model.predict(scenarios))
    st.subheader('Compare hours under the same conditions')
    st.line_chart(pd.DataFrame({'Hour':range(24),'Estimated rentals':curve}).set_index('Hour'))
    st.caption('Weather is held constant across all 24 scenarios. This is a scenario comparison, not a day-ahead forecast or a causal effect.')
    st.write('Use higher-demand hours to plan a capacity review. These are total system rentals, not the number of bikes needed at one station.')
st.subheader('About the model')
scores = info['test_scores']
a,b,c = st.columns(3)
a.metric('Model test MAE', f"{scores['mae']:.1f} rentals")
b.metric('Dummy test MAE', f"{scores['baseline_mae']:.1f} rentals")
c.metric('MAE improvement', f"{scores['relative_mae_reduction']:.1%}")
st.write(f"Model: {info['selected_model']}. MAE means average absolute error per observed hour; it is not an uncertainty interval for each prediction.")
st.caption(f"Chronological test period: {info['test_start']} to {info['test_end']}.")
st.subheader('Source, privacy, and limits')
st.markdown('[UCI Bike Sharing dataset](https://doi.org/10.24432/C5W894), Fanaee-T (2013), CC BY 4.0. Based on Capital Bikeshare observations from 2011–2012.')
st.write('Inputs are processed in memory for this request; the app does not save them to a file or database. Hosting infrastructure may retain ordinary connection logs. No personal information is requested.')
st.write('This historical model is not validated for current operations, Thailand, individual stations, or extreme conditions. Future weather is uncertain. Associations do not establish causes. Rare conditions may have larger errors.')
