"""
Data cleaner for CS 315 raw data.

Goes through all files in raw data folder and does the following in order:
    1. Creates dataframe for file and sets necessary columns ("user" and "saved")
    2. Concatenates the files together into one master dataframe
    3. Creates "batchID" column which is string concatenation of "user", "run", "batch", "index"
    4. Orders columns and saves to CSV

Description of columns:
    "batchID": string concatenation of "user, "run", "batch", "index"
    "run": int representing 1-5 runs that webdriver preformed
    "batch": int representing batch 1-5 for each individual run
    "index": int representing index value of video per batch
    "saved": boolean True if video was saved, False otherwise
    "author": string representation of video's creator
    "likes": int number of likes
    "comments": int number of comments
    "shares": int number of shares
    "saves": int number of saves
    "music": string representation of sound used in video
    "hashtags": list of hashtags used in video

@author: fernandagonzalez
"""

import pandas as pd
import glob

# Get all raw data files from folder
raw_data = glob.glob("data/raw/*.csv")

# Going through every file in folder, creating and cleaning data, and appending to df
master = []
for file in raw_data:
    df = pd.read_csv(file)

    # Adding necessary columns
    df["filename"] = file
    df["user"] = str(file)[-12:-4]
    df["saved"] = "saved" in str(file)

    # Updating pre-set column "run"
    run = 0  # Initialize run to 0
    previous_batch = None

    for i, row in df.iterrows():
        if row["batch"] != previous_batch or row["index"] == 0:
            run += 1
        df.at[i, "run"] = run
        previous_batch = row["batch"]

    # Making values into ints for concatenation
    ints = ["batch", "run", "index", "likes", "comments", "shares", "saves"]
    df[ints] = df[ints].astype(int)

    # Creating "batchID" column which is string concatenation of "user, "run", "batch", "index"
    df["batchID"] = df[["user", "run", "batch", "index"]].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)


    master.append(df)

# Concatenating the files together into master dataframe
df = pd.concat(master, axis=0, ignore_index=True)

# Once all files are cleaned and concatenated:

# Splitting hashtag string value into list
df["hashtags"] = df["hashtag"].str.split(", ")

# Ordering column names
df = df[["batchID", "run", "batch", "index", "saved", "author", "likes", "comments", 
         "shares", "saves", "music", "hashtags"]]

# Saving to CSV
df.to_csv("data/master.csv", index=False)

