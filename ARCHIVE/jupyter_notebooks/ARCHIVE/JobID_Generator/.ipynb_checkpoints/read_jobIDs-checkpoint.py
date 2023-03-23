#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os

os.chdir('/global/u1/j/joeschm')
os.system("sacct -u joeschm -X --format=jobid,jobname,state,start,end,timelimit,elapsed,nodelist -S 06/15/21-00:00:00 -p > test.txt")


# In[2]:


#ll


# In[ ]:





# In[3]:


file = open('test.txt', 'r')
read_content = file.read()
chunks = read_content.split('\n')

header = chunks[0].split('|')[:-1]           #header column for dataframe and drop empty '' at the end

jobs_df = pd.DataFrame(columns = header)
#print(chunks)

for string in chunks[1:-1]:  #run through list of entries omitting first entry which is the header and final entry which is blank
    entry = string.split('|')[:-1]           #drop empty '' at the end
    
    job_entry = pd.DataFrame([entry], columns = header) #create single job entry
    jobs_df = jobs_df.append(job_entry, ignore_index = True)  #append job entry to job dataframe


# In[4]:


#print(jobs_df)


# In[5]:


#jobs_df['JobID']


# In[ ]:





# In[6]:


GENE_path = '/global/homes/j/joeschm/GENE'
os.chdir(GENE_path)

col = ["JobID","Path"]
filepath_df = pd.jobs = pd.DataFrame(columns = col)

for filename in os.listdir(os.getcwd()):
    if filename.startswith("prob_"):
        prob_path = GENE_path + "/" + filename
        os.chdir(prob_path) #change into GENE prob directory to search for GENE.XXXX.out files
        
        #print("")
        #print(filename)
        
        for GENEfile in os.listdir(os.getcwd()):
            #scan through all files in GENE prob directory
            
            if GENEfile.startswith("GENE.") and GENEfile.endswith("out"):
                jobID = GENEfile[5:-4]  #get XXXX jobID in GENE.XXXX.out file
                #print(jobID)
                
                path_found = False           #reset filepath data dump for every new GENE.XXXX.out file
                
                #print(GENEfile)
                
                file = open(GENEfile, 'r')    #open text file
                text = file.read()            #read text file
                line_list = text.split('\n')  #split into list using newline

                for line in line_list:
                    line = line.replace(" ","")     #remove spaces from within lines
                    if 'SCANDIR' in line:           #if a line has 

                        for i in range(len(line)):  #scan through line character-by-character
                            if line[i] == '=':
                                data_path = line[i+1:]
                                path_found = True
                                break    #once the filepath is found exit the search 
                                
                        break          #break out of the list line search if 'SCANDIR' is present
                if not path_found:
                    data_path = False  #if no filepath is found just set it to False
                
                #print("HERE'S THE FILEPATH", data_path)
                #print("HERE'S THE JOBID", jobID)
                
                
                entry = pd.DataFrame([[jobID, data_path]], columns = col) #create single job entry
                filepath_df = filepath_df.append(entry, ignore_index = True)  #append job entry to job dataframe


# In[7]:


#print(filepath_df)


# In[8]:


jobs_df = filepath_df.set_index('JobID').combine_first(jobs_df.drop_duplicates().set_index('JobID')).reset_index() #fill in n0_global values according to kymin values
#jobs_df['n0_global'] = jobs_df.n0_global.astype(float) #convert from an object to a float


# In[9]:


print(jobs_df)



jobs_df.to_csv('test.csv', sep='\t')
print("CSV Converted, my guy")

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




