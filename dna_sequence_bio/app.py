import streamlit as st
import pandas as pd
from PIL import Image
import altair as alt
# Title
image = Image.open('download.png')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App


This app counts the nucleotide composition of query DNA!
***
""")

# TextBox

st.header(body="ENTER DNA SEQUENCE")

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequnce input", sequence_input, height=250)

sequence = sequence.splitlines()
# skip the name
sequence = sequence[1:]

sequence = ''.join(sequence)

st.write("""
***
 """)


st.header("INPUT (DNA QUERY)")
sequence


st.header('Result (DNA Nucleotide Count)')

st.subheader('1.  Print Dictionary')


def dna_nucleotide_count(sequence):
    return dict([
        ('A', sequence.count('A')),
        ('C', sequence.count('C')),
        ('T', sequence.count('T')),
        ('G', sequence.count('G')),
    ])


count = dna_nucleotide_count(sequence)

# X_label = list(count)
# X_values = list(count.values())

count

st.subheader('2. Print text')
st.write(f"There are {str(count['A'])} adenine (A) ")
st.write(f"There are {str(count['C'])} cytosine (C) ")
st.write(f"There are {str(count['T'])} thymine (T)")
st.write(f"There are {str(count['G'])} guanine (G) ")


st.subheader('3 . Display Dataframe')

df = pd.DataFrame.from_dict(count, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

st.subheader('4 .  Display Bar Chart')

plot = alt.Chart(df).mark_bar().encode(
    x='nucleotide', y='count'
)

# bar was too thin
plot = plot.properties(width=alt.Step(80))

st.write(plot)
