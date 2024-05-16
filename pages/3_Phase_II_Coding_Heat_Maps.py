import streamlit as st
import utils
import plotly.express as px

st.title("Phase II Coding Heat Maps")
with st.expander("Second Cycle / Phase II Coding "):
    st.write("""
        A Phase II coding technique was applied to national policy documents to identify instances of interaction between Policy Engineering Tasks 1 and 2 (National Interests and Objectives) and the core assumptions of various theoretical paradigms. This interaction represents the operationalization of the first step of the research methodology, which is designed to assess alignment between theory and practice in cybersecurity.

        Alignment occurs when enough core assumptions of a theory match the assumptions identified in a national policy, such that the theory has prescriptive power in judging what a policy or strategy should be and what implementation will look like. 

        The expectation of alignment is consistency and coherency within a policy document and across the policy-strategy-implementation continuum for a given case study.

        The heat maps below depict the number of interactions between Policy Engineering Tasks 1 and 2 and Core Assumptions for each theoretical paradigm. This function allows the user to compare instances of theory-policy interaction for each case. 
    """)

utils.line_break()

st.header("Compare case studies")

csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'])

if len(csc) > 0:
    choice = st.selectbox("Choose code", utils.codes[:-1])
    if len(csc) < 3:
        cols = st.columns(len(csc))
        for i, col in enumerate(cols):
            with col:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                pet_dict = utils.get_pet_dict()
                figs = cs.plot_heatmap(pet_dict, choice)
                for fig in figs:    
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(csc)
        for i, tab in enumerate(tabs):
            with tab:
                if csc[i] == 'All':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                pet_dict = utils.get_pet_dict()
                figs = cs.plot_heatmap(pet_dict, choice)
                for fig in figs:    
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
