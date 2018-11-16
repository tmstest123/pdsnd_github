import time
import pandas as pd
import numpy as np
import calendar as cal

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
    
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('Enter the name of the city (chicago, new york city or washington): ')
        
        #The user might be tempted to enter the proper capitalization 
        #but we need a lowercase capitalization for our dictionary lookup
        city = city.lower()
        
        #Check if city name is valid / data exists for the given city
        if city in CITY_DATA:
            #User has entered a valid city name
            break 
        else:
            print("Invalid or unknown city name. Please try it again.")

    # Get user input for month (all, january, february, ... , june)
    valid_month_input = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('Enter the name of the month (january, february, ...) or \'all\' for the whole year: ')
        
        #Same as city lowercase conversion
        month = month.lower()
        
        #Check if input is valid
        if month in valid_month_input:
            #User has entered a valid month
            break 
        else:
            print("Invalid month. Please try it again.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',  'sunday']
    while True:
        day = input('Enter the name of the day (monday, tuesday, ...) or \'all\' for the whole week: ')

        #Same as city lowercase conversion
        day = day.lower()

        #Check if input is valid
        if day in valid_day_of_week:
            #User has entered a valid day
            break 
        else:
            print("Invalid day of the week. Please try it again.")

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
    
    # Read CSV file
    df = pd.read_csv(CITY_DATA[city],index_col=0)
    
    #Convert set to dateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Add additional columns which we need later on    
    df['_month'] = df['Start Time'].dt.month
    df['_day_of_week'] = df['Start Time'].dt.weekday_name
    df['_start_hour'] = df['Start Time'].dt.hour
    df['_start_end_station'] = df['Start Station']+" - "+df['End Station']
    
    # Filter by month
    if month != "all":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        df = df[df['_month'] == months.index(month) + 1]

    # Filter by day of the week
    if day != "all":
        df = df[df['_day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month if month hasn't been restricted
    if len(df['_month'].unique()) > 1:
        most_common_month = cal.month_name[df['_month'].mode()[0]+1]
        print("Most common month: {}".format(most_common_month))

    # Display the most common day of week
    if len(df['_day_of_week'].unique()) > 1:
        most_common_day_of_week = df['_day_of_week'].mode()[0]
        print("Most common day of week: {}".format(most_common_day_of_week))

    # Display the most common start hour
    most_common_start_hour = df['_start_hour'].mode()[0]
    print("Most common start hour: {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("Most commonly used start station: {}".format(df['Start Station'].mode()[0]))

    # Display most commonly used end station
    print("Most commonly used end station: {}".format(df['End Station'].mode()[0]))

    # Display most frequent combination of start station and end station trip
    most_common_start_end_station = df['_start_end_station'].mode()[0]
    print("Most commonly used end start and end station trip: {}".format(most_common_start_end_station))

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print("Total travel time: {}".format(df['Trip Duration'].sum()))

    # Display mean travel time
    print("Mean travel time: {}".format(int(df['Trip Duration'].mean())))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Unique user types: {}".format(len(df['User Type'].unique())))

    # Display counts of gender
    if 'Gender' in df.index:
        print("Gender count: {}".format(len(df['Gender'].unique())))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.index:
        print("Earliest year of birth: {}".format(int(df['Birth Year'].min())))
        print("Most recent year of birth: {}".format(int(df['Birth Year'].max())))
        print("Most common year of birth: {}".format(int(df['Birth Year'].mode()[0])))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Prints the filtered raw data."""
    while True:
        display_raw_data = input('Would you like to see the raw data? (yes, no): ')
        if display_raw_data == 'no':
            print('-'*40)
            return
        elif display_raw_data == 'yes':
            break
        else:
            print("Invalid input. Please try it again.")
    
    #User want's to see the raw data
    i = 1
    for index, row in df.iterrows():
        print("+++++++++++{}+++++++++++".format(i))
        for column in row.index:
            #Skip rows which have have not been part of the original dataset
            if(column[0] != "_"):
                print("{}: {}".format(column, row[column]))
            
        if i % 5 == 0:            
            while True:
                display_more_data = input('Would you like to see more raw data? (yes, no): ')
                if display_more_data == 'no':
                    print('-'*40)
                    return
                elif display_more_data == 'yes':
                    break
                else:
                    print("Invalid input. Please try it again.")
        i += 1
    
    print('-'*40)
    
def main():
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
