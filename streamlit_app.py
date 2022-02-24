from os import sep
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.title("Do Couples Always Sleep Together? 👩‍❤️‍👨 👩‍❤️‍👩 👨‍❤️‍👨")

image = Image.open('Figs/sleeping_together_or_not.png')
st.image(image, caption='Photo by Somnox Sleep on Unsplash')

st.subheader("Data")
st.markdown("Source: [Sleeping alone data](https://github.com/fivethirtyeight/data/tree/master/sleeping-alone-data) by FiveThirtyEight")
#@st.cache  # add caching so we load the data only once

# ===================================== PART 0 =====================================
# Read data

def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_raw = 'https://raw.githubusercontent.com/fivethirtyeight/data/22a478af3edc00f69693c3f5f4604b2f1fd024b0/sleeping-alone-data/sleeping-alone-data.csv'
url_separate = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Data/sleep_separately.csv'
url_together = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Data/sleep_together.csv'
url_demo = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Data/demographic_data.csv'

raw = load_data(url_raw, encode ='ISO-8859-1')
demo_df = load_data(url_demo)
separate_df = load_data(url_separate)
together_df = load_data(url_together)

with st.expander("See raw data"):
    st.write('Here is the raw data.')
    st.write(raw)

with st.expander("See cleaned data"):
    st.write("Here is the cleaned data.")
    st.text("Demographic data:")
    st.write(demo_df)
    st.text("Data of couples who sleep together:")
    st.write(together_df)
    st.text("Data of couples who sleep separately:")
    st.write(separate_df)


# MAIN CODE


# ===================================== PART 1 =====================================
# Basic information
# Sleep together or not?
st.header("Part 1: Sleep Together or Not?")
st.write("We have 1079 valid responses. Let's look at how many couples actually sleep together every day.")

demo_df['Sleep Together?'] = demo_df['Sleep Together?'].map({0: 'NO', 1:'YES'})
sleep_together = alt.Chart(demo_df, title='Do you and your partner sleep together every day?').mark_bar(tooltip = True, size = 30).encode(
    alt.X('count()'),
    alt.Y('Sleep Together?:N', sort='-x', axis=alt.Axis(title='')),
    alt.Color('Sleep Together?', scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']), legend=None)
).interactive(
).properties(width=600, height=200)
st.write(sleep_together)

st.write("Surprise! Among the 1079 respondent, there are 493 of them who do not always sleep with their partner.")
st.write("Now, you may wonder, among those who don't always sleep with their partner, are they married?\
         How long have they been in the relationship with their partner?")

# Sleep together or not?
group = st.radio("👇 Select one of the demographics you want to look at",
     ('Relationship Length', 'Relationship Status',))

# Relationship status
status_chart = alt.Chart(demo_df, title='Relationship Status').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('CurrentRelationshipStatus', sort = '-x', axis=alt.Axis(title='')), 
    color=alt.Color('Sleep Together?', legend = None,
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue'])),
    row = 'Sleep Together?'
).properties(width = 600)
    
# Timespan of current relationship
categories_in_order = ["More than 20 years", "16-20 years", "11-15 years", "6-10 years", "1-5 years", "Less than 1 year"]
length_chart = alt.Chart(demo_df, title='Relationship Length').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('RelationshipLength', sort = categories_in_order, axis=alt.Axis(title='')),
    color = alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']),
            legend = None),
    row = 'Sleep Together?'
).properties(width = 600)

if group == 'Relationship Length':
     st.write(length_chart)
else:
     st.write(status_chart)

# freq_chart = alt.Chart(demo_df, title='Frequency in separate beds').mark_bar(tooltip = True).encode(
#     x = alt.X('count()'),
#     y = alt.Y('Frequency in separate beds', sort = ['Never', 'Once a year or less', 'Once a month or less', 'A few times per month', 'A few times per week', 'Every night']),
#     color=alt.Color('Sleep Together?',
#         scale=alt.Scale(
#         domain=['YES', 'NO'],
#         range=['pink', 'lightblue']))
# ).properties(
#     width = 600
# )
# st.write(freq_chart)


# ===================================== PART 2 =====================================
# Correlations between frequency of sleeping separately and demographics

st.header("Part 2: Demographics Correlations")
st.write("""The survey collected demographic data of the respondents, including age, gender, household income, and education level.
         Demographic data is useful for researcher to understand human behavior, and it can be used in many ways to learn the generalities of a particular population.""")
st.write("The demographic distributions can help us better understand the correlation between **demographics** and **whether the couple sleep together**.")

# Demographic data
age_chart = alt.Chart(demo_df, title="Distribution of age vs sleep together or not").mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Age', sort = ['> 60', '45-60', '30-44', '18-29', 'Did not disclose']),
    color = alt.Color('Sleep Together?', 
                scale = alt.Scale(domain=['YES', 'NO'], 
                range=['pink', 'lightblue']), 
                legend=None),
    row = 'Sleep Together?'
).properties(
    width = 600
)

gender_chart = alt.Chart(demo_df, title="Distribution of gender vs sleep together or not").mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Gender', sort = '-x'),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']),
            legend = None),
    row = 'Sleep Together?'
).properties(
    width = 600
)

income_chart = alt.Chart(demo_df, title="Distribution of household income vs sleep together or not").mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Household income', sort = ['$150,000+', '$100,000 - $149,999', '$50,000 - $99,999', '$25,000 - $49,999', '$0 - $24,999', 'Did not disclose']),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']),
            legend = None),
        row = 'Sleep Together?'
).properties(
    width = 600
)
    
