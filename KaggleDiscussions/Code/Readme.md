The analysis of kaggle data is done 3 fold:
- api_request
- kaggle_data_filtering
- Kaggle Discussion Insight for Problems

## Step 1: api_request

We start with executing the python script *api_request.py* to extract data about the discussions happening on the kaggle website. This script sends api requests to the url endpoint "https://www.kaggle.com/topics/(topic_id).json", where topic_id refers to the id assigned by the kaggle developers for a particular discussion thread.

**Note**: We can only make 1000 requests at a time due to the server constraints.

The data is collected for every 1000 requests are collected in a JSON file type.

**Important Points**
1. In the below mentioned line of code, we need to increase the starting and ending values of the range function by 1000's. 
```
# range should be iterated for every 1000 requests starting from 1 to 75000. Now the there can be more than 75000 requests as well.
for i in range(45000, 46000):
    # sending requests to kaggle
    data = requests.get("https://www.kaggle.com/topics/" + str(i) + ".json")
```
2. In the same way the data collected for every 1000 requests was stored in JSON file format like 46000.json, 47000.json, .... etc. 
```
with open("C:\\Users\\srevann\\Desktop\\json_files\\46000.json", 'w') as outfile:
    json.dump(data_list, outfile)
```
These files can be stored in any suitable naming convention which would help the filtering stage **(kaggle_data_filtering)** explained in the next stage.

3. Out of all the requests, there will be some requests with status code 4xx and 5xx indicating that such requests have been removed by kaggle. Hence, I have only considered the statuses with code of 2xx.

## Step 2: kaggle_data_filtering

Second step is to filter the unwanted data extracted from the previous step. So in each iteration, the json file containing the entire data of every 1000 requests are opened and the data of the six columns required for the analysis is retained. Finally, we get one json file containing the data about the following:
- **id** of the discussion
- **competition** name
- **author** who started the discussion thread
- **date_time** as when the discussion thread was started
- **overview** about the discussion
- **comments** combined with the replies to the comments by the users participating in that particular discussion
- **votes** recieved for the particular discussion

One small change to be done in the *data_extraction.py* code in the line:
```
file_path = r'C:\\Users\\srevann\\Desktop\\json_files\\'
```
Here in the above line, please provide the path where you store the json files extracted by executing previous script to the variable **file_path**.

The output of this file <filename with link> was loaded to the **Microsoft Azure databricks** to perform data analysis.

It is sufficient if we run the script *data_extraction.py*. Here is the [code](../Code/kaggle_data_filtering/data_extraction.py) to be run.

## Step 3: Kaggle Discussion Insight for Problems

This script involves concepts of NLP to provide the statistics about the discussions happened on kaggle containing the keywords about the defects affecting the ML model. Further, what is the frequency of occurrence of each of the keywords considered for our analysis.

Load the python script onto the cloud and execute each step as we do in the python notebook.

The important step in this script is to change the keywords of the defect in the parameter "pattern" and run the query to analyze the trend. The code snippet is given below:

```
regexTokenizer = RegexTokenizer(inputCol = "refined_text", outputCol = "words", pattern = "overfit|underfit|missing values|imbalance|covariate shift|outlier|leakage|calibration|dataset shift|drift", gaps=False)
```
