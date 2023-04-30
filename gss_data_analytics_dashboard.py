#!/usr/bin/env python
# coding: utf-8

# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
# 
# ## Name: Brook Tarekegn Assefa
# ## ID: rnc3mm
# 
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# ## Problem 0
# Import the following libraries:

# In[1]:


import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# For this lab, we will be working with the 2019 General Social Survey one last time.

# In[2]:


gss = pd.read_csv("gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
# In[3]:


gss.head()


# In[4]:


#  https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv


# Here is code that cleans the data and gets it ready to be used for data visualizations:

# In[5]:


mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk' , 'childs' , 'rincome'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork',
                              'childs': 'children_number',
                              'rincome': 'respondent_income'
                             },axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')


# The `gss_clean` dataframe now contains the following features:
# 
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."
# * `children_number` -  number of children
# * `respondent_income` - respondent's income group from occupation before taxes or other deductions.

# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
# 
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
# 
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
# 
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
# 
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

# In[6]:


gender_wage_gap_paragraph = '''
## The Gender Wage Gap 

According to the Global Gender Gap Report by World Economic Forum in 2022, 
**_"Gender parity is not recovering, and It will take another 132 years to close 
the global gender gap_."** 
The gender wage gap is a well-documented phenomenon that refers to the difference 
in earnings between men and women for the same role and responsibilities. 
The most salient factors contributing to gender-based wealth inequity are gender 
pay gaps, unequal career progression trajectories, gender gaps in financial literacy, 
and life events that typically influence women's participation in paid work and their 
ability to contribute to wealth accumulation. Childcare-related life events have the 
greatest impact on gender wealth equity, with women accumulating only 74% of the
wealth of men on average after a 40-year career in comparable roles if they have 
a child to care for.

Despite high levels of female representation in certain industries, 
there remains a gender gap in leadership roles. In the Personal Services and
well-being industry, for instance, women account for 62% of the total workforce
but only 45% of leadership positions.

**Is the gender wage gap due to underperformance in leadership?**
As an analyst, I was motivated to investigate the relationship between political
leadership positions and their potential impact on a country's economy, 
given that these positions represent the highest level of achievement in this domain. 

The global average share of women in parliament rose to 22.9%, with Mexico (50%),
Nicaragua (50.6%), and Rwanda (61.3%) having the highest shares of women in parliament.
It is interesting that the countries Nicaragua and Rwanda recorded the highest
economic growth as a country over the past decade and reached the pinnacle 
last year with 17.70 and 20.06 respectively in their quarterly GDP Growth Rate.

Sources: 
[weforum](https://www.weforum.org/reports/global-gender-gap-report-2022/) , 
[American Lifetime wage gap](https://nwlc.org/resource/the-lifetime-wage-gap-state-by-state/),
[tradingeconomics](https://tradingeconomics.com/)
'''


# In[7]:


General_Social_Survey_GSS_paragraph = '''
## The General Social Survey (GSS)    

The **General Social Survey (GSS)** is a biennial survey conducted by the 
National Opinion Research Center (NORC) at the University of Chicago. 
The survey has been conducted since 1972 and is designed to gather data
on social trends and attitudes in the United States.
The GSS collects information on a wide range of topics, 
including race relations, gender roles, politics, and religion. 
The data is collected through face-to-face interviews with a nationally 
representative sample of adults in the United States.

The gss_clean dataframe provided in this lab contains data from the GSS, 
including information on respondents' 
sex, education, region, age, income, job prestige, and attitudes towards gender roles.
The data has been cleaned and processed for analysis, and includes a weight variable 
to adjust for sampling bias. This dataset provides a valuable source of information
for researchers and policymakers interested in understanding social trends in the
United States. 
'''


# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# In[8]:


gss_clean.head()


# In[9]:


# create a new  mean table dataframe grouped by sex
mean_table = gss_clean.groupby('sex')[['income',
                                'job_prestige',
                                'socioeconomic_index', 
                                'education']].mean().round(2)

# create a table with Plotly
mean_table_figure = go.Figure(data=[go.Table(
    header=dict(values=['<b>Gender</b>',
                        '<b>Mean Income</b>',
                        '<b>Mean Occupational Prestige</b>', 
                        '<b>Mean Socioeconomic Index</b>',
                        '<b>Mean Years of Education</b>'],
                fill_color='paleturquoise',
                align='center'),
    cells=dict(values=[mean_table.index, 
                       mean_table['income'], 
                       mean_table['job_prestige'],
                       mean_table['socioeconomic_index'],
                       mean_table['education']],
               fill_color='lavender',
               align='center'))
]).update_layout(width=800,
                 height=400,
                 title_font_size=20) # format table and layout

# create Dash app
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# set layout of app
app.layout = html.Div(children=[ 
    dcc.Graph(id='mean_table_id',
              figure=mean_table_figure)
])

# run the app
if __name__ == '__main__':
    app.run_server(mode='inline',port=8052)


# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[32]:


