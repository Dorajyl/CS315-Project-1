import pandas as pd
import glob

"""
Columns in original dataset:
    videoID: int unique ID for every video
    batch: str number/ID of batch that we collected data on
    saved: boolean value for if we saved or did not save a video
    creator: str username of poster
    sound: str sound used in the video
    likes: int number of likes in the video
    comments: int number of comments on the video
    saved: int number of times the video was saved
    shares: int number of times the video was shared
    views: int number of views the video has
    hashtags: list of hashtags tagged on the video

Outlining each function:

1. Taking a data set with the columns listed above: how many times does a hashtag appear, per batch. 
   
   I want to measure, per batch, how many times does the hashtag appear. In the end I want to use this 
   to measure how the occurrence of certain hashtags changes over time (aka over batch)
	
    Example: If we see 20 videos in each batch, I would want an analysis that shows how many times 
    the hashtags seen in the first batch are continued to be seen in the next batches as well. 

    This result should be in a dataset with the following columns:
        hashtag: str the hashtag (each unique hashtag should have a new row)
        batch:  str number/ID that we are tracking (each hashtag will have a row for each batch so 
                if there are three batches each hashtag will have three rows)
        videoIDs: list of videoIDs where the hashtag appeared per batch
        appeared: int number of times it appears 

    Are there any other columns necessary?

2. Taking the dataset from the columns listed at the start: how many times, for the videos that we 
   saved, do hashtags reappear. This should work like the function above but only for saved videos. 
   (Maybe merge both and have an input be a boolean value to see if we are testing saved or all). 
   
   I want to measure, per batch, how many times the hashtags, in the videos that we saved, continue 
   to appear in later batches. So for the first batch (which we would run first) it would just track 
   how many times the hashtags in the videos we saved appear. Then in the next batch it will continue
   to check those hashtags and add in any new hashtags on the videos we saved in that batch, and on 
   and on. 
   
   In the end I want to use this to measure the trend of how hashtag reoccurrence changes 
   based on the videos we saved.

3. Taking the dataset from the columns listed at the start: how many times to specific creators 
   reappear in each batch? This should work similarly as the first function but rather than hashtags
   we would be measuring creator reaccurance. 

Each of these functions should return a dataset.
"""

def hashtag_occurrence_per_batch(data):
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame(columns=['hashtag', 'batch', 'videoIDs', 'appeared'])

    # Iterate over each batch
    for batch_id, batch_data in data.groupby('batch'):
        hashtag_count = {}

        # Iterate over each row in the batch
        for _, row in batch_data.iterrows():
            hashtags = row['hashtag']
            for hashtag in hashtags:
                if hashtag not in hashtag_count:
                    hashtag_count[hashtag] = {'videoIDs': [], 'appeared': 0}
                hashtag_count[hashtag]['videoIDs'].append(row['videoID'])
                hashtag_count[hashtag]['appeared'] += 1

        # Add batch data to the result DataFrame
        for hashtag, count_data in hashtag_count.items():
            result_df = result_df.append({'hashtag': hashtag, 'batch': batch_id, 
                                          'videoIDs': count_data['videoIDs'], 'appeared': count_data['appeared']},
                                         ignore_index=True)

    return result_df

def hashtag_occurrence_for_saved_videos(data):
    # Filter the data to consider only saved videos
    saved_data = data[data['saved']]

    # Use the same logic as the previous function
    return hashtag_occurrence_per_batch(saved_data)

def creator_occurrence_per_batch(data):
    # Create an empty DataFrame to store the results
    result_df = pd.DataFrame(columns=['author', 'batch', 'videoIDs', 'appeared'])

    # Iterate over each batch
    for batch_id, batch_data in data.groupby('batch'):
        creator_count = {}

        # Iterate over each row in the batch
        for _, row in batch_data.iterrows():
            creator = row['author']
            if creator not in creator_count:
                creator_count[creator] = {'videoIDs': [], 'appeared': 0}
            creator_count[creator]['videoIDs'].append(row['videoID'])
            creator_count[creator]['appeared'] += 1

        # Add batch data to the result DataFrame
        for creator, count_data in creator_count.items():
            result_df = result_df.append({'author': creator, 'batch': batch_id, 
                                          'videoIDs': count_data['videoIDs'], 'appeared': count_data['appeared']},
                                         ignore_index=True)

    return result_df

def split_hashtags(row):
    return row.split(', ') if isinstance(row, str) else []

def initialize_functions(folder):
    # Get all CSV files from the specified folder
    file_list = glob.glob(f"{folder}/*.csv")

    # Concatenate all the dataframes from the list of files
    raw_data = pd.concat([pd.read_csv(file) for file in file_list], ignore_index=True)

    # Split the 'hashtags' column into a list
    raw_data['hashtag'] = raw_data['hashtag'].apply(split_hashtags)

    # Fille these columns in as blank for now
    raw_data["videoID"] = "N/A"
    raw_data["saved"] = True

    hashtag_occurrence = hashtag_occurrence_per_batch(raw_data)
    hashtag_saved = hashtag_occurrence_for_saved_videos(raw_data)
    creator_occurrence = creator_occurrence_per_batch(raw_data)

    hashtag_occurrence.to_csv("hashtag_occurrence.csv", index=False)
    hashtag_saved.to_csv("hashtag_saved.csv", index=False)
    creator_occurrence.to_csv("creator_occurrence.csv", index=False)

initialize_functions("data")