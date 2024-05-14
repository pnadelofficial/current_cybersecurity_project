import streamlit as st
import utils
import plotly.express as px

st.title("Double Codes Heat Maps")
with st.expander("Lorem ipsum"):
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

utils.line_break()

st.header("Compare case studies")

# csc = ['All'] # 
csc = st.multiselect("Choose case studies", list(utils.case_studies.keys()) + ['All'])

# with st.expander("Liberalism "):
#     st.markdown("""
# * States are primary (rational) actors, but they share power with non-state actors.
# * International cooperation is desirable and possible. Economic and Internet
# governance cooperation can drive politico-military cooperation.
# * Security comes from leveraging institutions to foster cooperative relationships
# built on mutual trust. (Causal mechanism: institutions)
# * Complex interdependence renders national economies more sensitive and
# vulnerable to events in other countries. The global nature of the Internet
# intensifies interdependence and demands cooperation.
# * Norm conformance is driven by material self-interest. Actors construct and
# conform to norms because norms help them get what they want.
# * NLI is rooted in a normative, optimistic ideology that produced moralistic,
# prescriptive theories of political behavior based on how the world ought to be
# (Carr 1939, 6).
#     """.strip())

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