education_chart = alt.Chart(demo_df, title="Distribution of education level vs sleep together or not").mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Education', sort = ['Graduate degree', 'Bachelor degree', 'Some college or Associate degree', 'High school degree', 'Less than high school degree', 'Did not disclose']),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']),
            legend = None),
    row = 'Sleep Together?'
).properties(
    width = 500
)

# location_chart = alt.Chart(demo_df).mark_bar(tooltip = True).encode(
#     x = alt.X('count()'),
#     y = alt.Y('Location', sort = '-x'),
#     color=alt.Color('Sleep Together?',
#             scale=alt.Scale(
#             domain=['YES', 'NO'],
#             range=['pink', 'lightblue']))
# ).properties(
#     width = 600
# )

# Drop down list for user to select demographic features
demo_options = st.multiselect(
     '👇 Select one or more demographic factors you are interested in',
     ['Age', 'Gender', 'Household Income', 'Education'])
if 'Age' in demo_options:
    st.write(age_chart)
    st.markdown("---")
if 'Gender' in demo_options:
    st.write(gender_chart)
    st.markdown("---")
if 'Education' in demo_options:
    st.write(education_chart)
    st.markdown("---")
if 'Household Income' in demo_options:
    st.write(income_chart)
    st.markdown("---")
#if 'Location' in demo_options:
#    st.write(location_chart)
    
# ===================================== PART 3 =====================================
# Drop down demographics and timespan of relationship selection + reasons (bar chart)
# Select the reasons for sleeping in separate beds and show the correspondent demographics data

st.header("Part 3: Why Couples Do Not Sleep Together?")

# ===================================== PART 4 =====================================
# Drop down reason selection + questions opinions (box plots)
# Select the reasons for sleeping in separate beds and show the correspondent opinion

st.header("Part 4: Is Sleeping Separately Better?")
st.write("""In addition to investigating the reasons for sleeping separately,
         the survey also asked those who don't sleep with their partner for their opinions of the following three questions.""")
st.markdown("- Sleeping in separate beds helps us to stay together")
st.markdown("- We sleep better when we sleep in separate beds")
st.markdown("- Our sex life has improved as a result of sleeping in separate beds")

separate_reasons =['Reason_One of us snores',
                'Reason_One of us makes frequent bathroom trips in the night',
                'Reason_One of us is sick','Reason_We are no longer physically intimate',
                'Reason_We have different temperature preferences for the room',
                'Reason_We have had an argument or fight','Reason_Not enough space',
                'Reason_Do not want to share the covers','Reason_One of us needs to sleep with a child',
                'Reason_Night working/very different sleeping times','Reason_Other']

questions = ['Sleeping in separate beds helps us to stay together', 'We sleep better when we sleep in separate beds',
             'Our sex life has improved as a result of sleeping in separate beds' ]

reason_option = st.selectbox(
    "👇 Select the reason you want to see",
    ['One of us snores','One of us makes frequent bathroom trips in the night',
    'One of us is sick','We are no longer physically intimate',
    'We have different temperature preferences for the room',
    'We have had an argument or fight','Not enough space',
    'Do not want to share the covers','One of us needs to sleep with a child',
    'Night working/very different sleeping times'])

question_option = st.selectbox(
    "👇 Select the question you want to see",
    ['Sleeping in separate beds helps us to stay together', 'We sleep better when we sleep in separate beds',
    'Our sex life has improved as a result of sleeping in separate beds' ]
)

st.write("---")
st.subheader('If ' + reason_option.lower() +', does ' + question_option.lower() + ' ?')

yes_proportion = separate_df['Reason_'+reason_option].mean()
no_proportion = 1 - yes_proportion
no_score = separate_df[question_option+'_code'][separate_df['Reason_'+reason_option] == 0].mean()
yes_score = separate_df[question_option+'_code'][separate_df['Reason_'+reason_option] == 1].mean()

col1, col2 = st.columns(2)
with col1:
    st.metric(reason_option+' is not the reason', '{:.2%}'.format(no_proportion))
    st.metric('Mean score for question:' + question_option.lower() + '(5 is strongly agree)', 
                round(no_score, 3))
    chart = alt.Chart(separate_df[separate_df['Reason_'+reason_option] == 0], title='Not the reason').mark_bar(tooltip=True).encode(
        alt.X('count()'),
        alt.Y(question_option, title = None,
            sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree']),
        color = alt.value('#A2D9CE')
    )
    st.altair_chart(chart, use_container_width=True)
    
with col2:
    st.metric(reason_option+' is the reason', '{:.2%}'.format(yes_proportion))
    st.metric('Mean score for question:' + question_option.lower() + '(5 is strongly agree)', 
                round(yes_score, 3))
    chart = alt.Chart(separate_df[separate_df['Reason_'+reason_option] == 1], title='Is the reason').mark_bar(tooltip=True).encode(
        alt.X('count()'),
        alt.Y(question_option, title = None,
            sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree']),
        color = alt.value('#FAD7A0')
    )
    st.altair_chart(chart, use_container_width=True)

st.markdown("---")
st.markdown("This project was created by Erin Lin and Kylie Hsieh for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")



# Brushes
sleep_together_brush = alt.selection_multi(fields=['sleep together?'])
status_brush = alt.selection_multi(fields=['CurrentRelationshipStatus'])
length_brush = alt.selection_multi(fields=['RelationshipLength'])
freq_brush = alt.selection_multi(fields=['Frequency in separate beds'])
age_brush = alt.selection_multi(fields=['Age'])
gender_brush = alt.selection_multi(fields=['Gender'])
income_brush = alt.selection_multi(fields=['Household income'])
education_brush = alt.selection_multi(fields=['Education'])
location_brush = alt.selection_multi(fields=['Location'])
