import pandas as pd

def read_mindful_minutes():
    """Read the mindful minutes parquet file into a dataframe"""
    try:
        df = pd.read_parquet("mindful_minutes_data.parquet")
        return df
    except Exception as e:
        print("Error reading mindful_minutes_data.parquet:", e)
        return None

def print_first_n_rows(df, n=10):
    """Print the first n values for each column in the dataframe"""
    if df is not None:
        print("\nMindful Minutes Data - First 10 values per column:")
        for col in df.columns:
            print(f"\n{col}:")
            for val in df[col].head(n):
                print(f"  {val}")
    else:
        print("No data to display - dataframe is None")

def calculate_date_stats(df):
    """Calculate summary statistics for mindful minutes sessions, excluding sessions with duration less than 1 minute"""
    if df is None or df.empty:
        print("No data available for date statistics")
        return
    
    # Convert date strings to datetime
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    
    # Calculate session lengths in minutes
    df['session_length'] = (df['endDate'] - df['startDate']).dt.total_seconds() / 60

    # Exclude sessions with duration less than 1 minute
    valid_df = df[df['session_length'] >= 1]
    
    if valid_df.empty:
        print("No valid sessions with duration >= 1 minute")
        return

    # Calculate earliest and latest dates from valid sessions
    earliest_date = valid_df['startDate'].min()
    latest_date = valid_df['endDate'].max()
    
    print("\nDate Range Statistics (for sessions with duration >= 1 minute):")
    print(f"Earliest session: {earliest_date}")
    print(f"Latest session: {latest_date}")
    
    print("\nSession Length Statistics (minutes) for valid sessions:")
    print(valid_df['session_length'].describe())
    
    # Show distribution of session lengths
    print("\nSession Length Distribution (valid sessions):")
    print(pd.cut(valid_df['session_length'], 
                bins=[0, 5, 10, 15, 20, 30, 60, float('inf')],
                labels=['0-5', '5-10', '10-15', '15-20', '20-30', '30-60', '60+']
    ).value_counts().sort_index())

def unique_sessions_2024_stats(df):
    """
    Calculate and print statistics for unique sessions in 2024,
    excluding sessions with duration less than 1 minute.
    
    Assumes that a session is uniquely defined by its 'startDate' and 'endDate'.
    """
    if df is None or df.empty:
        print("No data available for statistics.")
        return

    # Convert start/end dates to datetime and compute session length in minutes
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    df['session_length'] = (df['endDate'] - df['startDate']).dt.total_seconds() / 60

    # Exclude sessions with duration less than 1 minute
    valid_df = df[df['session_length'] >= 1]

    # Filter sessions that started during 2024
    df2024 = valid_df[valid_df['startDate'].dt.year == 2024]

    # Get total count before deduplication
    count_total = len(df2024)

    # Remove duplicates based on 'startDate' and 'endDate'
    unique_df2024 = df2024.drop_duplicates(subset=['startDate', 'endDate'])

    # Count the number of unique sessions in 2024
    count_unique = len(unique_df2024)
    print("Number of total sessions in 2024 (>= 1 minute):", count_total)
    print("Number of unique sessions in 2024 (>= 1 minute):", count_unique)
    print("Number of duplicate sessions in 2024 (>= 1 minute):", count_total - count_unique)

    if count_unique > 0:
        print("\nUnique Session Duration Statistics (in minutes) for valid sessions:")
        print(unique_df2024['session_length'].describe())

        print("\nUnique Session Length Distribution (valid sessions):")
        distribution = pd.cut(
            unique_df2024['session_length'],
            bins=[0, 5, 10, 15, 20, 30, 60, float('inf')],
            labels=['0-5', '5-10', '10-15', '15-20', '20-30', '30-60', '60+']
        )
        print(distribution.value_counts().sort_index())

def print_last_10_unique_sessions_2024(df):
    """
    Filter and print the last 10 unique sessions in 2024 along with their start times,
    end times, and session durations (in minutes).

    A session is considered unique by its 'startDate' and 'endDate', and only sessions with a duration
    of at least 1 minute are considered.
    """
    if df is None or df.empty:
        print("No data available for sessions.")
        return

    # Convert start and end dates to datetime and compute session length in minutes
    df['startDate'] = pd.to_datetime(df['startDate'])
    df['endDate'] = pd.to_datetime(df['endDate'])
    df['session_length'] = (df['endDate'] - df['startDate']).dt.total_seconds() / 60

    # Exclude sessions with duration less than 1 minute
    valid_df = df[df['session_length'] >= 1]

    # Filter sessions that started during 2024
    df2024 = valid_df[valid_df['startDate'].dt.year == 2024]

    # Remove duplicates based on 'startDate' and 'endDate' to get unique sessions
    unique_df2024 = df2024.drop_duplicates(subset=['startDate', 'endDate'])

    if unique_df2024.empty:
        print("No unique sessions in 2024 with duration >= 1 minute.")
        return

    # Sort the unique sessions by startDate in descending order to get the most recent sessions first
    sorted_unique_df = unique_df2024.sort_values(by='startDate', ascending=False)

    # Get the last 10 unique sessions (i.e. the 10 most recent sessions)
    last_10 = sorted_unique_df.head(10)

    print("\nLast 10 unique sessions in 2024 (most recent sessions):")
    for i, row in enumerate(last_10.itertuples(), start=1):
        start_time = row.startDate.strftime("%Y-%m-%d %H:%M:%S")
        end_time = row.endDate.strftime("%Y-%m-%d %H:%M:%S")
        duration = row.session_length
        print(f"\nSession {i}:")
        print(f"  Start Time: {start_time}")
        print(f"  End Time  : {end_time}")
        print(f"  Duration  : {duration:.2f} minutes")

def main():
    df = read_mindful_minutes()
    # print_first_n_rows(df)
    # calculate_date_stats(df)
    unique_sessions_2024_stats(df)
    print_last_10_unique_sessions_2024(df)

if __name__ == "__main__":
    main()