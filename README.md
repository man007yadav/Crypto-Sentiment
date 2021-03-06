# Crypto-Sentiment
 
## Results

We generate two plots - Number of messages per day and Avg Sentiment Polarity per day for the dates between May 1, 2021 to May 15, 2021. We see the following results from the plots.

### Num of Messages per day plot
![alt text](https://github.com/man007yadav/Crypto-Sentiment/blob/main/num_msgs.jpeg)

* **Num of Messages per day plot** - The number of messages per day are moderate except dates between May 8 and May 11. This event corresponds to Elon Musk joking about dogecoin on Saturday Night Live Show on May 7, 2021, which caused the prices of dogecoin to fall roughly 30 % of its value. I verified the same that there were messages where people were discussing about this event in the dataset messages.

### Sentiment Polarity per day plot
![alt text](https://github.com/man007yadav/Crypto-Sentiment/blob/main/sentiment.jpeg)

* **Avg Sentiment Polarity per day plot** - Similar to the Number of messages per day plot, we can see that after May 7 2021, the sentiment polarity goes down after the mentioned event caused the prices of crypto like dogecoin to tumble. This confirms that our plot is correct and able to identify events like these using just sentiment polrity scores.


## Documentation

For details of implementation refer to the comments in the script code.

1. **Libraries used**
   * spaCy - Used for Language Detection for English and Sentiment Polarity scores of messages.
   * plotly - Used to plot the Number of messages per day and Avg Sentiment Polarity per day plots.

2. **Files**
   * result.json - Data Export of text messages 
   * crypto_sentiment.py - Script to generate the plots

## Instructions to run

1. Install Python dependencies
```
  pip install -r requirements.txt
```

2. Run the script to generate the plots
```
 python crypto_sentiment.py
```
Plots are generated with name **sentiment.jpeg** and **num_msgs.jpeg**


