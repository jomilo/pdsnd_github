# Nanodegree Python Project - Explore US Bikeshare Data
# Author: Jobst Loeffler
# Date: August 2022

import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) time_filter - user input for time filter
    """
    city = ""
    month = ""
    day = ""

    print('\n')
    print('   __O ', '   ' , '   __O ', '   ' ,'   __O ')
    print(' _ \<_  ', '  ' , ' _ \<_  ', '  ' , ' _ \<_  ')
    print('(_)/(_)', '   ' , '(_)/(_)', '   ' , '(_)/(_)')
    print('Hello and WELCOME to BIKESHARE ANALYTICS!')
    print('\n')
    print('Let\'s get started and explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    flag = True
    while flag == True:
        city = input("Would you like to explore data for Chicago, New York City or Washington: ")
        city = city.lower()
        if city in CITY_DATA.keys():
            flag = False
        else:
            print("Enter one of these cities: Chicago, New York City or Washington!")

    # enter time filter criteria month, day, both or none
    flag = True
    input_strings = ['month', 'day', 'both', 'none']
    while flag == True:
        user_input = input("Would you like to filter the data for month, day, both or not at all. Type 'none' for no time filter: ")
        if user_input in input_strings:
            flag = False
        else:
            print("Enter one of these filter options: month, day, both or none")

    if(user_input == 'none'):
        print("No time filter wil be applied for " + city + " data.")
        month = 'all'
        day = 'all'

    if(user_input == 'month' or user_input == 'both'):
        # get user input for month (all, january, february, ... , june)
        flag = True
        while flag == True:
            month = input("Which month would you like to explore: e.g. March: ")
            month = month.lower()
            if (month in months) or (month == 'all'):
                flag = False
            else:
                print("Enter a valifd month name: data available for January through June!")

    if(user_input == "day" or user_input == 'both'):
        # get user input for day of week (all, monday, tuesday, ... sunday)
        flag = True
        while flag == True:
            day = input("Which day would you like to explore: e.g. Monday: ")
            day = day.lower()
            if (day in days) or (day == 'all'):
                flag = False
            else:
                print("Enter a valifd day name!")

    if (user_input == "month"):
        day = 'all'
    if (user_input == "day"):
        month = 'all'

    print('-'*40)
    return city, month, day, user_input


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

    # load data file into a dataframe
    df = pd. read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month == 'all' and day == 'all':
        print ("Will not do time filtering")
    else:
        if (month != 'all'):
            # use the index of the months list to get the corresponding int
            month = months.index(month) + 1
            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, time_filter):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        time_filter - (str) user input for time filter
    Returns:
        nothing (in function printing only)
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    month_name = months[popular_month - 1].title()
    print("Most popular month was: {} ".format(month_name), "(with time filter: {})".format(time_filter))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("Most popular day of week was: {} ".format(popular_day), "(with time filter: {})".format(time_filter))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular start time was: {} ".format(popular_hour), "(with time filter: {})".format(time_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, time_filter):
    """Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        time_filter - (str) user input for time filter
    Returns:
        nothing (in function printing only)
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count = df[df['Start Station'] == popular_start_station].count()[0]
    print("Most popular start station was: {} with count: {} ".format(popular_start_station, count), "(with time filter: {})".format(time_filter))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count = df[df['End Station'] == popular_end_station].count()[0]
    print("Most popular end station was: {} with count: {} ".format(popular_end_station, count), "(with time filter: {})".format(time_filter))

    # display most frequent combination of start station and end station trip
    most_popular_route = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    count = df.groupby('Start Station')['End Station'].value_counts().max()
    print("Most popular route was: {} with count: {}".format(most_popular_route, count), "(with time filter: {})".format(time_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, time_filter):
    """Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month and day
        time_filter - (str) user input for time filter
    Returns:
        nothing (in function printing only)
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time_secs = df['Trip Duration'].sum().item()
    print("Total travel time [seconds]: {}".format(total_travel_time_secs), "(with time filter: {})".format(time_filter))
    total_travel_time_dt = datetime.timedelta(seconds=total_travel_time_secs)
    print("Total travel time [days, hours:mins:secs]: {}".format(total_travel_time_dt), "(with time filter: {})".format(time_filter))


    # display mean travel time
    mean_travel_time_secs = int(df['Trip Duration'].mean())
    print("Mean travel time [seconds]: {}".format(mean_travel_time_secs), "(with time filter: {})".format(time_filter))
    mean_travel_time_dt = datetime.timedelta(seconds=mean_travel_time_secs)
    print("Mean travel time [days, hours:mins:secs]: {}".format(mean_travel_time_dt), "(with time filter: {})".format(time_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, time_filter, city):
    """Displays statistics on bikeshare users.

        Args:
            df - Pandas DataFrame containing city data filtered by month and day
            time_filter - (str) user input for time filter
            city - city information
        Returns:
            nothing (in function printing only)
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = len(df)
    print("User count: {}".format(user_count), "(with time filter: {})".format(time_filter))

    # Display counts of gender
    if city == 'chicago' or city == 'new york city':
        user_count_male = df[df['Gender'] == 'Male'].count()[0]
        user_count_female = df[df['Gender'] == 'Female'].count()[0]
        print("Male user count: {}".format(user_count_male), "(with time filter: {})".format(time_filter))
        print("Female user count: {}".format(user_count_female), "(with time filter: {})".format(time_filter))

    # Display earliest, most recent, and most common year of birth
    if city == 'chicago' or city == 'new york city':
        earliest_yob = df['Birth Year'].min()
        print("Earliest year of birth: {}".format(earliest_yob), "(with time filter: {})".format(time_filter))

        most_recent_yob = df['Birth Year'].max()
        print("Most recent year of birth: {}".format(most_recent_yob), "(with time filter: {})".format(time_filter))

        most_common_yob = df['Birth Year'].mode()[0]
        print("Most common year of birth: {}".format(most_common_yob), "(with time filter: {})".format(time_filter))

    # Display User type
    user_type_subscriber = df[df['User Type'] == 'Subscriber'].count()[0]
    user_type_customer = df[df['User Type'] == 'Customer'].count()[0]
    print("Subscriber count: {}".format(user_type_subscriber), "(with time filter: {})".format(time_filter))
    print("Customer count: {}".format(user_type_customer), "(with time filter: {})".format(time_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, city):
    """Displays individual trip data for the time filtered data.

        Args:
            df - Pandas DataFrame containing city data filtered by month and day
                city - city information
        Returns:
            nothing (in function printing only)
    """

    df_filtered = df.reset_index()
    i = 0
    while i < len(df_filtered.index):
        display_raw = input("\nWould you like to review individual trip data. Please type yes or no.\n")
        if display_raw.lower() == 'yes':
            j = 0
            while j < 5:
                print('   __O ')
                print(' _ \<_  ')
                print('(_)/(_)')
                print('Start Time: ', df_filtered.loc[i, 'Start Time'])
                print('End Time: ', df_filtered.loc[i, 'End Time'])
                print('Trip Duration [sec]: ', df_filtered.loc[i, 'Trip Duration'])
                print('Start Station in {}:'.format(city), df_filtered.loc[i, 'Start Station'])
                print('End Station in {}:'.format(city), df_filtered.loc[i, 'End Station'])
                print('User Type: ', df_filtered.loc[i, 'User Type'])
                if city != 'washington':
                    print('Gender: ', df_filtered.loc[i, 'Gender'])
                    print('Birth Year: ', df_filtered.loc[i, 'Birth Year'])
                print('\n')
                j += 1
                i += 1
        elif display_raw.lower() == 'no':
            break
        elif display_raw.lower() != 'yes' and display_raw.lower() != 'no':
            print("Please type yes or no.\n")

def main():
    while True:
        # load data according to filter criteria
        city, month, day, time_filter = get_filters()
        df = load_data(city, month, day)

        # Calculate descriptive statistics
        time_stats(df, time_filter)
        station_stats(df, time_filter)
        trip_duration_stats(df, time_filter)
        user_stats(df, time_filter, city)

        # Display individual trip data
        display_raw_data(df, city)

        # Restart or end program
        flag = True
        while flag:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                print("Let's continue ...")
                flag = False
            elif restart.lower() == 'no':
                print('\n')
#                print("Thanks for visiting Bikeshare Analytics. Hope to see you soon!")
                print('   __O ', '   ' , '   __O ', '   ' ,'   __O ')
                print(' _ \<_  ', '  ' , ' _ \<_  ', '  ' , ' _ \<_  ')
                print('(_)/(_)', '   ' , '(_)/(_)', '   ' , '(_)/(_)')
                print("Thanks for visiting BIKESHARE ANALYTICS. Hope to see you soon!\n")
                flag = False
                break
            else:
                print("Please type yes or no")
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
