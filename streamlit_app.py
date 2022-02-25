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

##==============================================function===============================================
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
st.markdown("---")

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
st.markdown("---")
st.header("Part 3: Why Couples Do Not Sleep Together?")

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
    st.markdown("""---""")
    st.write("The subgroup is selected based on the demographics of your interest.")
    st.write("")
    reasons_chart = alt.Chart(sleep_separately_reasons, title="Why Couples Don't Sleep Together?").mark_bar().encode(
    x=alt.X('sum(agree)', axis=alt.Axis(title='Count of Respondents')),
    y=alt.Y('reason:O', axis=alt.Axis(title=''))).interactive()
    st.altair_chart(reasons_chart, use_container_width=True)


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

# separate_df['Reason_'+reason_option+'_Y/N'] = separate_df['Reason_'+reason_option].map({0: 'NO', 1: 'YES'})
# chart_title = 'If ' + reason_option.lower() +', does ' + question_option.lower() + ' ?'
# reason_chart = alt.Chart(separate_df, title = chart_title).mark_bar(tooltip = True).encode(
#     alt.X('count()'),
#     alt.Y(question_option, title = None,
#             sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree']),
#     alt.Color('Reason_'+reason_option+'_Y/N', scale = alt.Scale(domain=['YES', 'NO'], range=['Orange', 'lightgreen']), legend = None),
#     column = 'Reason_'+reason_option+'_Y/N'
# ).properties(
#     width = 250, height=200
# )
# st.write(reason_chart)

st.write("---")
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
    chart = alt.Chart(separate_df[separate_df['Reason_'+reason_option] == 0]).mark_bar(tooltip=True).encode(
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
score_chart = alt.Chart(separate_df, title=question_option).mark_boxplot(size = 50).encode(
    alt.X(question_option+'_code', title = 'Larger the score, higher the level of agreement'),
    alt.Y('Reason_'+reason_option+'_Y/N', title = None),
    alt.Color('Reason_'+reason_option+'_Y/N', legend = None, 
                scale = alt.Scale(domain = ['YES', 'NO'], range=['#FAD7A0', '#A2D9CE']))
).properties(
    width=700, height = 200
)
st.write(score_chart)
    
# col = st.columns(2)
# selected = alt.selection_multi(empty="none", on='mouseover')
# with col[0]:
#     reason_chart = alt.Chart(separate_df, title=reason_options).mark_bar(tooltip = True).encode(
#         alt.X('Reason_'+reason_options+':O', axis=alt.Axis(title=None)),
#         alt.Y('count()'),
#         color=alt.condition(selected, alt.ColorValue('#FCDEC1'), alt.ColorValue("lightgrey"))
#     ).properties(
#         height = 500, width = 300
#     ).add_selection(selected)
#     st.write(reason_chart)

# with col[1]:
#     # selected = alt.selection_single(empty="none")
#     # reason_chart = alt.Chart(separate_df, title=reason_options).mark_bar(tooltip = True).encode(
#     #     alt.X('Reason_'+reason_options+':O', axis=alt.Axis(title=' ')),
#     #     alt.Y('count()'),
#     #     color=alt.condition(selected, alt.ColorValue('#FCDEC1'), alt.ColorValue("lightgrey"))
#     # ).properties(
#     #     height = 500, width = 300
#     # ).add_selection(selected)

#     question1_chart = alt.Chart(separate_df, title='Sleeping in separate beds helps us to stay together').mark_bar(tooltip = True
#     ).encode(
#         alt.X('count()'),
#         alt.Y('Sleeping in separate beds helps us to stay together', 
#             sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'],
#             axis=alt.Axis(title=' ')),
#         color = 'Reason_'+reason_options+':O'
#     ).transform_filter(selected)

#     question2_chart = alt.Chart(separate_df,title='We sleep better when we sleep in separate beds').mark_bar(tooltip = True
#     ).encode(
#         alt.X('count()'),
#         alt.Y('We sleep better when we sleep in separate beds', 
#             sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'], 
#             axis=alt.Axis(title=' '))
#     ).transform_filter(selected)

#     question3_chart = alt.Chart(separate_df,title='Our sex life has improved as a result of sleeping in separate beds').mark_bar(tooltip = True
#     ).encode(
#         alt.X('count()'),
#         alt.Y('Our sex life has improved as a result of sleeping in separate beds', 
#         sort = ['Strongly agree', 'Somewhat agree','Neither agree nor disagree', 'Somewhat disagree', 'Strongly disagree'],
#         axis=alt.Axis(title=' '))
#     ).transform_filter(selected)

#     st.write(alt.vconcat(question1_chart, question2_chart, question3_chart))

# ===================================== PART 5 =====================================
st.header("Part 5: If Sleeping Separately, Where Does Each Of The Couple Sleep?")

freq_option = st.selectbox(
    "👇 Select the frequency of sleeping separately you want to see",
    ['A few times per month', 'A few times per week', 'Every night', 'Once a month or less', 'Once a year or less']
)

feature_option = st.selectbox(
    "👇 Select the demographic features you want to see",
    ['Age', 'Gender', 'Education', 'Household income']
)
selected = alt.selection_multi()
place_chart = alt.Chart(separate_df[separate_df['Frequency in separate beds'] == freq_option]).mark_bar().encode(
    alt.X('count()'),
    alt.Y('YouSleepAt'),
    color = feature_option
).add_selection(selected)

partner_chart = alt.Chart(separate_df[separate_df['Frequency in separate beds'] == freq_option]).mark_bar().encode(
    alt.X('count()'),
    alt.Y('PartnerSleepAt'),
    color = feature_option
).transform_filter(selected)
st.write(place_chart & partner_chart)




st.markdown("---")
st.markdown("This project was created by Erin Lin and Kylie Hsieh for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")

