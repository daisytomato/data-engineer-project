# Learnings 

## 1. learned how to migrate project from dbt -cloud to dbt-core :
    a. download project file from project settings on dbt cloud
    b. open Git repo and unzip download files using unzip *.zip
    c. pip install dbt-bigquerry , it is a dbt and bigquery adaptor.
    d. dbt init. basic settings of project. 
    e. find the profile.yml and make sure the profile value in dbt_project.yml is the same as that in the profile.yml
    f. dbt debug to test the connection
    g. dbt seed to materialize csv files
    h. dbt build to build models and they are now in bigquery. 
    i. have to add the newly added table into source.yml file
   