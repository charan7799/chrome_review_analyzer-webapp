## Q2: There are times when a user writes Good, Nice App or anyother positive text, in the review and gives 1-star rating. Your goal is to identify the reviews where the semantics of review text does not match rating. Your goal is to identify such ratings where review text is good, but rating is negative, So that the support team can point this to users.
## Deploy it using - Flask/Streamlit etc and share the live link.

# chrome_review_analyzer-webapp
Analyzing chrome reviews dataset to filter low ratings with reviews having positive sentiment  

## Steps  
### Gathering the required data  
As we only require ID, review, rating data from the dataset, we scrape these columns with star rating=1 from the original dataset (as we need to gather positive sentimental review with low rating) to temp dataset req_data  

### Cleaning review data  
From the head of the data we saw the reviews are not clean i.e, with emojis etc, first we convert emojis into text using demoji module then perform cleaning operations like removing unwanted numbers, spaces etc from the reviews using re module  

### Gathering the sentiment  
for this we can use simple and powerful library textblob to gather polarity of the review text but since we need a strong polarity to verify the positive sentiment of review, we adjust the threshold to 0.5. So, that only true positive sentimental reviews will be getting positive labels  

### Arranging the data  
We then arrange the required data from these positively classified sentiment data with low rating from original data to the output  

### Deploying using streamlit  
we deploy the above using streamlit api with authentication and the live url is given below  
https://charan7799-chrome-review-analyzer-webapp-base-question-2-ne1rel.streamlitapp.com/  

#### steps in the api  
As secrets.toml is not tracked, copy the contents of "secrets.toml" file to secrets page of streamlit api  
enter the user details(user_1, "streamlit123")  
upload the review file as csv  
verify the data  
click "Download as CSV" to download the full data with only these filtered reviews  
