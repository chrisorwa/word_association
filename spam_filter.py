
#load required libraries
import json
import time
import numpy as np
import ushahidiv2 as ush
import pandas as pd

#data source
url = 'https://pheme.ushahidi.com/'

#authentication variables
user = 'chris@ihub.co.ke'
passwd = 'pheme2015'


#get messages
data = ush.get_messages(url,user,passwd)
df = pd.DataFrame(data, columns=['incident_id', 'message_from', 'message_to', 'message_date','message_text','locationlatitude','message_detail','parent_id','reporter_id','message_level','service_message_id','message_type','message_id','locationlongitude'])
d = df['message_text']


#get reports
reports = ush.get_all_reports(url)
r = reports['incidentdescription']

#Classification
vectoriser_training = CountVectorizer(min_df=1,stop_words='english',strip_accents='unicode')
t = time.time()
features = vectoriser_training.fit_transform(d) 
print "training text to word vector took", time.time()-t, "seconds"

#define levenstein function


#remove spam
def remove_spam(ushahidi_reports,messages):

    #define levenstein distance
	def LD(s,t):
		s = ' ' + s
    	t = ' ' + t
    	d = {}
    	S = len(s)
    	T = len(t)
    	for i in range(S):
        	d[i, 0] = i
    	for j in range (T):
        	d[0, j] = j
    	for j in range(1,T):
        	for i in range(1,S):
        		if s[i] == t[j]:
        			d[i, j] = d[i-1, j-1]
            	else:
                	d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)
    	return d[S-1, T-1]

    #calculate report mean/centroid value
	def centroid(ushahidi_reports):
		distances = []
		for a,i in enumerate(ushahidi_reports) :
			for b,j in enumerate(ushahidi_reports):
				if (a!=b and a-b>0):
					dist = LD(i,j)
					distances.append(dist)
		n = np.mean(distances)
		return n

    	#ignore message with low centroid value
    	accept = []
    	decline = []
    	for k,m in enumerate(messages):
    		for l,u in enumerate(ushahidi_reports):
    			m_dist = LD(m,u)
    			if(m_dist < centroid(ushahidi_reports)):
    				accept.append(k)
    			elif(m_dist > centroid(ushahidi_reports)):
    				decline.append(k)

    	return accept

spam = remove_spam(r,d)
print spam 



