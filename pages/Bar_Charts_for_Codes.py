import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Bar Charts for Codes")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

utils.line_break()

st.header("Compare case studies")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'])
code_choice = st.selectbox("Choose code", ['All']+utils.codes)
code_choice = code_choice if code_choice != 'All' else None
if len(csc) > 0:
    if len(csc) < 3:
        cols = st.columns(len(csc))
        for i, col in enumerate(cols):
            with col:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source(code_choice=code_choice)
                fig = cs.plot_bar_chart(results)
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=1100)
                st.plotly_chart(fig,theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(csc)
        for i, tab in enumerate(tabs):
            with tab:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source()
                fig = cs.plot_bar_chart(results)
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=1100)
                st.plotly_chart(fig,theme="streamlit", use_container_width=True)

st.divider() # got rid of top level codes, seemed out of place

st.header('All codes by documents')
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
choices = st.multiselect("Choose documents to compare", list(utils.doc_mapping.values()), key=1)
rev_doc_mapping = {v:k for k,v in utils.doc_mapping.items()}
choices = [rev_doc_mapping[c] for c in choices]
if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=900)
                st.plotly_chart(cs.plot_bar_chart(results),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=900)
                st.plotly_chart(cs.plot_bar_chart(results),theme="streamlit", use_container_width=True)