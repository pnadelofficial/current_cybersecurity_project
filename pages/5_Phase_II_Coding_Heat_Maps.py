import streamlit as st
import utils

st.set_page_config(layout="wide")
st.title("Phase II Coding Heat Maps")
with st.expander("Second Cycle / Phase II Coding "):
    st.write("""
        A Phase II coding technique was applied to national policy documents to identify instances of interaction between Policy Engineering Tasks 1 and 2 (National Interests and Objectives) and the core assumptions of various theoretical paradigms. This interaction represents the operationalization of the first step of the research methodology, which is designed to assess alignment between theory and practice in cybersecurity.

        Alignment occurs when enough core assumptions of a theory match the assumptions identified in a national policy, such that the theory has prescriptive power in judging what a policy or strategy should be and what implementation will look like. 

        The expectation of alignment is consistency and coherency within a policy document and across the policy-strategy-implementation continuum for a given case study.

        The heat maps below depict the number of interactions between Policy Engineering Tasks 1 and 2 and Core Assumptions for each theoretical paradigm. This function allows the user to compare instances of theory-policy interaction for each case. 
    """)

# Show a bar chart of the core assumptions for each theorhetical code for each case study

utils.line_break()

st.header("Compare case studies")

csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'], format_func=lambda x: x.title() if x != 'All' else 'All Case Studies')

poss_docs = {
    '2011': ['2011 International Strategy for Cyberspace', '2010 National Security Strategy'],
    '2015': ['2015 White House Report on Cyber Deterrence Policy', '2015 National Security Strategy'],
    '2018': ['2018 National Cyber Strategy', '2018 National Cyber Strategy'],
    '2023': ['2023 National Cybersecurity Strategy', '2022 National Security Strategy']
}

def plot_same_cs_on_row(csc, choice):
    cols = st.columns(2)
    for i, col in enumerate(cols):
        with col:
            cs = utils.CaseStudy(csc)
            pet_dict = utils.get_pet_dict()
            figs = cs.plot_heatmap(pet_dict, choice)
            print(len(figs))
            if len(figs) == 1:
                figs.append(None)
            if figs[i] is None:
                utils.line_break(1)
                container = st.container(border=False)
                if poss_docs[csc][0] == "2015 White House Report on Cyber Deterrence Policy":
                    text = f"<b>{poss_docs[csc][i]}</b> This national-level policy document is the outlier among the four case studies. Because it is not written as a National Cyber Strategy, it does not articulate national interests and objectives in a way that lends the document to the Phase II Coding technique. Phase I Coding, however, does reveal the concentration of theoretical concepts, key words, and phrases, as depicted in the bar charts and hierarchy maps for this policy document." # how to get correct index for csc
                else:
                    text = f"<b>{poss_docs[csc][i]}</b> for the code <b>{choice.title()}</b> does not have enough data to plot"
                container.markdown(f"<div style='text-align: center;'>{text}</div>", unsafe_allow_html=True)
            else:                    
                st.plotly_chart(figs[i], theme="streamlit", use_container_width=True)

def plot_same_doc_on_row(docs, csc, choice):
    figs = {}
    for c in csc:
        cs = utils.CaseStudy(c)
        pet_dict = utils.get_pet_dict()
        figs.update(dict(cs.plot_heatmap(pet_dict, choice, as_tups=True)))

    selected_figs = []
    for doc in docs:
        if doc in figs:
            selected_figs.append(figs[doc])
        else:
            selected_figs.append(doc)

    cols_1 = st.columns(2, gap='large')
    cols_2 = st.columns(len(docs) - 2, gap='large')
    for i, col in enumerate(cols_1):
        with col:
            if isinstance(selected_figs[i], str):
                utils.line_break(1)
                container = st.container(border=False)
                if selected_figs[i] == "2015 White House Report on Cyber Deterrence Policy":
                    text = f"<b>{selected_figs[i]}</b> This national-level policy document is the outlier among the four case studies. Because it is not written as a National Cyber Strategy, it does not articulate national interests and objectives in a way that lends the document to the Phase II Coding technique. Phase I Coding, however, does reveal the concentration of theoretical concepts, key words, and phrases, as depicted in the bar charts and hierarchy maps for this policy document." # how to get correct index for csc
                else:
                    text = f"<b>{selected_figs[i]}</b> for the code <b>{choice.title()}</b> does not have enough data to plot"
                container.markdown(f"<div style='text-align: center;'>{text}</div>", unsafe_allow_html=True)
            else:                    
                st.plotly_chart(selected_figs[i], theme="streamlit", use_container_width=True)
    for i, col in enumerate(cols_2):
        with col:
            if isinstance(selected_figs[i + 2], str):
                utils.line_break(1)
                container = st.container(border=False)
                if selected_figs[i + 2] == "2015 White House Report on Cyber Deterrence Policy":
                    text = f"<b>{selected_figs[i + 2]}</b> This national-level policy document is the outlier among the four case studies. Because it is not written as a National Cyber Strategy, it does not articulate national interests and objectives in a way that lends the document to the Phase II Coding technique. Phase I Coding, however, does reveal the concentration of theoretical concepts, key words, and phrases, as depicted in the bar charts and hierarchy maps for this policy document."
                else:
                    text = f"<b>{selected_figs[i + 2]}</b> for the code <b>{choice.title()}</b> does not have enough data to plot"
                container.markdown(f"<div style='text-align: center;'>{text}</div>", unsafe_allow_html=True)
            else:
                st.plotly_chart(selected_figs[i + 2], theme="streamlit", use_container_width=True)

if len(csc) > 0:
    if 'All' in csc:
        csc = list(utils.case_studies.keys())
    choice = st.selectbox("Choose code", utils.codes, format_func=lambda x: x.title())

    if len(csc) <= 2:
        for c in csc:
            plot_same_cs_on_row(c, choice)
    else:
        tabs = st.tabs(['National Cyber Strategy', 'National Security Strategy'])
        for i, tab in enumerate(tabs):
            with tab:
                docs = [poss_docs[k][i] for k in poss_docs.keys()]
                plot_same_doc_on_row(docs, csc, choice)
