import numpy as np
import os,sys
from astropy.table import Table, Column
import jfind as jf
import jtools as jt

"""

Code for finding/organizing jobs on the AAS job register.

Author: Brendan Griffen (@brendangriffen)

Disclosure: code is based on https://github.com/gully/AASjobRegister but with 
            many more personal modifications.

Select your options below for one of your possible future career paths...

Some instructions.

1. Select the career options you would like to query.
2. Select your display options. Note: it is best to just do a full query on
   your keywords first, then from the in-browser table, select jobids (1st column)
   which are of interest to you. Add those job ids to the job_ids_filter below.
3. Re-run code with your jobids selected and create your deadline plot.

"""

# ------------------------------------ 
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

# select what you want to display in the web table
webtable = ('jobid',
          #'PostDate',
          'Deadline',
          'days_left',
          #'JobCategory',
          'Institution',
          'announce',
          'webURL',
          'attn_to',
          #'attn_to_title',
          'attn_to_org',
          #'attn_to_address',
          'attn_to_city',
          #'attn_to_state',
          #'attn_to_zip',
          'attn_to_country',
          #'attn_to_email',
          #'inquiry_email',
          )

# ------------------------------------------------------------------------
# CODE STARTS HERE
# ------------------------------------------------------------------------

datapath = './'
jobs_filename = "jobsforme.txt"
announce_filename = "announcements.txt"
abbriev_filename = "abbriev.dat"
announce_path = datapath+announce_filename
abbriev_path= datapath+abbriev_filename
jobs_path = datapath+jobs_filename

if not os.path.exists(announce_path) or not os.path.exists(abbriev_path) or not os.path.exists(jobs_path):
    print "Could not find file, creating..."
    print " >",announce_path
    print " >",abbriev_path
    print " >",jobs_path

    t = jf.get_all_jobs(announce_path,abbriev_path,jobs_path)    

else:
    print "Found file, loading...",jobs_path
    t = Table.read(jobs_path, format='ascii', delimiter=';')
        
    mask_keys = jt.get_mask_keys(WANT_FACULTY_JOBS,
                                 WANT_POSTDOC_JOB,WANT_PHD,
                                 WANT_ENGINEERING_OR_TECHSTAFF_JOB,
                                 WANT_MANAGEMENT_JOBS,
                                 WANT_OTHER_JOBS)

    days_left = jt.get_days_from_today(t)
    days_left_col = Column(name='days_left', data=days_left)
    t.add_column(days_left_col)

    if SELECT_OVER_KEYWORDS:
        dfk = jt.get_keyword_jobs(keywords,announce_path,abbriev_path)
        dfk = dfk.sort(columns='occurrence')
        print dfk
        if PLOT_KEYWORD_HIST: jt.plot_keywords(dfk,datapath)

        keep_jobs = jt.get_mask_on_keywords(keywords,announce_path,abbriev_path)
        idx_keep_jobs = list(set(keep_jobs))
        
        tsubset_all = jt.get_masked_data(t[idx_keep_jobs],mask_keys)
        
        print "number of unique jobs (total) with your keywords:",len(idx_keep_jobs)
    else:
        tsubset_all = jt.get_masked_data(t,mask_keys)

    tsubset_for_web = tsubset_all[webtable]

    jobs_left_mask = tsubset_for_web['days_left'] >= 0

    if FILTER_OVER_JOB_ID: 
        mask_jobids_want = np.in1d(np.array(tsubset_for_web['jobid']),job_ids_filter,assume_unique=True)
        jobs_left_mask = jobs_left_mask & mask_jobids_want

    tjobsleft = tsubset_for_web[jobs_left_mask]
    
    print "number of unique jobs (left):",len(np.array(tjobsleft['days_left']))

    if OPEN_RESULTS_IN_BROWSER:
        idx_sort_by_time_remaining = np.argsort(np.array(tjobsleft['days_left']))
        #print "Showing jobs for the following categories..."            
        tjobsleft[idx_sort_by_time_remaining].show_in_browser(jsviewer = True)

    if WANT_DEADLINE_PLOT:
        jt.plot_jobs_available(tsubset_all)


print "Good luck! =)"
