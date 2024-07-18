import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Hierarchy Maps for Codes")

utils.line_break()

st.header("Compare case studies")
with st.expander("Case Study Comparison"):
    st.write("""
        The color-coded tree maps below depict the parent-child code hierarchy for Concept and In Vivo Codes for each theoretical paradigm.  Users can click on the nested rectangles to expand the code and examine the parent-child relationship. The size of the rectangular data frames corresponds to the amount of text tagged with that paradigmatic code.

        The case study comparison function allows the viewer to evaluate coded language for the hierarchy of strategic documents associated with a single case study or compare across multiple cases.
    """)
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
                if isinstance(csc[i], str):
                    title = csc[i] + " Case Study" 
                else: 
                    title = "All case studies"
                st.plotly_chart(cs.plot_treemap(results, ps=title),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(csc)
        for i, tab in enumerate(tabs):
            with tab:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source()
                if isinstance(csc[i], str):
                    title = csc[i] + " Case Study" 
                else: 
                    title = "All case studies"
                st.plotly_chart(cs.plot_treemap(results, ps=title),theme="streamlit", use_container_width=True)

st.divider()

st.header("Compare Documents")
with st.expander("Document Comparison"):
    st.write("The primary source document comparison function allows the viewer to compare coded language within a single strategic document, between strategic documents within a single case study, or among several documents across multiple cases.")

choices = st.multiselect("Choose documents to compare", list(utils.all_docs))
if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                st.plotly_chart(cs.plot_treemap(results, ps=choices[i]),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                st.plotly_chart(cs.plot_treemap(results, ps=choices[i]),theme="streamlit", use_container_width=True)
