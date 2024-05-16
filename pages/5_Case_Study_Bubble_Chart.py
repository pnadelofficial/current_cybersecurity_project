import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Bubble Chart")
with st.expander("Bubble Chart for Cases"):
    st.write("The bubble chart illustrates how the use of theoretical language compares in strategic documents within and across case studies over time, with the size of the bubbles corresponding to the prevalence of language associated with a particular theoretical paradigm.  This function allows the user to examine how strategic thought nested (or didn't) down the policy/strategy hierarchy for each administration, and how it evolved over time from one administration to the next.")

bubble_df = pd.read_csv('./data/bubble_data0516.csv')
fig = px.scatter(bubble_df, x='year', y='doc_class', size='count', color='code', hover_name='doc')
fig.update_layout(
    xaxis=dict(
        # autorange=False,
        tickvals=[2011, 2015],
        ticktext=['2011', '2015'],
        tick0=0,
        dtick=1
    )
)
st.plotly_chart(fig, use_container_width=True)