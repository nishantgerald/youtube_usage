import pandas as pd

def _is_subscribed(watch_history: pd.DataFrame, subscriptions: pd.Series) -> pd.DataFrame:
    """
    Check if the user is subscribed to the channel

    Args:
        wh_name: watch_history data
        sub_channel_title: subscriptions data

    Returns:
        True or False value depending on whether the channel was in the list of subscribed channels
    """
    watch_history['is_subscribed'] = watch_history['channel_name'].isin(subscriptions)
    return watch_history

def preprocess_watch_history(watch_history: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for watch history.

    Args:
        watch_history: Raw data.
    Returns:
        Preprocessed data, with time changed to YYYY-MM-DD hh:mm:sss format, and
        drop unnecessary columns.
    """
    watch_history["time"] = pd.to_datetime(watch_history["time"])
    watch_history["time"] = watch_history["time"].dt.strftime("%Y-%m-%d %H:%M:%S")
    for count,row in enumerate(watch_history["subtitles"]):
        try:
            watch_history.loc[watch_history.index[count],'channel_name']=row[0]['name']
        except:
            watch_history.loc[watch_history.index[count],'channel_name']="nan"
    #Remove the word 'Watched' at the beginning of each line in the `title`` column and not anywhere else
    watch_history['title'] = watch_history['title'].str.replace('Watched ', '')
    #Drop all rows where the title contains www.youtube.com
    watch_history = watch_history[~watch_history['title'].str.contains('www.youtube.com')]
    preprocessed_watch_history = watch_history.drop(['activityControls', 'header', 'products', 'subtitles', 'details', 'description'], axis=1)
    return preprocessed_watch_history

def preprocess_subscriptions(subscriptions: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses the data for subscriptions.

    Args:
        subscriptions: Raw data.
    Returns:
        Preprocessed data dropping all unnecessary columns.
    """
    preprocessed_subscriptions = subscriptions.drop(["Channel Id", "Channel Url"], axis=1)
    return preprocessed_subscriptions

def create_combined_table (watch_history: pd.DataFrame, subscriptions: pd.DataFrame) -> pd.DataFrame:
    """Merge the watch_history and subscriptions dataframes.

    Args:
        watch_history: Raw data.
        subscriptions: Raw data.

    Returns:
        Merged dataframes.
    """
    # Merge the dataframes
    preprocessed_watch_history = preprocess_watch_history(watch_history)
    preprocessed_subscriptions = preprocess_subscriptions(subscriptions)
    combined_table = _is_subscribed(preprocessed_watch_history,preprocessed_subscriptions['Channel Title'])
    combined_table.to_csv('data/04_feature/combined_table.csv', index=False)
    return combined_table