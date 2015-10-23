Code for finding/organizing jobs on the AAS job register.

Author: Brendan Griffen (@brendangriffen)  

Disclosure: code is based on https://github.com/gully/AASjobRegister 
            but with many more personal modifications.  

Select your options below for one of your possible future career paths... 

Some instructions.

1. Select the career options you would like to query.
2. Select your display options. Note: it is best to just do a full query on
   your keywords first, then from the in-browser table, select jobids (1st column)
   which are of interest to you. Add those job ids to the job_ids_filter below.
3. Re-run code with your jobids selected and create your deadline plot.


```python
# career options
# select which jobs you would like
WANT_FACULTY_JOBS = False
WANT_POSTDOC_JOB = True
WANT_PHD = False
WANT_ENGINEERING_OR_TECHSTAFF_JOB = False
WANT_MANAGEMENT_JOBS = False
WANT_OTHER_JOBS = False

# display/output options
WANT_JOBS_PAST_DEADLINE = False  # do you want jobs past the deadline?
OPEN_RESULTS_IN_BROWSER = True   # do you want a searchable table in browser?
WANT_DEADLINE_PLOT = True        # do you want a timeline made?
SELECT_OVER_KEYWORDS = True      # do you want to only include the keywords (in descriptions) selected below?
FILTER_OVER_JOB_ID = False       # do you want only specific job ids (best to set once you've queried the keyword selected jobs)
PLOT_KEYWORD_HIST = True         # do you want a histogram of the keywords?

# select your filtered job ids
if FILTER_OVER_JOB_ID: job_ids_filter = [51388,51391,51554,51591,51624]

# select your keywords
keywords = ['theor', 'data-intensive', 'computational', 
            'galax','data science','statistics','simulations', 
            'high performance computing']
```

### Deadlines specific to your jobs
![histogram](https://raw.githubusercontent.com/bgriffen/easyaasjobs/master/jobs_left_timeline.png "Deadlines")  

### Display In Browser

![tables](https://raw.githubusercontent.com/bgriffen/easyaasjobs/master/easyaasjobstable.png "jobs table")

### Keyword Histograms

![deadlines](https://raw.githubusercontent.com/bgriffen/easyaasjobs/master/keywords.png "Keywords")
