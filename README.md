# Chrome Review Analyzer WebApp
Analyzing chrome reviews dataset to filter low ratings with reviews having positive sentiment  

## Steps  
### Gathering the required data  
As we only require ID, review, rating data from the dataset, we scrape these columns with low star ratings (<=2 stars) from the original dataset (as we need to gather review with low rating having positive sentiment) to a temp dataset for analysis

### Cleaning review data  
From the head of the data we saw the reviews are not clean i.e, with emojis etc, first we convert emojis into text using demoji module then perform cleaning operations like removing unwanted numbers, spaces etc from the reviews using re module  

### Gathering the sentiment  
for this we can use simple and powerful library textblob to gather polarity of the review text but since we need a strong polarity to verify the positive sentiment of review, we adjust the threshold to 0.5. So, that only true positive sentimental reviews will be getting positive labels  

### Arranging the data  
We then arrange the required data from these positively classified sentiment data with low rating from original data to the output  

### Deploying using streamlit  
we deploy the above using streamlit api with authentication and the live url is given below 
```
https://charan7799-chrome-review-analyzer-web-review-analyzer-wp-ad8ree.streamlitapp.com/  
```
#### Steps in the api  
As secrets.toml is not tracked, copy the contents of "secrets.toml" file to secrets page of streamlit api  

#### For testing the deployed app, enter the details below

username:```user_1```

password: ```streamlit123```

upload the reviews file as csv -> for testing you can use the file Reviews.CSV from this repo

verify the data  

click "Download as CSV" to download the full data with only these filtered reviews  
