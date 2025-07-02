import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load JSONL file
with open('reliance_tweets.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Extract date and content
tweets = [{"date": tweet["date"], "content": tweet["content"]} for tweet in data]
df = pd.DataFrame(tweets)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Define keyword categories
positive_keywords = ['gain', 'bullish', 'surge', 'spike', 'deal', 'rally', 'strong', 'soar']
negative_keywords = ['fall', 'drop', 'bearish', 'loss', 'hit', 'dip', 'crash']
neutral_keywords  = ['flat', 'wait', 'waiting', 'stable', 'unchanged']

# Function for sentiment analysis
def analyze_sentiment(text):
    base_score = analyzer.polarity_scores(text)['compound']
    
    # Word-level adjustments
    adjustment = 0
    for word in text.lower().split():
        if word in positive_keywords:
            adjustment += 0.2
        elif word in negative_keywords:
            adjustment -= 0.2
        elif word in neutral_keywords:
            adjustment += 0  # explicitly prevent negative shift

    final_score = base_score + adjustment

    if final_score >= 0.02:
        return 'positive'
    elif final_score <= -0.02:
        return 'negative'
    else:
        return 'neutral'

# Apply sentiment analysis
df['sentiment'] = df['content'].apply(analyze_sentiment)

# Save to CSV
df.to_csv('reliance_tweets_with_sentiment.csv', index=False)

print("✅ Done! CSV with improved financial sentiment saved as 'reliance_tweets_with_sentiment.csv'.")