# Define the layout
barplot_layout = {
    'xaxis': {'title': 'Level of Agreement'},
    'yaxis': {'title': 'Number of Respondents'},
    'barmode': 'group'
}
# Save the barplot layout since I will be using it for question 7
male_breadwinner_barplot_figure = {
    'data': [
        {'x': gss_clean[gss_clean['sex']=='male']['male_breadwinner'].value_counts().index,
         'y': gss_clean[gss_clean['sex']=='male']['male_breadwinner'].value_counts().values,
         'name': 'Male',
         'orientation': 'v',
         'type': 'bar'},
        {'x': gss_clean[gss_clean['sex']=='female']['male_breadwinner'].value_counts().index,
         'y': gss_clean[gss_clean['sex']=='female']['male_breadwinner'].value_counts().values,
         'name': 'Female',
         'orientation': 'v',
         'type': 'bar'}
    ],
    'layout': barplot_layout
}
# Create the interactive barplot
app = JupyterDash(__name__, external_stylesheets=external_stylesheets) 
app.layout = html.Div([
    dcc.Graph(id='male_breadwinner_barplot_id', 
              figure=male_breadwinner_barplot_figure)
])

if __name__ == '__main__':
    app.run_server(mode='inline',port=8053)


# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# In[11]:


# Clean data / remove the missing or NA values
gss_clean = gss_clean.dropna(subset=['income', 'job_prestige', 'sex'])

# Create scatterplot
job_prestige_income_scatterplot_figure = go.Figure()

for sex in ['male', 'female']:
    df_sex = gss_clean[gss_clean['sex']==sex]
    
    # Add scatter trace
    job_prestige_income_scatterplot_figure.add_trace(go.Scatter(
        x=df_sex['job_prestige'],
        y=df_sex['income'],
        mode='markers',
        name=sex.title(),
        marker=dict(color='blue' if sex == 'male' else 'red'),
        hovertemplate='<br>'.join([ 
            'Income: %{y:$,.0f}',
            'Education: %{customdata[0]} years',
            'Socioeconomic Index: %{customdata[1]}'
        ]),
        text=df_sex['sex'].replace({'male': 'Male', 'female': 'Female'}),
        customdata=df_sex[['education', 'socioeconomic_index']]
    ))

# Add best-fit lines
male_fit = np.polyfit(gss_clean[gss_clean['sex']=='male']['job_prestige'],
                      gss_clean[gss_clean['sex']=='male']['income'], 1)
female_fit = np.polyfit(gss_clean[gss_clean['sex']=='female']['job_prestige'],
                        gss_clean[gss_clean['sex']=='female']['income'], 1)
job_prestige_income_scatterplot_figure.add_trace(go.Scatter(
    x=gss_clean[gss_clean['sex']=='male']['job_prestige'].sort_values(),
    y=np.polyval(male_fit,
                 gss_clean[gss_clean['sex']=='male']['job_prestige'].sort_values()),
    name='Male Best-fit Line',
    mode='lines',
    line=dict(color='green')
))
job_prestige_income_scatterplot_figure.add_trace(go.Scatter(
    x=gss_clean[gss_clean['sex']=='female']['job_prestige'].sort_values(),
    y=np.polyval(female_fit,
                 gss_clean[gss_clean['sex']=='female']['job_prestige'].sort_values()),
    name='Female Best-fit Line',
    mode='lines',
    line=dict(color='darkorange')
))

# Set layout
job_prestige_income_scatterplot_figure.update_layout(
    title='Scatterplot of Job Prestige and Income by Sex',
    xaxis_title='Job Prestige',
    yaxis_title='Income',
    legend_title='Sex'
)

# Create app
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# Set layout
app.layout = html.Div([
    dcc.Graph(id='job_prestige_income_scatterplot_id',
              figure=job_prestige_income_scatterplot_figure)
])

if __name__ == '__main__':
    app.run_server(mode='inline',port=8054)


# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

# In[12]:


# Create interactive boxplot for income by sex
income_boxplot_figure = px.box(gss_clean, 
                        x='sex',
                        y='income',
                        color='sex',
                        points=False,
                        labels={'income': 'Income', 'sex': ''},
                       color_discrete_map={'male': 'blue', 'female': 'red'})
income_boxplot_figure.update_layout(showlegend=False)

# Create interactive boxplot for job_prestige by sex
prestige_boxplot_figure = px.box(gss_clean,
                          x='sex',
                          y='job_prestige',
                          color='sex',
                          points=False,
                          labels={'job_prestige': 'Job Prestige', 'sex': ''},
                          color_discrete_map={'male': 'blue', 'female': 'red'})
prestige_boxplot_figure.update_layout(showlegend=False)

# Create app
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# Set layout
app.layout = html.Div([ 
    dcc.Graph(id='income_boxplot_id', figure=income_boxplot_figure), 
    dcc.Graph(id='prestige_boxplot_id', figure=prestige_boxplot_figure)
])

if __name__ == '__main__':
    app.run_server(mode='inline',port=8055)


# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
# 
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
# 
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

# In[13]:


# create new dataframe with income, sex, and job_prestige
new_gss_clean = gss_clean[['income', 'sex', 'job_prestige']].copy()

