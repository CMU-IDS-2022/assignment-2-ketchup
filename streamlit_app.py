from os import sep
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.title("Do Couples Always Sleep Together? 👩‍❤️‍👨 👩‍❤️‍👩 👨‍❤️‍👨")

image = Image.open('Figs/sleeping_together_or_not.png')
st.image(image, caption='Photo by Somnox Sleep on Unsplash')

st.subheader("Data")
#@st.cache  # add caching so we load the data only once
st.write("The data is collected by a survey conducted by FiveThirtyEight.\
         The survey provides answers to several intriguing questions: How many couples sleep in separate beds?\
         What kind of people don't sleep with their partner? Why don't they sleep together?\
         We hope this web application offers you the opportunity to explore this interesting dataset and unfold the untold.")

# ===================================== PART 0 =====================================
# Read data

def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_raw = 'https://raw.githubusercontent.com/fivethirtyeight/data/22a478af3edc00f69693c3f5f4604b2f1fd024b0/sleeping-alone-data/sleeping-alone-data.csv'
url_separate = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Data/sleep_separately1.csv'
url_together = 'https://raw.githubusercontent.com/CMU-IDS-2022/assignment-2-ketchup/master/Data/sleep_together1.csv'
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

st.write("Source: [Sleeping alone data](https://github.com/fivethirtyeight/data/tree/master/sleeping-alone-data) by FiveThirtyEight")

## ===================================== Functions =====================================

def get_slice_membership(df, genders, age, income, occupation):
    """
    Implement a function that computes which rows of the given dataframe should
    be part of the slice, and returns a boolean pandas Series that indicates 0
    if the row is not part of the slice, and 1 if it is part of the slice.
    
    In the example provided, we assume genders is a list of selected strings
    (e.g. ['Male', 'Transgender']). We then filter the labels based on which
    rows have a value for gender that is contained in this list. You can extend
    this approach to the other variables based on how they are returned from
    their respective Streamlit components.
    """
    labels = pd.Series([1] * len(df), index=df.index)
    if genders:
        labels &= df['Gender'].isin(genders)
    if age:
        labels &= df['Age'].isin(age)
    if income:
        labels &= df['Household income'].isin(income)
    if occupation:
        labels &= df['Occupation'].isin(occupation)
    return labels

def make_long_reason_dataframe(df, reason_prefix):
    """
    ======== You don't need to edit this =========
    
    Utility function that converts a dataframe containing multiple columns to
    a long-style dataframe that can be plotted using Altair. For example, say
    the input is something like:
    
         | why_no_vaccine_Reason 1 | why_no_vaccine_Reason 2 | ...
    -----+-------------------------+-------------------------+------
    1    | 0                       | 1                       | 
    2    | 1                       | 1                       |
    
    This function, if called with the reason_prefix 'why_no_vaccine_', will
    return a long dataframe:
    
         | id | reason      | agree
    -----+----+-------------+---------
    1    | 1  | Reason 2    | 1
    2    | 2  | Reason 1    | 1
    3    | 2  | Reason 2    | 1
    
    For every person (in the returned id column), there may be one or more
    rows for each reason listed. The agree column will always contain 1s, so you
    can easily sum that column for visualization.
    """
    reasons = df[[c for c in df.columns if c.startswith(reason_prefix)]].copy()
    reasons['id'] = reasons.index
    reasons = pd.wide_to_long(reasons, reason_prefix, i='id', j='reason', suffix='.+')
    reasons = reasons[~pd.isna(reasons[reason_prefix])].reset_index().rename({reason_prefix: 'agree'}, axis=1)
    return reasons


# MAIN CODE


# ===================================== PART 1 =====================================
# Basic information
# Sleep together or not?

st.markdown("---")
st.header("Part 1: Sleep Together or Not?")
st.write("Let's start off by looking at how many couples actually sleep together every day.")
st.write("")

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



# ===================================== PART 2 =====================================
# Correlations between frequency of sleeping separately and demographics

