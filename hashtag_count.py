from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json

HOST = "localhost"
PORT = 5000
WINDOW_LENGTH = 300 # 5 minutes
SLIDE_INTERVAL = 10 # 10 seconds

def process_tweet(tweet):
    try: 
        tweet = json.loads(tweet)
        country_code = tweet.get('place', {}).get('country_code')
        if country_code!= "US":
            return []
        hashtags = tweet.get('entities', {}).get('hashtags', [])
        if hashtags:
            return [('#' + tag['text'].lower(), 1) for tag in hashtags]
    except json.JSONDecodeError:
        return []
    except Exception:
        return []
    return []

if __name__ == "__main__":
    sc = SparkContext("local[*]", "HashtagCount")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, SLIDE_INTERVAL)
    ssc.checkpoint("checkpoint")

    lines = ssc.socketTextStream(HOST, PORT)

    hastag_pairs = lines.flatMap(process_tweet)

    windowed_counts = hastag_pairs.reduceByKeyAndWindow(
        func=lambda x, y: x + y,
        invFunc=lambda x, y: x - y,
        windowDuration=WINDOW_LENGTH,
        slideDuration=SLIDE_INTERVAL
    )

    sorted_hashtags = windowed_counts.transform(
        lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False)
    )

    sorted_hashtags.pprint(10)

    ssc.start()
    ssc.awaitTermination()