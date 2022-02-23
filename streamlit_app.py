import streamlit as st
import pandas as pd
import altair as alt

st.title("How many couples sleep in separate beds?👩‍❤️‍👨 👩‍❤️‍👩 👨‍❤️‍👨")

#@st.cache  # add caching so we load the data only once
def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_raw = 'https://raw.githubusercontent.com/fivethirtyeight/data/22a478af3edc00f69693c3f5f4604b2f1fd024b0/sleeping-alone-data/sleeping-alone-data.csv'
url_separate = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/sleep_separately.csv'
url_together = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/sleep_together.csv'
url_demo = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/demographic_data.csv'

# READ DATA
raw = load_data(url_raw, encode ='ISO-8859-1')
demo_df = load_data(url_demo)
separate_df = load_data(url_separate)
together_df = load_data(url_together)

with st.expander("See raw data"):
    st.text('Here are the raw data')
    st.write(raw)

with st.expander("See cleaned data"):
    st.write("Here are the cleaned data")
    st.text("Demographic data:")
    st.write(demo_df)
    st.text("Data of couples who sleep separately:")
    st.write(separate_df)
    st.text("Data of couples who sleep together:")
    st.write(together_df)



# Distribution of sleep together vs separately
st.title("Let's see how many couples sleep together")
demo_df['Together?'] = demo_df['sleep together?'].map({0: 'NO', 1:'YES'})

sleep_together = alt.Chart(demo_df).mark_bar(tooltip = True).encode(
    alt.X('Together?:N', sort='-y', axis=alt.Axis(title='Do couples sleep together?')),
    alt.Y('count()')
).interactive(
).properties(width=600)
st.write(sleep_together)

# brushes
status_brush = alt.selection_multi(fields=['CurrentRelationshipStatus'])
length_brush = alt.selection_multi(fields=['RelationshipLength'])
freq_brush = alt.selection_multi(fields=['Frequency in separate beds'])
age_brush = alt.selection_multi(fields=['Age'])
gender_brush = alt.selection_multi(fields=['Gender'])
income_brush = alt.selection_multi(fields=['Household income'])
education_brush = alt.selection_multi(fields=['Education'])
location_brush = alt.selection_multi(fields=['Location'])

# Relationship status
st.title('How the relationships status look like')
status_chart = alt.Chart(demo_df, title='Relationship Status').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('CurrentRelationshipStatus', sort = '-x'), 
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)
st.write(status_chart)

length_chart = alt.Chart(demo_df, title='Relationship Length').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('RelationshipLength', sort = '-x'),
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)
st.write(length_chart)

freq_chart = alt.Chart(demo_df, title='Frequency in separate beds').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Frequency in separate beds', sort = ['Never', 'Once a year or less', 'Once a month or less', 'A few times per month', 'A few times per week', 'Every night']),
    color=alt.Color('Together?',
        scale=alt.Scale(
        domain=['YES', 'NO'],
        range=['pink', 'steelblue']))
).properties(
    width = 600
)
st.write(freq_chart)


# Demographic data
age_chart = alt.Chart(demo_df, title='Age').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Age', sort = ['18-29', '30-44', '45-60', '> 60', 'Did not disclose']),
    color=alt.Color('Together?',
        scale=alt.Scale(
        domain=['YES', 'NO'],
        range=['pink', 'steelblue']))
).properties(
    width = 600
)

gender_chart = alt.Chart(demo_df, title='Gender').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Gender', sort = '-x'),
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)

income_chart = alt.Chart(demo_df, title='Household Income').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Household income', sort = ['$150,000+', '$100,000 - $149,999', '$50,000 - $99,999', '$25,000 - $49,999', '$0 - $24,999', 'Did not disclose']),
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)
education_chart = alt.Chart(demo_df, title='Education Level').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Education', sort = ['Graduate degree', 'Bachelor degree', 'Some college or Associate degree', 'High school degree', 'Less than high school degree', 'Did not disclose']),
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)

location_chart = alt.Chart(demo_df, title='Location').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Location', sort = '-x'),
    color=alt.Color('Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'steelblue']))
).properties(
    width = 600
)

# Drop down list for user to select demographic features
options = st.multiselect(
     'What demographic feature distribution do you want to see?',
     ['Age', 'Gender', 'Household Income', 'Education', 'Location'])
if 'Age' in options:
    st.write(age_chart)
if 'Gender' in options:
    st.write(gender_chart)
if 'Education' in options:
    st.write(education_chart)
if 'Location' in options:
    st.write(location_chart)
if 'Household Income' in options:
    st.write(income_chart)
if 'Location' in options:
    st.write(location_chart)










st.markdown("This project was created by Li-Hsin Lin and Kylie Hsieh for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
