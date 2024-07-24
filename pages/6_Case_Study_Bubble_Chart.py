import streamlit as st
import pandas as pd
import plotly.express as px
import random
import numpy as np
import utils
np.random.seed(0)
random.seed(42)

st.title("Bubble Chart")
with st.expander("Bubble Chart for Cases"):
    st.write("The bubble chart illustrates how the use of theoretical language compares in strategic documents within and across case studies over time, with the size of the bubbles corresponding to the prevalence of language associated with a particular theoretical paradigm.  This function allows the user to examine how strategic thought nested (or didn't) down the policy/strategy hierarchy for each administration, and how it evolved over time from one administration to the next.")

@st.cache_data
def load_data_with_jitters():
    bubble_df = pd.read_csv('./data/bubble_data0717.csv')
    df_with_dates = pd.read_csv('./data/docs_with_dates.csv')
    bubble_df['year'] = pd.to_datetime(bubble_df.year)
    df_with_dates['date'] = pd.to_datetime(df_with_dates['date'])
    bubble_df['category_numeric'] = bubble_df['doc_class'].astype('category').cat.codes
    bubble_df['category_jittered'] = bubble_df['category_numeric'] + np.random.uniform(-0.2, 0.2, size=len(bubble_df))

    merged = pd.merge(bubble_df, df_with_dates, on='doc')
    return merged
bubble_df = load_data_with_jitters()

csc = st.multiselect("Choose case studies", ['2011', '2015', '2018', '2023'], default=['2011', '2015', '2018', '2023'])

if csc:
    fig = px.scatter(bubble_df[bubble_df.year.isin(csc)], x='date', y='category_jittered', size='count', color='code', color_discrete_map=utils.color_mapping_lower, hover_data=['code', 'count'], hover_name='doc')
    fig.update_layout(
        xaxis=dict(
            # autorange=False,
            tickvals=[int(c) for c in csc],
            ticktext=[c for c in csc],
            tick0=0,
            dtick=1
        )
    )
    fig.update_yaxes(tickvals=[0, 1, 2, 3, 4], ticktext=['NSS', 'NCS', 'QDR_NDS', 'NMS', 'DoD'])
    fig.update_layout(yaxis_title='Document Class')
    fig.update_layout(xaxis_title='Date')
    st.plotly_chart(fig, use_container_width=True) 