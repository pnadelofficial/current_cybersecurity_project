import streamlit as st
import pandas as pd
import plotly.express as px
import utils

st.title("Bar Charts for Codes")
with st.expander("Code Book Development"):
    st.write("""
        This study examines the theory-practice gap through four different paradigms situated at two different layers of International Relations (IR) theoretical hierarchy.  Neoliberal Institutionalism (NLI) and International Norms theory—the latter rooted in Constructivism—are comprehensive explanations of international relations that can influence how policy is developed broadly.  Deterrence Theory and Cyber Persistence Theory (CPT)—both rooted in Realism—are more narrow aspects of international relations focused on security. However, all four paradigms make causal assumptions about how security is achieved. NLI assumes security comes from leveraging institutions to foster cooperative relationships built on mutual trust. Normative theories assume security comes from like-minded states defaulting to generally accepted norms of behavior. Deterrence Theory assumes security is derived from a prospective threat or cost imposition. The theory of Cyber Persistence assumes security is derived from maintaining operational persistence below the threshold of armed conflict. 

        These paradigms served as categories that were disaggregated to apply a hybrid text coding methodology using deductive and inductive techniques. An a priori—or theoretically derived—coding technique was employed based on a review of relevant IR theoretical literature, applying Concept Coding for core assumptions underpinning the causal logic of each theory, and Provisional Coding for key words and phrases commonly associated with each theory. This deductive process resulted in a preliminary list of researcher-generated codes based on what preparatory investigation suggested might appear in the data before they were collected and analyzed (Saldana 2021, 368).  While analyzing the text of the primary source documents line-by-line, I inductively applied In Vivo Coding to capture additional expressions, constructs, and word choices that implicated theoretical paradigms to iteratively refine the codebook. 
    """)

utils.line_break()

st.header("Compare Case Studies")
with st.expander("Case Study Comaprison"):
    st.write("The bar charts below depict the aggregated number of text excerpts coded against each paradigmatic code for all files within the selected case studies.  This function allows the viewer to evaluate coded language for the hierarchy of strategic documents associated with a single case study or compare across multiple cases.")
csc = st.multiselect("Choose case studies", list(k.title() for k in utils.case_studies.keys()) + ['All'])
code_choice = st.selectbox("Choose code", ['All']+utils.codes, format_func=lambda x: x.title().replace('_', ' ') if x != 'All' else 'All codes')
code_choice = code_choice if code_choice != 'All' else None
with st.expander("Individual Code Comparison"):
    st.write("The bar charts below depict the number of text excerpts coded against each paradigmatic code.  This function allows the viewer to compare the use of theoretical core assumptions, causal logic, key words and phrases across individual cases or files.")
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
with st.expander("Document Comparison"):
    st.write("The bar charts below depict the number of text excerpts coded against each paradigmatic code within the selected file(s). This function allows the viewer to compare coded language within a single strategic document, between strategic documents within a single case study, or among several documents across multiple cases.")
choices = st.multiselect("Choose documents to compare", list(utils.doc_mapping.values()), key=1, format_func=lambda x: x.replace('_', ' ').replace('CLEAN', '').strip())
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