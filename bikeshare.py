import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(name):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello!! {} Let\'s explore some US bikeshare data!\n'.format(name))
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        print("Enter a Number Corresponding to the City from the Following Options:\n ")

        for index,city in enumerate(CITY_DATA):
            print(index+1,city.title())

        print("\n")
        try:
            city_index = int(input())
        except ValueError:
            print("\nPlease Enter a Valid Option.\n") 
            continue
        print("\n")

        if  (city_index< 0 or city_index > len(CITY_DATA)):
            print("Please Enter a Valid Option.\n") 
            continue
        else:
            city = list(CITY_DATA.keys())[city_index-1]
            print("You Chose {} as the City.\n".format(city.title()))
            print("Great let\'s move on!! \n")
            break

    # TO DO: get user input for month (all, january, february, ... , june)

    months = ['all','january','february','march','april','may','june']

    while True:
        print("Please Enter a Number to Select the month(s): \n")
        for index,option in enumerate(months):
            print(index+1,option.title())

        print("\n")
        try:
            month_index = int(input())
        except ValueError:
            print("\nPlease Enter a Valid Option.\n") 
            continue
        print("\n")

        if (month_index<0 or month_index>len(months)) :
            print("Please Enter a Valid Number.\n")
            continue
        else:
            month = months[month_index-1].lower()
            print("You Chose {} for the Month.\n".format(month.title()))
            print("We are Almost Done Here, We Just Need One Last Input From You {}.\n".format(name))
            break
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thrusday','friday','saturday','sunday']

    while True:
        print("Please Enter a Number to Select the Day(s) of the week: \n")
        for index,option in enumerate(days):
            print(index+1,option.title())

        print("\n")
        try:
            day_index = int(input())
        except ValueError:
            print("\nPlease Enter a Valid Option.\n") 
            continue
        print("\n")

        if (day_index < 0 or day_index > len(days)):
            print("Please Enter a Valid Number. \n")
            continue
        else:
            day = days[day_index-1].lower()
            print("You Chose {} for the Day.\n".format(day.title()))
            print("Alright!!, {} We are Done Here.".format(name))
            break
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
    print("Loading Data....... \n")

    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    #Converting to TimeStamp
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Travel Time for Each Entry
    df['travel time'] = (df['End Time'].subtract(df['Start Time'])).\
    apply(lambda x: round(x.seconds/60,3))

    #Extracting Month from 'Start Time', creating a new column 'month'
    df['month'] = df['Start Time'].dt.month

    #Extracting day of week from 'Start Time'
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    print("\n Here are the First Five Records of the Data Set You Selected.\n")
    records = 5
    print(df.head(records))
    while True:
        print("\n Would You Like See More Records of the Data Set? Please Enter Yes or No.\n")
        more_records = input()
        if more_records.lower() == 'yes':
            records+=5
            print(df.head(records))
        elif more_records.lower() == 'no':
            break
        else:
            print("\nPlease Enter a Valid Option.\n")
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The Most Common Month of Travel is: {}\n'.\
    format(calendar.month_name[df['month'].mode()[0]]))


    # TO DO: display the most common day of week
    print('The Most Common Day of the Week is: {}\n'.\
          format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour']= df['Start Time'].dt.hour
    print('The Most Common Hour of Travel is: {}:00\n'.
          format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The Most Commonly Used Start Station is: {}\n'.\
        format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print('The Most Commonly Used End Station is: {}\n'.\
        format(df['End Station'].mode()[0]))
    if (df['End Station'].mode()[0] == df['Start Station'].mode()[0]):
        print("Looks like {} is a very busy place.\n".\
              format(df['Start Station'].mode()[0]))
        
    # TO DO: display most frequent combination of start station and end station trip
    #Combining The Start And End Stations Separated by a Comma
    df['start end'] = df['Start Station'] +',' +df['End Station']
    start_end_combination = df['start end'].mode()[0].split(',')
    
    print('The Most Frequent Combination of Start And End Station is:\n \
{} as the Start Station\n \
and\n \
{} as the End Station'.\
format(start_end_combination[0],start_end_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df,city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('The Customers of {} Have Travelled a Total of {} Minutes.'.\
        format(city,df['travel time'].sum()))

    # TO DO: display mean travel time
    print('\nThe Customers of {} Have Travelled an Average of {} Minutes.'.\
        format(city,round(df['travel time'].mean(),3)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('The Following is the User Count for Different User Types: \n')
    print(df['User Type'].value_counts().to_frame(name='User Count'),'\n')
    
    if city != 'washington':
        # TO DO: Display counts of gender
        print('The Following is the Gender Count the Users: \n')
        print(df['Gender'].value_counts().to_frame(name='Gender Count'),'\n')

        # TO DO: Display earliest, most recent, and most common year of birth
        print('The Earliest Year of Birth for Our Customers is: {}\n'.\
            format(df['Birth Year'].min().astype(int)))

        print('The Most Recent Year of Birth for Our Customers is: {}\n'.\
            format(df['Birth Year'].max().astype(int)))

        print('The Most Common Year of Birth for Our Customers is: {}\n'.\
            format(df['Birth Year'].mode().astype(int)[0]))
    else:
        print("\nWe Do Not Have Any Information Regarding \
Gender of the Customers or their Year of Birth for Washington.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    '''A LOT OF HELP HAS BEEN TAKEN FROM STACKOVERFLOW FOR SYNTAX CLARIFICATION'''
    print("Hello!!, Welcome to bikeshare Data Analysis Platform.\n")
    print("What is your name?\n")
    name = input()
    try:
        if type(int(name)) == int:
            print("That is a strange name for a human.\n")
    except ValueError:
        name = name.title()
    while True:
        city, month, day = get_filters(name)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df,city)
        user_stats(df,city) 
        while True:
            restart = input('\n{}, Would you like to restart? Enter yes or no.\n'.format(name))
            if type(restart) != str or \
            (restart.lower() != 'yes' and restart.lower() != 'no'):
                                        print("\n{}, Pleae Enter a Valid Option.".format(name))
            else:
                break
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()