from docx import Document
import re
import pandas as pd
import plotly.express as px
import os
import streamlit as st
import collections

codes = [
    "liberalism", 
    "constructivism", 
    "realism", 
    "cyberpersistence", 
    "policy_engineering_tasks"
]

color_mapping = {
    "Academic Interaction":"gold",
    "Liberalism":"darkgreen", 
    "Constructivism":"darkblue", 
    "Realism":"darkred", 
    "Cyber Persistence":"saddlebrown", 
    "Policy Engineering Tasks":"teal"
}

def get_number_of_codes_by_doc_and_primary_source(doc_path, primary_source):
    ancestor = doc_path.split('/')[-3]
    parent = doc_path.split('/')[-2]
    child = doc_path.split('/')[-1].replace('.docx', '')
    doc = Document(doc_path)
    doc_text = '\n'.join([p.text for p in doc.paragraphs])
    doc_refs = re.findall(r'Files\\\\2011 Case Study\\\\Primary Sources_Policy_Strategies\\\\.*',doc_text)
    for dr in doc_refs:
        if primary_source in dr:
            matches = re.findall(r'§ (\d+) references coded', dr)
            if len(matches) > 0:
                return (ancestor, parent, child, int(matches[0]))
            
def plot_treemap_from_ps(ps):
    results = []
    for code in codes:
        for root, dirs, files in os.walk(f'./data/code_docs/{code}/'):
            for file in files:
                if file.endswith('.docx'):
                    tag_tup = get_number_of_codes_by_doc_and_primary_source(os.path.join(root, file), ps)
                    if tag_tup:
                        results.append(tag_tup)

    df = pd.DataFrame(results, columns=['ancestor', 'parent', 'child', 'refs'])
    fig = px.treemap(df[~(df.child.isnull())] , path=[px.Constant(ps), 'ancestor', 'parent', 'child'], values='refs')
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(
        treemapcolorway = [color_mapping[cm] for cm in color_mapping if cm in sorted(list(df.ancestor.unique()))],
        margin = dict(t=50, l=50, r=50, b=50)
    ) 
    return fig

def make_df_from_ps(ps):
    results = []
    for code in codes:
        for root, dirs, files in os.walk(f'./data/code_docs/{code}/'):
            for file in files:
                if file.endswith('.docx'):
                    tag_tup = get_number_of_codes_by_doc_and_primary_source(os.path.join(root, file), ps)
                    if tag_tup:
                        results.append(tag_tup)

    df = pd.DataFrame(results, columns=['ancestor', 'parent', 'child', 'refs']) 
    return df

def read_doc_collect_codes(path):
    code = path.split('/')[-1].replace('.docx', '') 
    doc = Document(path)
    doc_text = '\n'.join([p.text for p in doc.paragraphs])
    doc_names = re.findall(r'Files\\\\2011 Case Study\\\\Primary Sources_Policy_Strategies\\\\(.*) - .*', doc_text)
    doc_refs = re.split(r'Files\\\\2011 Case Study\\\\Primary Sources_Policy_Strategies\\\\.*',doc_text)[1:]
    docs = list(zip(doc_names, doc_refs))

    doc_dict = {} 
    for name, dr in docs:
        refs = re.findall(r'Reference \d+ - .* Coverage\n(.*)', dr.strip())
        doc_dict[name] = [(code, r) for r in refs]

    return doc_dict

@st.cache_data
def get_pet_dict():
    pet_dict = collections.defaultdict(list)
    for file in os.listdir('./data/code_docs/policy_engineering_task'):
        if file == 'implementation':
            continue
        path = f'./data/code_docs/policy_engineering_task/{file}'
        _dict = read_doc_collect_codes(path)
        for k, v in _dict.items():
            pet_dict[k] += v
    return pet_dict

def get_ca_dict(path):
    ca_dict = collections.defaultdict(list)
    for file in os.listdir(path):
        doc_path = f'{path}/{file}'
        _dict = read_doc_collect_codes(doc_path)
        for k, v in _dict.items():
            ca_dict[k] += v
    return ca_dict

def get_heatmap_data(code, doc, pet_dict, ca_dict):
    test_pet = pet_dict[doc]
    test_lib = ca_dict[doc]

    hm_data = []
    for t in test_pet:
        for s in test_lib:
            if t[1] == s[1]:
                hm_data.append((t[0], s[0])) # t[1]

    hmdf = pd.DataFrame(hm_data, columns=['policy engineering task', f'{code} core assumptions'])
    pair_counts = hmdf.groupby([f'{code} core assumptions', 'policy engineering task']).size().reset_index(name='Count')
    heatmap_data = pair_counts.pivot(index=f'{code} core assumptions', columns='policy engineering task', values='Count').fillna(0)
    return heatmap_data