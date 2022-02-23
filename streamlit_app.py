import streamlit as st
import pandas as pd
import altair as alt

st.title("How many couples sleep in separate beds?👩‍❤️‍👨 👩‍❤️‍👩 👨‍❤️‍👨")
st.markdown("Data source: FiveThirtyEight [Sleeping alone data](https://github.com/fivethirtyeight/data/tree/master/sleeping-alone-data)")
#@st.cache  # add caching so we load the data only once
def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_raw = 'https://raw.githubusercontent.com/fivethirtyeight/data/22a478af3edc00f69693c3f5f4604b2f1fd024b0/sleeping-alone-data/sleeping-alone-data.csv'
url_separate = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Sleep_separately.csv'
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


#===================================== PART 1 =================================================
# Basic information
# Sleep together or not?
st.title("Let's see how many couples sleep together")
demo_df['Sleep Together?'] = demo_df['sleep together?'].map({0: 'NO', 1:'YES'})

st.text("After removing all null values, we have total 1078 data.")
sleep_together = alt.Chart(demo_df).mark_bar(tooltip = True, size = 70).encode(
    alt.X('count()'),
    alt.Y('Sleep Together?:N', sort='-x', axis=alt.Axis(title='Do couples sleep together?')),
    alt.Color('Sleep Together?', scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).interactive(
).properties(width=600, height=300)
st.write(sleep_together)


# Relationship status
st.title('How the relationships status look like')
status_chart = alt.Chart(demo_df, title='Relationship Status').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('CurrentRelationshipStatus', sort = '-x'), 
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)
st.write(status_chart)

# Timespan of current relationship
length_chart = alt.Chart(demo_df, title='Relationship Length').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('RelationshipLength', sort = '-x'),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)
st.write(length_chart)

# Frequency of sleeping separately
freq_chart = alt.Chart(demo_df, title='Frequency in separate beds').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Frequency in separate beds', sort = ['Never', 'Once a year or less', 'Once a month or less', 'A few times per month', 'A few times per week', 'Every night']),
    color=alt.Color('Sleep Together?',
        scale=alt.Scale(
        domain=['YES', 'NO'],
        range=['pink', 'lightblue']))
).properties(
    width = 600
)
st.write(freq_chart)

# Demographic data
age_chart = alt.Chart(demo_df, title='Age').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Age', sort = ['18-29', '30-44', '45-60', '> 60', 'Did not disclose']),
    color=alt.Color('Sleep Together?',
        scale=alt.Scale(
        domain=['YES', 'NO'],
        range=['pink', 'lightblue']))
).properties(
    width = 600
)

gender_chart = alt.Chart(demo_df, title='Gender').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Gender', sort = '-x'),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)

income_chart = alt.Chart(demo_df, title='Household Income').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Household income', sort = ['$150,000+', '$100,000 - $149,999', '$50,000 - $99,999', '$25,000 - $49,999', '$0 - $24,999', 'Did not disclose']),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)
education_chart = alt.Chart(demo_df, title='Education Level').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Education', sort = ['Graduate degree', 'Bachelor degree', 'Some college or Associate degree', 'High school degree', 'Less than high school degree', 'Did not disclose']),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)

location_chart = alt.Chart(demo_df, title='Location').mark_bar(tooltip = True).encode(
    x = alt.X('count()'),
    y = alt.Y('Location', sort = '-x'),
    color=alt.Color('Sleep Together?',
            scale=alt.Scale(
            domain=['YES', 'NO'],
            range=['pink', 'lightblue']))
).properties(
    width = 600
)

# Drop down list for user to select demographic features
demo_options = st.multiselect(
     'What demographic feature distribution do you want to see?',
     ['Age', 'Gender', 'Household Income', 'Education', 'Location'])
if 'Age' in demo_options:
    st.write(age_chart)
if 'Gender' in demo_options:
    st.write(gender_chart)
if 'Education' in demo_options:
    st.write(education_chart)
if 'Location' in demo_options:
    st.write(location_chart)
if 'Household Income' in demo_options:
    st.write(income_chart)
