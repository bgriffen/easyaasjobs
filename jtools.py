import numpy as np
import datetime
from dateutil import parser
from scipy import stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime as datetime
import pandas as pd

def get_mask_keys(WANT_FACULTY_JOBS,WANT_POSTDOC_JOB,WANT_PHD,WANT_ENGINEERING_OR_TECHSTAFF_JOB,WANT_MANAGEMENT_JOBS,WANT_OTHER_JOBS):
    mask_keys = []
    if WANT_FACULTY_JOBS:
        mask_keys.append("Faculty Positions (tenure and tenure-track)")
        mask_keys.append("Faculty Positions (visiting and non-tenure)")
    if WANT_POSTDOC_JOB:
        mask_keys.append("Post-doctoral Positions and Fellowships")
    if WANT_PHD:
        mask_keys.append("Pre-doctoral/Graduate Positions")
    if WANT_ENGINEERING_OR_TECHSTAFF_JOB:
        mask_keys.append("Scientific/Technical Staff")
        mask_keys.append("Science Engineering")
    if WANT_MANAGEMENT_JOBS:
        mask_keys.append("Science Management")
    if WANT_OTHER_JOBS:
        mask_keys.append("Other")
    return mask_keys

def plot_jobs_available(tsubset):
    #print "Unique jobs:",set(t['JobCategory'])
    N_jobs = len(tsubset['JobCategory'])
    cats = set(tsubset['JobCategory'])
    N_cats = len(cats)
    vi, vc = np.unique(tsubset['JobCategory'].data.tolist(), return_counts=True)
    dct = {'name':vi, 'counts':vc}
    tdf = pd.DataFrame(dct)
    sortedvi = [x for (y,x) in sorted(zip(vc,vi))]
    dateArr = []
    for i in range(N_jobs):
        dt = parser.parse(tsubset['Deadline'].data[i])
        dateArr.append(dt)
    days = np.asarray([timer.timetuple().tm_yday for timer in dateArr])
    today = int(datetime.datetime.now().timetuple().tm_yday)
    nextYear = (days < today-90)
    days[nextYear] += 365
    days = days - today
    nov1 = datetime.datetime(2015, 11, 1).timetuple().tm_yday - today
    nov15 = datetime.datetime(2015, 11, 14).timetuple().tm_yday - today
    dec1 = datetime.datetime(2015, 12, 1).timetuple().tm_yday - today
    dec15 = datetime.datetime(2015, 12, 14).timetuple().tm_yday - today
    
    #jan15 = datetime.datetime(2016, 1, 14).timetuple().tm_yday - today
    jan1 = 365 - today

    # time to plot
    print "Plotting: jobs_left_timeline.png"
    fig,ax = plt.subplots(figsize=(15,6))
    #hist,val = np.histogram(days,bins=150)
    #print hist
    ax.hist(days,alpha=0.5,bins=150)
    ax.plot([0, 0], [0, 100], '-', color='k',linewidth=3,label='today')
    xfill = np.linspace(-30,0,10)
    jobs_remaining = np.sum(days > 0)
    
    ax.plot([nov15, nov15], [0, 100], ':', color='b',linewidth=2,label='November 15')
    ax.plot([dec1, dec1], [0, 100], '--', color='b',linewidth=2,label='December 1')
    ax.plot([dec15, dec15], [0, 100], ':', color='r',linewidth=2,label='December 15')
    ax.plot([jan1, jan1], [0, 100], '--', color='r',linewidth=2,label='January 1')
    #ax.plot([jan15, jan15], [0, 100], ':', color='g',linewidth=2,label='January 15')
    
    ax.fill_between(xfill,0,1000, color="none", hatch="X", edgecolor="k")

    #ax.text(dec1+1, 35, 'December 1', color ='b', rotation=90, fontsize=28,va='center')
    #ax.text(jan1+1, 35, 'January 1', color ='r', rotation=90, fontsize=28,va='center')
    #ax.text(1, 35, 'today', color ='k', rotation=90, fontsize=28,va='center')
    
    ax.set_xlabel('days from today',fontsize=16)
    ax.set_ylabel('number of jobs',fontsize=16)
    ax.set_title("Job Deadlines from the AAS Job Register - jobs remaining (based on your keywords): %i" % (jobs_remaining))
    ax.set_xlim([-30, 120])
    maxval,vals = np.histogram(days,bins=150)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,frameon=False,loc='upper right')
    ax.set_ylim([0,np.max(maxval)+5])
    fig.savefig('./jobs_left_timeline.png',bbox_inches='tight',dpi=200)
    plt.close()
    #plt.show()

def get_masked_data(t,mask_keys):

    mask = [False]*len(t['JobCategory'])

    for maski in mask_keys:
        mask += (t['JobCategory'] == maski)

    return t[mask]

def get_days_from_today(t):
    dateArr = []
    for date in t['Deadline'].data:
        dt = parser.parse(date)
        dateArr.append(dt)

    days = np.asarray([timer.timetuple().tm_yday for timer in dateArr])
    today = int(datetime.datetime.now().timetuple().tm_yday)
    days_left = days - today

    return  days_left

def get_keyword_jobs(keywords,announce_path,abbriev_path,verbose=False):
    announceFile = open(announce_path, 'r')
    announce = []
    
    for line in announceFile:
        announce.append(line)
    announceFile.close()
    
    # The lord list of jobs, separate from the announcements
    dat = pd.read_csv(abbriev_path, sep=';')
    totHits = []
    for thisWord in keywords:
        occurences = []
        for advert in announce:
            thisAdvert = advert.lower()
            thisCount = thisAdvert.count(thisWord.lower())
            occurences.append(thisCount)
    
        occurences = np.asarray(occurences)
        dat[thisWord] = occurences
        hits = (occurences > 0)
        totHits.append(sum(hits))
        if verbose: print sum(hits), thisWord

    dct = {'keyword':keywords, 'occurrence':totHits}
    df = pd.DataFrame(dct)
    return df
    
def plot_keywords(dfk,dpath):
    oc = np.array(dfk['occurrence'])
    hist_dict = dict((key,val) for key,val in zip(dfk['keyword'],oc))
    fig,ax = plt.subplots()
    label_locs = np.arange(len(hist_dict))
    idx = np.argsort(oc)
    ax.bar(label_locs[idx], oc[idx], align='center',alpha=0.5)
    ax.set_xticks(label_locs)
    ax.set_xticklabels(hist_dict.keys(), rotation=90)
    ax.set_xlim([label_locs[0]-1,label_locs[-1]+1])
    ax.set_ylabel('number of times it occured in job descriptions')
    fig.savefig(dpath+'/keywords.png',bbox_inches='tight',dpi=200)
    plt.close(fig)


def get_mask_on_keywords(keywords,announce_path,abbriev_path,verbose=False):
    announceFile = open(announce_path, 'r')
    announce = []
    
    for line in announceFile:
        announce.append(line)

    announceFile.close()
    
    # The lord list of jobs, separate from the announcements
    dat = pd.read_csv(abbriev_path, sep=';')
    totHits = []
    keepjob = []
    for thisWord in keywords:
        for jobi,advert in enumerate(announce):
            thisAdvert = advert.lower()
            if thisWord in thisAdvert:
                keepjob.append(jobi)

    return np.array(keepjob,dtype='int32')