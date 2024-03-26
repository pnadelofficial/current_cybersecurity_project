import streamlit as st
import utils
import plotly.express as px

# will give me a name

choice = st.selectbox("Choose code", utils.codes[:-1])

with st.expander("Liberalism "):
    st.markdown("""
* States are primary (rational) actors, but they share power with non-state actors.
* International cooperation is desirable and possible. Economic and Internet
governance cooperation can drive politico-military cooperation.
* Security comes from leveraging institutions to foster cooperative relationships
built on mutual trust. (Causal mechanism: institutions)
* Complex interdependence renders national economies more sensitive and
vulnerable to events in other countries. The global nature of the Internet
intensifies interdependence and demands cooperation.
* Norm conformance is driven by material self-interest. Actors construct and
conform to norms because norms help them get what they want.
* NLI is rooted in a normative, optimistic ideology that produced moralistic,
prescriptive theories of political behavior based on how the world ought to be
(Carr 1939, 6).
    """.strip())

pet_dict = utils.get_pet_dict()
_ca_dict = utils.get_ca_dict(f'./data/code_docs/{choice}/core_assumptions')
color_scale = utils.double_codes_color_mapping[choice]
docs = list(pet_dict.keys())

for doc in docs:
    hm_data = utils.get_heatmap_data(choice, doc, pet_dict, _ca_dict)
    if len(hm_data) == 0:
        continue
    fig = px.imshow(hm_data, title=doc, text_auto=True, color_continuous_scale=color_scale)
    st.write(fig)