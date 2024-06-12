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

csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'], format_func=lambda x: x.title() if x != 'All' else 'All Case Studies', help="HELP")

if len(csc) > 0:
    choice = st.selectbox("Choose code", utils.codes[:-1], format_func=lambda x: x.title())
    if len(csc) < 3:
        fig_dict = {}
        for i in range(len(csc)):
            if csc[i] == 'All':
                csc[i] = list(utils.case_studies.keys())
            cs = utils.CaseStudy(csc[i])
            pet_dict = utils.get_pet_dict()
            figs = cs.plot_heatmap(pet_dict, choice)
            fig_dict[i] = sorted(figs, key=lambda x: x.layout.title.text[5:].strip())

        fig_height = 0
        cols = st.columns(len(csc))
        if len(csc) > 1:
            if len(fig_dict[0]) < len(fig_dict[1]):
                something = csc[0] + ' ' + fig_dict[1][-1].layout.title.text[5:].strip()
                fig_dict[0].append(f"{something}")
            if len(fig_dict[1]) < len(fig_dict[0]):
                something = csc[1] + ' ' + fig_dict[0][-1].layout.title.text[5:].strip()
                fig_dict[1].append(f"{something}")
            for i, col in enumerate(cols):
                with col:
                    for fig in fig_dict[i]:    
                        if type(fig) == str:
                            utils.line_break(1)
                            container = st.container(height=fig_height, border=False)
                            text = f"<b>{fig}</b> is missing"
                            container.markdown(f"<div style='text-align: center;'>{text}</div>", unsafe_allow_html=True) # 
                        else:
                            fig_height += fig.layout.height
                            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
        else:
            for i, col in enumerate(cols):
                with col:
                    for fig in fig_dict[i]:    
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
