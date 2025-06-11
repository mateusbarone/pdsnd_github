import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)

    #create list to evaluate users input

    city_values =['chicago', 'washington', 'new york city']
    month_values =['january', 'february', 'march','april', 'may', 'june', 'all']
    day_values =['monday', 'tuesday', 'wednesday','thursday', 'friday', 'saturday', 'sunday', 'all']
    filter_month_values =['yes', 'no']
    filter_day_values =['yes', 'no']
    city = month = day = filter_month = filter_day = 0

    # ask and evaluate users input

    while city not in city_values:
        city = input('Please enter a valid name of a city (chicago, washington, new york city) that you would like to have more information  ')
        city = city.lower()

    while filter_month not in filter_month_values:
        filter_month = input('Would you like to filter data by month? (yes/no)  ')
        filter_month = filter_month.lower()

    if filter_month == 'no':
        month= 'all'
    else:
        while month not in month_values:
            month = input('Please enter a valid name of a month (from january to june) that you would like to have more information  ')
            month = month.lower()

    while filter_day not in filter_day_values:
        filter_day = input('Would you like to filter data by day of the week? (yes/no)  ')
        filter_day = filter_day.lower() 

    if filter_day == 'no':
        day= 'all'
    else:
        while day not in day_values:
            day = input('Please enter a valid name of a day of the week that you would like to have more information  ')
            day = day.lower()



    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #calculating used columns to avoid redundancy
    df['hour'] = df['Start Time'].dt.hour
    # create a new column that concantenates both the star and ending stations to get the trajectory
    df['trajectory'] = df['Start Station'] + ' -> ' + df['End Station']
    # get the duration in minutes
    df['Trip Duration Minutes'] = df['Trip Duration'] / 60
    # filter by month if applicable.
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month =  months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_values =['January', 'February', 'March','April', 'May', 'June']


    # display the most common month
    # using the mode to get the number of the month and get the correspondent name 
    popular_month = df['month'].mode()[0]
    popular_month_name = month_values[popular_month-1]
    print ('Most popular month:', popular_month_name)


    # display the most common day of week
    # using the mode to get the name of the most popular weekday
    popular_weekday = df['day_of_week'].mode()[0]
    print ('Most popular day of the week:', popular_weekday)


    # display the most common start hour
    # again, using the mode and creating the column hour extracting it from the Start Time
    popular_hour = df['hour'].mode()[0]
    print ('Most popular hour of the day:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print ('Most popular start station:', popular_start_station)


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print ('Most popular end station:', popular_end_station)


    # display most frequent combination of start station and end station trip
    popular_trajectory = df['trajectory'].mode()[0]
    print ('Most popular trajectory:', popular_trajectory)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    
    

    # display total travel time by summing all trip durations
    total_travel_time = df['Trip Duration Minutes'].sum()
    print ('Total trip duration (minutes):', total_travel_time)



    # display mean travel time
    mean_travel_time = df['Trip Duration Minutes'].mean()
    print ('Mean trip duration (minutes):', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types using value_counts
    user_types = df['User Type'].value_counts()
    print ('Split of User Type:', user_types)

    # getting additional info from new york and washington
    if city != 'washington':
        # Display counts of gender using value_counts
        gender = df['Gender'].value_counts()
        print ('Split of Gender:', gender)

        # Display earliest, most recent, and most common year of birth
        popular_year_of_birth= df['Birth Year'].mode()[0]
        print ('Most popular Year of Birth:', popular_year_of_birth)
        earliest_year_of_birth = df['Birth Year'].min()
        print ('Earliest Year of Birth:', earliest_year_of_birth)
        latest_year_of_birth = df['Birth Year'].max()
        print ('Most recent Year of Birth:', latest_year_of_birth)

    else:
        print ('Unfortunately there is no available data on users gender and year of birth for the selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        #asking if user wants to see raw data
        raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if raw_data.lower() == 'yes':
            # resetting the initial df as it could have been filtered and modified by the previous functions.
            # Using an auxiliary variable for counting, to always go ahead and not repeat the rows of raw data.
            count_raw = 0
            raw_df = pd.read_csv(CITY_DATA[city])
            while True:
                print (raw_df.loc[count_raw:count_raw+4])
                count_raw += 5
                raw_data_continue = input('\nWould you like to see more 5 rows of raw data? Enter yes or no.\n')
                if raw_data_continue.lower() != 'yes':
                    break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
