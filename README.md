# Real-time twitter hashtag analysis using PySpark Streaming

This project implements a distributed application using **PySpark Streaming** to perform real-time analysis of tweet data. The primary goal is to determine the most relevant hashtags currently trending within the **United States** by employing powerful sliding window operations.

The application connects to a continuous TCP socket data feed (simulated by `tweet_emitter.py`) and provides a fault-tolerant, scalable mechanism for analyzing high-velocity data streams.

-----

This project implements a distributed application using **PySpark Streaming** to perform real-time analysis of tweet data. The primary goal is to determine the most relevant hashtags currently trending within the **United States** by employing powerful sliding window operations.

The application connects to a continuous TCP socket data feed (simulated by `tweet_emitter.py`) and provides a fault-tolerant, scalable mechanism for analyzing high-velocity data streams.

-----

## Execution Guide

Running the project requires two separate terminals to be active simultaneously: one for the data emitter (server) and one for the Spark Streaming process (client/analysis).

### **Phase 1: Environment Setup (Terminal 1)**

Before running, ensure you have Python and `pip` installed, then follow these steps to configure the virtual environment:

1.  **Create and Activate the Virtual Environment:**

    ```bash
    python3 -m venv spark
    source spark/bin/activate
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### **Phase 2: Start the Tweet Emitter (Terminal 1)**

This process simulates the streaming data source. It **must be running** before launching the Spark script.

```bash
# Ensure you are in the activated environment
python3 tweet_emitter.py
```

*(You should see the message: `[+] listening on port 5000`)*

### **Phase 3: Run the Spark Streaming Analysis (Terminal 2)**

Open a **second terminal**, activate the virtual environment, and execute the analysis:

1.  **Activate the Virtual Environment (in Terminal 2):**

    ```bash
    source spark/bin/activate
    ```

2.  **Run the Analysis Script:**

    ```bash
    python3 hashtag_count.py
    ```

*(Once connected, in Terminal 1 you will see the tweet flow, and in Terminal 2 you will start seeing the sorted results every 10 seconds.)*

-----

## Reasoning for Obtained Data (Secondary Objective)

The objective of the practice is to determine the most relevant hashtags in real-time over the last 5 minutes, with results updating every 10 seconds. To achieve this, the implemented solution uses two fundamental concepts of Spark Streaming:

### 1. Data Filtering and Robustness

The first step is data source filtering. The `process_tweet` function ensures that:

  * Only tweets originating from the **United States** (`"country_code": "US"`) are processed, complying with the geographical requirement.
  * It safely handles parsing errors (`json.JSONDecodeError`) and the absence of fields (`place`, `entities`, `hashtags`), preventing crashes in the continuous stream execution.

### 2. Sliding Window Mechanism (`reduceByKeyAndWindow`)

The hashtag counts obtained in the `pprint()` output do not represent the total count since the start, nor just the count from the last 10 seconds, but the **total count of hashtag occurrences during the 5 minutes preceding the output.**

  * **Window Length (300s):** Defines the length of the history considered relevant (5 minutes).
  * **Sliding Interval (10s):** Defines the frequency at which a new result is calculated.

**Observed Dynamics:**

By using the inverse reduction function (`invFunc = lambda x, y: x - y`), the system implements **efficient incremental calculation**. In each 10-second interval:

1.  The counts of the new data entering the window are **added**.
2.  The counts of the older data leaving the window (tweets older than 5 minutes) are **subtracted**.

This dynamic allows the counts to accurately reflect current relevance. If a hashtag ceases to trend, its count will not disappear instantly; it will decrease progressively over the course of the 5 minutes until all the tweets containing it have left the analysis window. This confirms that the solution is measuring the **current trend**, and not just recent activity.

-----

## Project Files

  * `hashtag_count.py`: The main PySpark Streaming script with filtering, windowing, and sorting logic.
  * `tweet_emitter.py`: Python script provided to simulate the TCP data stream on port 5000.
  * `requirements.txt`: Necessary dependencies (`pyspark`, `colorama`).

