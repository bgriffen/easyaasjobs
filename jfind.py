from bs4 import BeautifulSoup
from urllib2 import urlopen
import pandas as pd
import re
from astropy.table import Table, Column
import numpy as np
import sys
import os

def extract_and_format_AAS_sibling_entry(cup_of_soup, sub_tag_name):
    entry = "---"
    thisTag = cup_of_soup.find('div',sub_tag_name)
    if (thisTag != None):
        thisLabel = thisTag.find("div", "field-label-inline-first")
        sibling = thisLabel.next_sibling
        formatted_content = re.sub(' +',' ',sibling).encode('utf-8', 'ignore').replace("\r\n", "")
        entry = unicode(formatted_content, errors='ignore')
    return entry


def get_all_jobs(announce_path,abbriev_path,jobs_path):

    BASE_URL = "https://jobregister.aas.org/"
    html = urlopen(BASE_URL).read()
    soup = BeautifulSoup(html, "lxml")
    pppcp2 = soup.find("div", "panel-pane pane-custom pane-2")
    paneContent = pppcp2.find("div", "pane-content")
    pcTab = paneContent.find("table")
    allRows = pcTab.findAll("tr")
    
    lordList = []
    for row in allRows:
        td = row.find("td")
        if (td != None):
            link = td.a["href"]
            lordList.append(BASE_URL+link)
    
    print 'There are ', len(lordList), ' jobs listed on the AAS job register.'
    
    # Job Details
    institute_field = "field field-type-text field-field-institution-name"
    jobCat_field = "field field-type-text field-field-job-category"
    
    # Submission Address for Resumes/CVs
    attn_to_field = 'field field-type-text field-field-attention-to'
    attn_to_title_field = 'field field-type-text field-field-attention-to-title'
    attn_to_org_field = 'field field-type-text field-field-attention-to-rganization' #[sic]
    attn_to_address_field = 'field field-type-text field-field-attention-to-street-addres' #[sic]
    attn_to_city_field = 'field field-type-text field-field-attention-to-city'   
    attn_to_state_field = 'field field-type-text field-field-attention-state-province'
    attn_to_zip_field = 'field field-type-text field-field-zip-postal-code'         
    attn_to_country_field = 'field field-type-text field-field-attention-to-country' 
    attn_to_email_field =   'field field-type-text field-field-attention-to-email'
    
    # Inquiries
    inquiry_email_field = "field field-type-text field-field-inquirie-email" #[sic]
    
    # Desired columns:
    PostDate = []
    Deadline = []
    JobCategory = []
    Institution = []
    attn_to = []
    attn_to_title = []
    attn_to_org = []
    attn_to_address = []
    attn_to_city = []
    attn_to_state = []
    attn_to_zip = []
    attn_to_country = []
    attn_to_email = []
    inquiry_email = []
    joburls = []
    jobids = []
    #this is a bad coding strategy because the memory/entry will be that of the largest string:
    announce = [] 
    
    out_arr  = [PostDate,
                Deadline, 
                JobCategory,
                Institution,
                joburls,
                attn_to,
                attn_to_title,
                attn_to_org,
                attn_to_address,
                attn_to_city,
                attn_to_state,
                attn_to_zip,
                attn_to_country,
                attn_to_email,
                inquiry_email,
                announce,
                jobids]
    
    out_names = ('PostDate',
                'Deadline',
                'JobCategory',
                'Institution',
                'webURL',
                'attn_to',
                'attn_to_title',
                'attn_to_org',
                'attn_to_address',
                'attn_to_city',
                'attn_to_state',
                'attn_to_zip',
                'attn_to_country',
                'attn_to_email',
                'inquiry_email',
                'announce',
                'jobid')
    
    #subLordList = lordList
    
    i = 0
    for webLink in lordList:
        i+=1
        #print i
        if ((i % 10) == 0):
            print i," URLs processed!"
        thisHtml = urlopen(webLink).read()
        jobid = webLink.split("=")[-1]
        soup = BeautifulSoup(thisHtml, "lxml")
        #time.sleep(1)
        #print soup
        # ---Submission Dates---
        # n.b non-standard extraction strategy here.
        gsd = soup.find("fieldset", "fieldgroup group-submission-dates")
        dds = gsd.findAll("span","date-display-single")
        
        PostDate.append(str(dds[0].contents[0]))
        Deadline.append(str(dds[2].contents[0]))
        
        # ---Job Details---
        gjd = soup.find("fieldset", "fieldgroup group-job-details")
        
        job_category = extract_and_format_AAS_sibling_entry(gjd,jobCat_field)

        JobCategory.append(job_category)
        Institution.append(extract_and_format_AAS_sibling_entry(gjd,institute_field))
        
        # ---Submission Address for Resumes/CVs---
        gsa = soup.find("fieldset", "fieldgroup group-submission-address")
    
        attn_to.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_field))
        attn_to_title.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_title_field))
        attn_to_org.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_org_field))
        attn_to_address.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_address_field))
        attn_to_city.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_city_field))
        attn_to_state.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_state_field))
        attn_to_zip.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_zip_field))
        attn_to_country.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_country_field))
        attn_to_email.append(extract_and_format_AAS_sibling_entry(gsa, attn_to_email_field))
        jobids.append(jobid)
        #joburls.append('<a href="'+webLink+'">'+webLink+'</a>')
        joburls.append(webLink)

        # ---Contact Information For Inquiries about the Job---
        gin = soup.find("fieldset", "fieldgroup group-inquiries")
        
        if (gin != None):
            inquiry_email.append(extract_and_format_AAS_sibling_entry(gin, inquiry_email_field))
        else:
            inquiry_email.append(unicode('---'))
        
        # Announcement 
        # nb. Slightly different parsing than the others above
        gga = soup.find("fieldset", "fieldgroup group-announcement")
        ann_tag = gga.find('div', 'field-items')
        announce_raw = ann_tag.getText().encode('utf-8', 'ignore')
        thisAnnounce = unicode(announce_raw, errors='ignore')
    
        #sys.exit()
        announce.append(thisAnnounce)


    t = Table(out_arr, names = out_names)
    t.write(jobs_path, format='ascii', delimiter=';')
    #t.write(jobs_path.replace(".txt",".html"), format='html')

    tsimple = t
    tsimple.remove_column('announce')
    tsimple.write(abbriev_path, format='ascii', delimiter=';')
    
    f = open(announce_path, 'w')
    for item in announce:
        cleanedNewLines = item.replace("\n", "")
        jobAnnouncement = cleanedNewLines.replace("\t", "")+"\n"
        f.write(jobAnnouncement)
    f.close()

    return t