if 'Location' in demo_options:
    st.write(location_chart)


#====================================== PART 4 =================================================
# Drop down reason selection + questions opinions (box plots)
# Select the reasons for sleeping in separate beds and show the correspondent opinion 
st.title('The reason of sleeping separately and their opinions')
separate_reasons =['Reason_One of us snores',
                'Reason_One of us makes frequent bathroom trips in the night',
                'Reason_One of us is sick','Reason_We are no longer physically intimate',
                'Reason_We have different temperature preferences for the room',
                'Reason_We have had an argument or fight','Reason_Not enough space',
                'Reason_Do not want to share the covers','Reason_One of us needs to sleep with a child',
                'Reason_Night working/very different sleeping times','Reason_Other']

questions = ['Sleeping in separate beds helps us to stay together', 'We sleep better when we sleep in separate beds',
             'Our sex life has improved as a result of sleeping in separate beds' ]

reason_options = st.radio(
    "Select the reason you want to see",
    ['One of us snores','One of us makes frequent bathroom trips in the night',
    'One of us is sick','We are no longer physically intimate',
    'We have different temperature preferences for the room',
    'We have had an argument or fight','Not enough space',
    'Do not want to share the covers','One of us needs to sleep with a child',
    'Night working/very different sleeping times']
)


col = st.columns(2)
selected = alt.selection_single(empty="none")
with col[0]:
    reason_chart = alt.Chart(separate_df, title=reason_options).mark_bar(tooltip = True).encode(
        alt.X('Reason_'+reason_options+':O', axis=alt.Axis(title=' ')),
        alt.Y('count()'),
        color=alt.condition(selected, alt.ColorValue('#FCDEC1'), alt.ColorValue("lightgrey"))
    ).properties(
        height = 500, width = 300
    ).add_selection(selected)
    st.write(reason_chart)

with col[1]:
    selected = alt.selection_single(empty="none")
    reason_chart = alt.Chart(separate_df, title=reason_options).mark_bar(tooltip = True).encode(
        alt.X('Reason_'+reason_options+':O', axis=alt.Axis(title=' ')),
        alt.Y('count()'),
        color=alt.condition(selected, alt.ColorValue('#FCDEC1'), alt.ColorValue("lightgrey"))
    ).properties(
        height = 500, width = 300
    ).add_selection(selected)

    question1_chart = alt.Chart(separate_df, title='Sleeping in separate beds helps us to stay together').mark_bar(tooltip = True
    ).encode(
        alt.X('count()'),
        alt.Y('Sleeping in separate beds helps us to stay together', 
            sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'],
            axis=alt.Axis(title=' '))
    ).transform_filter(selected)

    question2_chart = alt.Chart(separate_df,title='We sleep better when we sleep in separate beds').mark_bar(tooltip = True
    ).encode(
        alt.X('count()'),
        alt.Y('We sleep better when we sleep in separate beds', 
            sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'], 
            axis=alt.Axis(title=' '))
    ).transform_filter(selected)

    question3_chart = alt.Chart(separate_df,title='Our sex life has improved as a result of sleeping in separate beds').mark_bar(tooltip = True
    ).encode(
        alt.X('count()'),
        alt.Y('Our sex life has improved as a result of sleeping in separate beds', 
        sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'],
        axis=alt.Axis(title=' '))
    ).transform_filter(selected)

    st.write(alt.vconcat(reason_chart, question1_chart, question2_chart, question3_chart))





st.markdown("This project was created by Li-Hsin Lin and Kylie Hsieh for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")



# brushes
status_brush = alt.selection_multi(fields=['CurrentRelationshipStatus'])
length_brush = alt.selection_multi(fields=['RelationshipLength'])
freq_brush = alt.selection_multi(fields=['Frequency in separate beds'])
age_brush = alt.selection_multi(fields=['Age'])
gender_brush = alt.selection_multi(fields=['Gender'])
income_brush = alt.selection_multi(fields=['Household income'])
education_brush = alt.selection_multi(fields=['Education'])
location_brush = alt.selection_multi(fields=['Location'])
