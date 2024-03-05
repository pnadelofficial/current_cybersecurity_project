from docx import Document
import re
import pandas as pd
import plotly.express as px
import os

codes = [
    "Liberalism", 
    "Constructivism", 
    "Realism", 
    "Cyber Persistence", 
    "Policy Engineering Tasks"
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
    print(df)
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