# create six equally sized ranges for job_prestige
new_gss_clean['job_prestige_category'] = pd.qcut(new_gss_clean['job_prestige'],
                                                 q=6,
                                                 labels=False)

# drop any rows with missing values. 
# Dropping Would not be required because I already cleaned the gss_clean previously
new_gss_clean.dropna(inplace=True)

# create color map for male/female
color_map = {'male': 'blue', 'female': 'red'}

# create facet grid
job_prestige_facet_grid_figure = px.box(new_gss_clean, 
             x='job_prestige_category', 
             y='income', color='sex',
             facet_col='sex', 
             facet_row='job_prestige_category',
             labels={'income': 'Income', 
                     'job_prestige_category': 'Job Prestige Category'
                    },
             category_orders={'job_prestige_category': [5,4,3,2,1,0]},
             color_discrete_map=color_map)

# remove legend and update layout
job_prestige_facet_grid_figure.update_layout(
    showlegend=False,
    margin=dict(l=20, r=20, t=50, b=20),
    height=1000,
    font=dict(size=10),
    paper_bgcolor='rgba(0,0,0,0)'
)


# Create app
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# Set layout
app.layout = html.Div([
    dcc.Graph(id='job_prestige_facet_grid_id', figure=job_prestige_facet_grid_figure)
])

if __name__ == '__main__':
    app.run_server(mode='inline',port=8056)


# ## Problem 7
# Create a dashboard that displays the following elements:
# 
# * A descriptive title
# 
# * The markdown text you wrote in problem 1
# 
# * The table you made in problem 2
# 
# * The barplot you made in problem 3
# 
# * The scatterplot you made in problem 4
# 
# * The two boxplots you made in problem 5 side-by-side
# 
# * The faceted boxplots you made in problem 6
# 
# * Subtitles for all of the above elements
# 
# Use `JupyterDash` to display this dashboard directly in your Jupyter notebook.
# 
# Any working dashboard that displays all of the above elements will receive full credit. [4 points]

# In[14]:


# Since I have assigned all the figures to constant Object variables 
# I can reuse the figures here. Reusability is considered pythonic.

# Create app
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    
    # Title
    html.H1('GSS Data Analysis', style={'text-align': 'center'}),
    
    # Markdown Text
    html.H3('Problem 1: Markdown Paragraphs'),
    dcc.Markdown(children=gender_wage_gap_paragraph),
    dcc.Markdown(children=General_Social_Survey_GSS_paragraph),
    
    # Table
    html.H3('Problem 2: Mean Characteristics by Gender Table'),
    dcc.Graph(id='mean_table_id', figure=mean_table_figure),
    
    # Barplot
    html.H3('Problem 3: Male as Bread Winner Agreement Barplot'),
    dcc.Graph(id='male_breadwinner_barplot_id',
              figure=male_breadwinner_barplot_figure),
    
    # Scatterplot
    html.H3('Problem 4: Job Prestige and Income by Sex Scatterplot'),
        dcc.Graph(id='job_prestige_income_scatterplot_id',
              figure=job_prestige_income_scatterplot_figure),
    
    # Boxplots
html.H3('Problem 5: Income and Job Prestige by Sex Boxplots'),
html.Div([
    html.Div([
        html.H6('Distribution of Income by Sex', style={'text-align': 'center'}),
        dcc.Graph(id='income_boxplot_id', figure=income_boxplot_figure),
    ], className='six columns'),
    html.Div([
        html.H6('Distribution of Job Prestige by Sex', style={'text-align': 'center'}),
        dcc.Graph(id='prestige_boxplot_id', figure=prestige_boxplot_figure),
    ], className='six columns'),
], className='row'),
    
    # Faceted Boxplots
    html.H3('Problem 6: Job Prestige into six categories Faceted Boxplots'),
    dcc.Graph(id='job_prestige_facet_grid_id', figure=job_prestige_facet_grid_figure),
    
], style={'width': '100%', 'height': '10000', 'margin': '0 auto'})


if __name__ == '__main__':
    app.run_server(mode='inline', port=8057)


# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
# 
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
# 
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
# 
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.

# In[ ]:





# ### This is a code to download the entire Notebook as HTML to the current Directory
# ### Note: Full display requires running all chuncks before this section

# In[30]:


# Reusable function to export as HTML to see the entire Notebook
import re 
import nbformat
from jinja2 import pass_eval_context
from markupsafe import Markup, escape
from nbconvert.exporters import HTMLExporter
from traitlets.config import Config
from IPython.display import display, HTML

def escape_html_keep_quotes(text):
    """Escapes HTML special characters but keeps quotes."""
    return Markup(re.sub(r'(<.*?>)',
                         lambda m: Markup(m.group(0)).unescape().replace('"', '&quot;'), text))

c = Config()
c.HTMLExporter.filters = {'escape_html_keep_quotes': escape_html_keep_quotes}

html_exporter = HTMLExporter(config=c)
notebook_node = nbformat.read(open("labassignment12.ipynb"), as_version=4)
(body, resources) = html_exporter.from_notebook_node(notebook_node)

with open('labassignment12.html', 'w') as f:
    f.write(body)


# In[ ]:




