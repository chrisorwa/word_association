

'
R library for accessing Ushahidi V2 Platform
'

#load required libraries
library(RCurl)
library(RJSONIO)

#get all reports
get_all_incidents <-function(mapurl){
  
  #get data
  ext_url <-"api?task=incidents"
  resource <-paste(mapurl,ext_url,sep="")
  data <-getURL(resource)
  
  #parse data from JSON to list
  a = fromJSON(data)
  b = a$payload
  c = b$incidents
  
  #process data
  df = data.frame()
  for (index in 1:length(c)){
    data = c[index][[1]]
    incident_data = as.data.frame(t(as.matrix(data$incident)))
    df = rbind(df,incident_data)
  }
  
  #return data frame
  return(df)
}

#add categories to map
add_categories_to_map <-function(mapurl,categories){
  addedcats = c()
  return(addedcats)
}

#change categories list on Ushahidi report
change_report_categories <-function(mapurl,reportid,add=c(),removes=c(),removeall=FALSE){
  return()
}





