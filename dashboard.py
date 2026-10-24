import pandas as pd
import streamlit as st

st.title('Highwall Monitoring — InSAR')
st.caption('North component assumed negligible: the satellite is '
           'nearly blind to north-south movement.')

data = pd.read_csv('results.csv')

def status(row):
    if row['significant'] == 'no':
        return 'GREEN'
    speed = row['v_total_mm_yr']
    if speed > 120:
        return 'RED'
    if speed > 30:
        return 'AMBER'
    return 'GREEN'

data['status'] = data.apply(status, axis=1)

if (data['status'] == 'RED').any():
    st.error('ALARM — rapid ground movement detected. Warn the site.')
elif (data['status'] == 'AMBER').any():
    st.warning('Caution — movement above the watch level.')
else:
    st.success('All scatterers stable.')

st.subheader('Scatterers, fastest first')
st.dataframe(data.sort_values('v_total_mm_yr', ascending=False))

st.subheader('Movement direction')
st.scatter_chart(data, x='v_east_mm_yr', y='v_up_mm_yr')
st.caption('Points should lie on a line whose slope is -tan(35 deg), '
           'because the block slides down the failure plane.')