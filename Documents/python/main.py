import json
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load JSON file
with open('reliance_tweets.json', 'r') as file:
    data = [json.loads(line) for line in file]

# Extract date and content
tweets = [{"date": tweet["date"], "content": tweet["content"]} for tweet in data]

# Create DataFrame
df = pd.DataFrame(tweets)

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.02:
        return 'positive'
    elif score <= -0.02:
        return 'negative'
    else:
        return 'neutral'

# Apply sentiment analysis
df['sentiment'] = df['content'].apply(analyze_sentiment)

# Save to CSV
df.to_csv('reliance_tweets_with_sentiment.csv', index=False)

print("✅ Sentiment-added CSV created successfully!")
