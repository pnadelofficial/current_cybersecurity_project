import streamlit as st
import utils

st.title("Bar Charts for Codes")

utils.line_break()

st.header("Compare Case Studies")
with st.expander("Case Study Comaprison"):
    st.write("The bar charts below depict the aggregated number of text excerpts coded against each paradigmatic code for all files within the selected case studies.  This function allows the viewer to evaluate coded language for the hierarchy of strategic documents associated with a single case study or compare across multiple cases.")
csc = st.multiselect("Choose case studies", list(k.title() for k in utils.case_studies.keys()) + ['Combined'])
code_choice = st.selectbox("Choose code", ['Combined']+utils.codes, format_func=lambda x: x.title().replace('_', ' ') if x != 'Combined' else 'All codes')
code_choice = code_choice if code_choice != 'Combined' else None
with st.expander("Individual Code Comparison"):
    st.write("The bar charts below depict the number of text excerpts coded against each paradigmatic code.  This function allows the viewer to compare the use of theoretical core assumptions, causal logic, key words and phrases across individual cases or files.")
if len(csc) > 0:
    if len(csc) < 3:
        cols = st.columns(len(csc))
        for i, col in enumerate(cols):
            with col:
                if csc[i] == 'Combined':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source(code_choice=code_choice)
                if isinstance(csc[i], str):
                    if code_choice:
                        title = code_choice.title() + " in the " + csc[i] + " Case Study"
                    else:
                        title = csc[i] + " Case Study"
                else:
                    if code_choice:
                        title = code_choice.title() + " in all case studies"
                    else:
                        title = "Combined Case Studies"
                fig = cs.plot_bar_chart(results, title=title)
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=1100)
                st.plotly_chart(fig,theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(csc)
        for i, tab in enumerate(tabs):
            with tab:
                if csc[i] == 'Combined':
                    csc[i] = list(utils.case_studies.keys())
                cs = utils.CaseStudy(csc[i])
                results = cs._get_number_of_codes_by_primary_source(code_choice=code_choice)
                if isinstance(csc[i], str):
                    if code_choice:
                        title = code_choice.title() + " in the " + csc[i] + " Case Study"
                    else:
                        title = csc[i] + " Case Study"
                else:
                    if code_choice:
                        title = code_choice.title() + " in all case studies"
                    else:
                        title = "Combined Case Studies"
                fig = cs.plot_bar_chart(results, title=title)
                fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=1100)
                st.plotly_chart(fig,theme="streamlit", use_container_width=True)

st.divider() # got rid of top level codes, seemed out of place

st.header('All codes by documents')
with st.expander("Document Comparison"):
    st.write("The bar charts below depict the number of text excerpts coded against each paradigmatic code within the selected file(s). This function allows the viewer to compare coded language within a single strategic document, between strategic documents within a single case study, or among several documents across multiple cases.")
choices = st.multiselect("Choose documents to compare", list(utils.all_docs), key=1, format_func=lambda x: x.replace('_', ' ').replace('CLEAN', '').strip())
# rev_doc_mapping = {v:k for k,v in utils.doc_mapping.items()}
# choices = [rev_doc_mapping[c] for c in choices]
if len(choices) > 0:
    if len(choices) < 3:
        cols = st.columns(len(choices))
        for i, col in enumerate(cols):
            with col:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                st.plotly_chart(cs.plot_bar_chart(results, title=choices[i]),theme="streamlit", use_container_width=True)
    else:
        tabs = st.tabs(choices)
        for i, tab in enumerate(tabs):
            with tab:
                year_of_ps = utils.get_year_of_ps(choices[i])    
                cs = utils.CaseStudy(year_of_ps)
                results = cs._get_number_of_codes_by_primary_source(ps=choices[i])
                # fig.update_layout(yaxis={"dtick":1},margin={"t":100,"b":100},height=900)
                st.plotly_chart(cs.plot_bar_chart(results, title=choices[i]),theme="streamlit", use_container_width=True)