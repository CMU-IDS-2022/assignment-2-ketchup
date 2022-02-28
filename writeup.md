# Do Couples Always Sleep Together?

(Figs/screenshot.png)

The project is inspired by a long-lasting question that many kids may have in their childhood: Why my parents don't sleep together?

FiveThirtyEight published an article [*Dear Mona, How Many Couples Sleep in Separate Beds?*](https://fivethirtyeight.com/features/dear-mona-how-many-couples-sleep-in-separate-beds/) with the result of an online survey to explore people's sleeping arrangements with their partner. The survey provides answers to several intriguing questions: How many couples sleep in separate beds? What kind of people doesn't sleep with their partner? Why don't they sleep together? We visualize the dataset through an interactive web application that offers users the opportunity to explore this interesting dataset and unfold the untold.


## Project Goals

As discussed previously, we hope to use this dataset to answer why couples do not sleep together. This well-known but barely discussed question extends the discussion to the broader social psychology area. We utilized the demographic data collected in the survey, such as `age`, `gender`, `household income`, `occupation`, to excavate the insights behind it - are people with specific demographics associated with a higher possibility for sleeping separately with their partner?

Our web application enables users to begin by looking at the dataset, understanding what was in the survey and the basic demographics of the respondents. With that knowledge in mind, we display various topics stemming from the study and allow users to explore them based on their interests. As an example, one section enables users to see the correlation between demographics of those who sleep separately with their partner and the frequency of sleeping separately.


## Design

Our application consists of 7 parts. In part 1, we provide statistical summaries of the survey. In parts 2 and 3, we demonstrate the correlations between demographics and two factors: whether the couple sleeps together or not and the frequency of sleeping separately. In part 4, we introduce the most exciting part of the application - why couples sleep separately. In part 5, we investigate the respondents' opinions of three questions regarding sleeping separately. In part 6, we look at the locations where each couple sleeps if they sleep separately. In part 7, we allow users to select an individual in the dataset randomly.

A large proportion of our application and interactive visualizations is composed of **Select** and **Filter** techniques. We chose these two techniques as the primary interaction between users and charts based on the core questions we wanted to enable the users to answer. Additionally, we wanted to allow users to select demographics of their interests because we don't have a target audience with specific demographics. They can be any gender, at any age, or with any household income range. It is valuable that users can look at the conditional result by selecting their own or interested demographics.

A significant challenge for chart variety is that none of the variables in this survey data is quantitative, even the demographics such as age and household income being designed as categorical. That is to say, our choices of chart types are very limited. To make up for this weakness, we transformed some of the nominal variables to numeric. For example, we converted the `opinion of a specific question` from the scale of `strongly disagree to strongly agree` to the scale of `1 to 5`; we can then present the data in a numeric format like average value or a box chart.


## Development

The project is developed by Kylie Hsieh and Erin Lin. The team works together throughout the project, but to be more specific, Kylie leads the data cleaning and software development, and Erin leads the document write-up and topic development.

We divide the project into three phases: (1) research and discovery, (2) design, and (3) development.
| Phase  | Task and Time Spent (in people-hours) | Total Time Spent (in people-hours)|
| ------------- | ------------- | ------------- |
| Research and Discovery | ・Explore and select dataset of interest (1)<br/> ・Define project scope (2)| 3 |
| Design  | ・High-level design (questions, topics, contents, etc.) (2)<br/> ・Visualization design (chart type, layout, color theme)(3)| 5 |
| Development  | ・Environment setup (0.5)<br/> - Data cleaning (3)<br/> ・Visualization development (15)<br/> - Testing (2)<br/> - Document write-up (2)| 22.5 |

It was pretty smooth when choosing the dataset and topic as a team. It didn't take much time for us to conduct the high-level design either because we both agreed this is an interesting dataset, and our questions derived from the data were similar. In contrast, we spent relatively more time thinking about the visualization design. Because this is survey data, there are actually not too many choices for visualizations but bar charts. We decided to try to incorporate more different interaction techniques to make up for the potential monotonous chart variety.


## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.

As a person whose parents sleep separately, this application helps me answer this difficult question since childhood, even in greater detail. When I was a child, 

According to the survey, of the 483 who do not sleep with their partner, about 45% said it's because one of them `snores`, and 26% responded `sickness`. Other reasons include `different sleeping times`, `frequent bathroom trips in the night`, `children`, `different temperature preferences`, most of which are related to bedroom behaviors or living habits. In contrast, only 15% and 6.6% reported `argument or fight` and `no longer physically intimate`. We observed that, in essence, a majority of the reasons that drive couples to sleep in separate beds are related to bedroom behaviors or living habits and not necessarily related to their emotional relationship. 
