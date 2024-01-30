import streamlit as st
import pickle
import re

st.title("Automatic Tagging Example")

with open('./data/dod_sec_zs_example.p', 'rb') as f:
    data = pickle.load(f)

color_mapping = {
    "Academic Interaction":"gold",
    "Liberalism":"darkgreen", 
    "Constructivism":"darkblue", 
    "Realism":"darkred", 
    "Cyber Persistence":"saddlebrown", 
    "Policy Engineering Tasks":"teal"
}

css = """<style>
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 5px;

  /* Position the tooltip */
  position: left;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}

</style>"""

st.markdown(css, unsafe_allow_html=True)

mark_tag = """<mark class='tooltip' style='background-color:{color}'>{line}<span class="tooltiptext">{tag}</span></mark>"""

for d in data:
    escape_line = d[0].replace('-', '\-')
    if d[1] != 'No tag':
        color = d[1].split('_')[0]
        c = re.sub(r'\{color\}', color_mapping[color], mark_tag)
        l = re.sub(r'\{line\}', escape_line, c)
        t = re.sub(r'\{tag\}', color, l)
        st.markdown(t, unsafe_allow_html=True)
    else:
        st.write(escape_line)