st.markdown("---")
st.header("Part 2: Demographics Distributions")
st.write("""The survey collects demographic data of the respondents, including age, gender, household income, and education level.
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


# ===================================== PART 3 =====================================
# Drop down demographics and timespan of relationship selection + reasons (bar chart)
# Select the reasons for sleeping in separate beds and show the correspondent demographics data

st.markdown("---")
st.header("Part 3: Why Do Couples Not Sleep Together?")
st.write("After understanding the dataset and the basic demographics of the respondents, it's time to learn more about\
         one of the most interesting part in this survey: the reason why people don't sleep with their partner.")
st.write("You can select one or more demographics to filter a subset of respondents, and then look at the reasons why\
         this group of people and their partners sleep in separate beds.")


# Dropdown filters
cols = st.columns(4)
with cols[0]:
    genders = st.multiselect('Gender', separate_df['Gender'].unique())
with cols[1]:
    age = st.multiselect('Age', separate_df['Age'].unique())
with cols[2]:
    income = st.multiselect('Household Income', separate_df['Household income'].unique())
with cols[3]:
    occupation = st.multiselect('Occupation', separate_df['Occupation'].unique())
    
# Get the selected vavlues and reasons
slice_labels = get_slice_membership(separate_df, genders, age, income, occupation)
st.write("The sliced dataset contains {} elements ({:.1%} of total).".format(slice_labels.sum(), slice_labels.sum() / len(separate_df)))

# Plot the bar chart for reasons
if slice_labels.sum() < len(separate_df):
    sleep_separately_reasons = make_long_reason_dataframe(separate_df[slice_labels], 'Reason_')
    st.text("The subgroup is selected based on the demographics of your interest.")
    st.write("")
    reasons_chart = alt.Chart(sleep_separately_reasons, title="Why Couples Don't Sleep Together?").mark_bar().encode(
    x=alt.X('sum(agree)', axis=alt.Axis(title='Count of Respondents')),
    y=alt.Y('reason:O', axis=alt.Axis(title='')),
    color = alt.value('#AED6F1')).interactive()
    st.altair_chart(reasons_chart, use_container_width=True)
    st.write("*Note*: One respondent may select multiple reasons.")


# ===================================== PART 4 =====================================
# Drop down reason selection + questions opinions (box plots)
# Select the reasons for sleeping in separate beds and show the correspondent opinion

st.markdown("---")
st.header("Part 4: Is Sleeping Separately Better?")
st.write("""In addition to investigating the reasons for sleeping separately,
         the survey also asked those who don't sleep with their partner for their opinions of the following three questions.""")
st.markdown("- Sleeping in separate beds helps us to stay together")
st.markdown("- We sleep better when we sleep in separate beds")
st.markdown("- Our sex life has improved as a result of sleeping in separate beds")
st.write("")

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

st.subheader('If ' + reason_option.lower() +', does ' + question_option.lower() + ' ?')

yes_proportion = separate_df['Reason_'+reason_option].mean()
no_proportion = 1 - yes_proportion
no_score = separate_df[question_option+'_code'][separate_df['Reason_'+reason_option] == 0].mean()
yes_score = separate_df[question_option+'_code'][separate_df['Reason_'+reason_option] == 1].mean()

col1, col2 = st.columns(2)
with col1:
    ## answer no to the reason
    st.metric(reason_option+' is not the reason', '{:.2%}'.format(no_proportion))
    st.metric('Mean score for question:' + question_option.lower() + '(5 is strongly agree)', 
                round(no_score, 3))
    chart = alt.Chart(separate_df[separate_df['Reason_'+reason_option] == 0], title = 'Is not the reason').mark_bar(tooltip=True).encode(
        alt.X('count()'),
        alt.Y(question_option, title = None,
            sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree']),
        color = alt.value('#A2D9CE')
    )
    st.altair_chart(chart, use_container_width=True)
    
with col2:
    ## answer yea to the reason
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

# Box plot of the question
separate_df['Reason_'+reason_option+'_Y/N'] = separate_df['Reason_'+reason_option].map({0: 'NO', 1: 'YES'})
score_chart = alt.Chart(separate_df, title = 'Box plot for the responses of ' + question_option.lower()).mark_boxplot(size = 50
).encode(
    alt.X(question_option+'_code', title = 'Larger the score, higher the level of agreement'),
    alt.Y('Reason_'+reason_option+'_Y/N', title = None),
    alt.Color('Reason_'+reason_option+'_Y/N', legend = None, 
                scale = alt.Scale(domain = ['YES', 'NO'], range=['#FAD7A0', '#A2D9CE']))
).properties(
    width=700, height = 200
)
st.write(score_chart)
st.markdown("*Note:* `5` represents strongly agree and `1` represents strongly disagree.")


# ===================================== PART 5 =====================================
st.write('---')
st.header("Part 5: What's The Relaitonship Between Demographic Features and The Frequency of Sleeping Separately?")

freq_option = st.selectbox(
    "👇 Select the frequency of sleeping separately you want to see",
    ['A few times per month', 'A few times per week', 'Every night', 'Once a month or less', 'Once a year or less']
)

feature_option = st.selectbox(
    "👇 Select the demographic features you want to use to classify",
    ['Age', 'Gender', 'Education', 'Household income']
)
selected = alt.selection_multi()
place_chart = alt.Chart(separate_df[separate_df['Frequency in separate beds'] == freq_option]).mark_bar(tooltip=True).encode(
    alt.X('count()'),
    alt.Y(feature_option),
    color = alt.value('#A2D9CE')
).properties(
    width = 600
)
st.write(place_chart)



# ===================================== PART 6 =====================================

st.write('---')
st.header("Part 6: If Sleeping Separately, Where Does Each of the Couple Sleep?")
st.write("👇 Select the population demographic features that you want to see")

age_dropdown = alt.binding_select(options = separate_df['Age'].unique())
age_selected = alt.selection_single(
    fields = ['Age'],
    bind = age_dropdown,
    name = "4 Select"
)
edu_dropdown = alt.binding_select(options = separate_df['Education'].unique())
edu_selected = alt.selection_single(
    fields = ['Education'],
    bind = edu_dropdown,
    name = "3 Select"
)
gender_dropdown = alt.binding_select(options = separate_df['Gender'].unique())
gender_selected = alt.selection_single(
    fields = ['Gender'],
    bind = gender_dropdown,
    name = "2 Select"
)
income_dropdown = alt.binding_select(options = separate_df['Household income'].unique())
income_selected = alt.selection_single(
    fields = ['Household income'],
    bind = income_dropdown,
    name = "1 Select"
)
you_sleep_at_chart = alt.Chart(separate_df).mark_bar(tooltip=True).encode(
    alt.X('count()'),
    alt.Y('YouSleepAt', title = 'Respondent sleeping at'),
    color = alt.value('#A2D9CE')
).add_selection(age_selected
).transform_filter(age_selected
).add_selection(edu_selected
).transform_filter(edu_selected
).add_selection(gender_selected
).transform_filter(gender_selected
).add_selection(income_selected
).transform_filter(income_selected
).properties(
    width = 600, height = 200
)
partner_sleep_at_chart = alt.Chart(separate_df).mark_bar(tooltip=True).encode(
    alt.X('count()'),
    alt.Y('PartnerSleepAt', title = 'Partner sleeping at'),
    color = alt.value('#FAD7A0')
).add_selection(age_selected
).transform_filter(age_selected
).add_selection(edu_selected
).transform_filter(edu_selected
).add_selection(gender_selected
).transform_filter(gender_selected
).add_selection(income_selected
).transform_filter(income_selected
).properties(
    width = 600, height = 200
)

st.write(you_sleep_at_chart & partner_sleep_at_chart)


# ===================================== PART 7 =====================================

st.write('---')
st.header("Part 7: Person Sampling")

st.write("""
Select a random person from the data, and see his/her characteristics""")

sleep_separate = st.checkbox("Sample a person who sometimes sleeps separately with his/her partner")

if st.button("Get Random Person"):
    df_to_sample = separate_df if sleep_separate else together_df
    person = df_to_sample.sample(n=1).iloc[0]
    st.write(f"""
This person is a **{person.Gender.lower()}**, his/her job is **{person.Occupation.lower()}**, age is between **{person.Age}**, with a 
**{person.Education.lower()}**, and a household income between **{person['Household income'].lower()}**.""")
    
    st.write(f"""The sampled person is **{person.CurrentRelationshipStatus.lower()}**, 
            and has been together for **{person.RelationshipLength.lower()}**.""")

    if sleep_separate:
        st.write(f"""This person sleeps separately with his/her partner **{person['Frequency in separate beds'].lower()}**.""")
        st.write(f'When they are not sleeping together:')
        st.markdown(f"""- The place where this person sleeps: **{person.YouSleepAt.lower()}**.""") 
        st.write(f"""- The place where his/her partner sleeps: **{person.PartnerSleepAt.lower()}**.""")
    
    else:
        st.write(f"""This person sleeps with his/her partnes.""")


st.markdown("---")
st.markdown("This project was created by Erin Lin and Kylie Hsieh for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")