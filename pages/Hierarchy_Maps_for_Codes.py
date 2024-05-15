import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Hierarchy Maps for Codes")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

utils.line_break()

st.header("Compare case studies")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'])
if len(csc) > 0:
    if len(csc) < 3:
        cols = st.columns(len(csc))
        for i, col in enumerate(cols):
            with col:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source()
                st.plotly_chart(cs.plot_treemap(results, ps=f'{csc[i]} Case Study'),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(csc)
        for i, tab in enumerate(tabs):
            with tab:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source()
                st.plotly_chart(cs.plot_treemap(results, ps=f'{csc[i]} Case Study'),theme="streamlit", use_container_width=True)

st.divider()

st.header("Compare primary sources")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
rev_doc_mapping = {v:k for k,v in utils.doc_mapping.items()}
choices = st.multiselect("Choose documents to compare", list(utils.doc_mapping.values()))
choices_rev = [rev_doc_mapping[c] for c in choices]
if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                year_of_ps = utils.get_year_of_ps(choices_rev[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices_rev[i])
                st.plotly_chart(cs.plot_treemap(results, ps=choices_rev[i]),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                year_of_ps = utils.get_year_of_ps(choices_rev[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices_rev[i])
                st.plotly_chart(cs.plot_treemap(results, ps=choices_rev[i]),theme="streamlit", use_container_width=True)
