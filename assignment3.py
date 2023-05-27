import matplotlib.pyplot as plt

def load_dataset():
    while True:
        file_name = input("Enter the dataset file name: ")
        try:
            content = read_file(file_name)
            header, data = process_dataset(content)
            return header, data
        except FileNotFoundError:
            print("File not found. Please try again.")
        except IOError:
            print("Error reading the file. Please try again.")
        except Exception as e:
            print("An error occurred: ", e)

def process_dataset(content):
    lines = content.split('\n')
    header = lines[0].split(',')
    data = []
    for line in lines[1:]:
        if line.strip():
            data.append(line.split(','))

    # Transpose the data to align the values with the corresponding header labels
    data = list(map(list, zip(*data)))

    return header, data

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        raise FileNotFoundError("File not found. Please try again.")
    except IOError:
        raise IOError("Error reading the file. Please try again.")
    except Exception as e:
        raise Exception("An error occurred: ", e)


def show_pie_chart(country_name, country_activities, activityList):
    # Create a pie chart
    plt.pie(country_activities, labels=activityList, autopct='%1.1f%%')
    plt.title(f"Breakdown of time spent by people in {country_name}")

    plt.show()
    
def show_bar_chart(top_10_sleep_data):
    sorted_sleep_data = dict(sorted(top_10_sleep_data.items(), key=lambda item: item[1]))  # Sort the dictionary in ascending order

    countries = list(sorted_sleep_data.keys())
    
    # Convert from string to integer
    durations_minutes = [int(duration) for duration in sorted_sleep_data.values()]
    
    # Convert minutes to hours
    durations_hours = [round(duration / 60.0, 2) for duration in durations_minutes]  
    
    plt.bar(countries, durations_hours)
    plt.xlabel('')
    plt.ylabel('Sleep Duration (hours)')
    plt.title('Where do people sleep the longest time')

    # Set y-axis range and ticks
    min_duration = 8.4
    max_duration = 9.4
    plt.ylim(min_duration, max_duration)
    tick_values = [round(x, 1) for x in generate_ticks(min_duration, max_duration, 0.2)]
    plt.yticks(tick_values)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    print("Bar chart opens in a new window. Close it to continue...")
    
    plt.show()

def generate_ticks(start, end, step):
    tick_values = []
    current = start
    while current <= end:
        tick_values.append(current)
        current += step
    return tick_values


def show_line_chart(activity_list, average_times):
    plt.plot(activity_list, average_times, marker='o', markersize=2)
    plt.xlabel('Activity')
    plt.ylabel('Time (minutes)')
    plt.title('Worldwide average time spent in different activities')
    plt.xticks(fontsize=8)
    plt.xticks(rotation=90)
    plt.yticks([0, 100, 200, 300, 400, 500])

    # Add big dots at each point
    plt.scatter(activity_list, average_times, color='red', s=5)

    plt.show()


def show_box_chart(data):
    plt.boxplot(data)
    plt.title("Variation in Paid-Work Time")
    plt.ylabel("Time (hours)")
    plt.show()

def get_country_data(country, header, data):
    try:
        index = header.index(country)
        return [int(row[index]) for row in data]
    except ValueError:
        print("Country not found in the dataset.")
        return []

def get_sleep_data(data):
    country_list = data[0]
    sleep_data = data[-3]
    
    # Combine country and sleep duration into a dictionary
    sleep_dict = dict(zip(country_list, sleep_data))

    # Sort the dictionary by sleep duration in descending order
    sorted_sleep_dict = dict(sorted(sleep_dict.items(), key=lambda item: item[1], reverse=True))

    # Extract top 10
    top_10_sleep_data = {}
    count = 0
    for key, value in sorted_sleep_dict.items():
        top_10_sleep_data[key] = value
        count += 1
        if count == 10:
            break
        
    return top_10_sleep_data


def get_average_activity_times(activityTimeSpent, header):
    # Extract the activity list from the header (excluding the first element)
    activity_list = header[1:]

    # Initialize an empty list to store the average times
    average_times = []

    # Iterate over each row in the activityTimeSpent data of all countries to calculate the avg of each activity
    for i in range(len(activityTimeSpent)):
        total = 0
        avg = 0

        # Iterate over current activities but with varies of time spent by different countries in data set.
        for j in range(len(activityTimeSpent[i])):
            total += int(activityTimeSpent[i][j])
        avg = total / len(activityTimeSpent[i])

        # Append the average time of current activity in this iteration to the list of average times 
        average_times.append(avg)

    return activity_list, average_times


def get_paid_work_time(data):
    paid_work_time = [int(row[-6]) // 60 for row in data[1:]]
    return paid_work_time


def display_main_menu():
    print("Main Menu:")
    print("(1) Time components")
    print("(2) Top 10 sleep lovers")
    print("(3) Average activity times")
    print("(4) Variation in paid-work time")
    print("(5) Exit the program")

def run_program(header, data):
    while True:
        countryList = data[0]
        activityList = header[1:]
        activityTimeSpent = data[1:]

        display_main_menu()

        choice = input("Enter your choice (1-5): ")
        if choice == '1':
            country = input("Enter the country name: ").title()       
    
             # Find the index of the selected country in the countryList
            if country in countryList:
                country_index = countryList.index(country)
                country_activities = []

                for activities in activityTimeSpent:
                    country_activities.append(activities[country_index])    
                show_pie_chart(country, country_activities, activityList)

            else:
                print("Country not found. Please enter a valid country name.")            
        elif choice == '2':
            sleep_data = get_sleep_data(data)
            print("Pie chart opens in a new window. Close it to continue...")
            show_bar_chart(sleep_data)
        elif choice == '3':
            activity_list, average_times = get_average_activity_times(activityTimeSpent, header)
            show_line_chart(activity_list, average_times)
        elif choice == '4':
            paid_work_time = get_paid_work_time(data)
            show_box_chart(paid_work_time)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


#------Main-----
header, data = load_dataset()

if data is not None:
    print("Data loading complete.")
else:
    print("No data loaded.")

run_program(header, data)

    
            
