# Andrew Castelli // Student ID: #001488272

import datetime
from route import finalize_mileage
from data_parse import finalize_package_timelines, finalize_addresses


# O(1)
def display_single_pkg_info(i_d, adr, city, state, status):
    # Print package's current info
    print("Package ID: {}".format(i_d))
    print("Delivery Address: {} {}, {}".format(adr, city, state))
    print("Status: {}".format(status))


# O(4N^2)
def display_interface():
    # Display User Interface
    print("*********************************************************")
    print("                 All Packages Delivered                  ")
    print("                   Total Mileage: {}\n".format(int(finalize_mileage())))
    print("*********************************************************")
    print("------ Western Governors University Parcel Service ------")
    print("*********************************************************\n"
          "            To Display All Package Information         \n"
          "                        Enter: 1                     \n\n"
          "            For Individual Package Information         \n"
          "                        Enter: 2                         ")
    print("*********************************************************")
    print("                    Enter: x to Exit                     ")
    print("*********************************************************")

    user_key = input()
    while user_key != 'x':
        # O(N)
        if user_key == '1':
            # user enters 1: All Package Information
            print("-----------------------------")
            print("-- All Package Information --")
            print("-----------------------------")
            # Prompt user for start and end times of desired query
            print("Reminder: Please use military time to query.")
            user_end_time = input("Enter start of query window (HH:MM format): ")
            # add on :00 seconds to user inputs
            user_end_time = user_end_time + ':00'
            # Format times as timedelta for below comparisons
            (h, m, s) = user_end_time.split(':')
            query_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            time_slices = [10, 11, 12]
            check_slice = int(user_end_time[0:2])
            check_digit = int(user_end_time[0])
            if check_digit == 0 or check_slice in time_slices:
                if check_digit == 0:
                    p = user_end_time[1:5] + ' AM'
                elif check_slice == 10 or 11:
                    p = user_end_time[0:5] + ' AM'
                elif check_slice == 12:
                    p = user_end_time[0:5] + ' PM'
                print("All Package Progress from 8:00 AM to {}".format(p))
            elif check_slice > 12:
                p = "{}:{} PM".format(check_slice - 12, user_end_time[3:5])
                print("All Package Progress from 8:00 AM to {}".format(p))
            else:
                print("Error: {} is not a valid time query".format(user_end_time))
                display_interface()

            # O(N^2)
            for pkg in finalize_package_timelines():
                # Loop through finalized timeline list
                pkg_id = pkg[0]
                departure = pkg[1]
                delivery = pkg[2]
                # Compare departure/delivery times to query window to determine output
                (h, m, s) = departure.split(':')
                formatted_departure = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                (h, m, s) = delivery.split(':')
                formatted_delivery = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

                # display package departure/deliver stats for delivered packages
                if formatted_departure >= query_time:
                    status = "At Hub | Leaving on Truck at {} | Delivery Time: TBD".format(departure)
                    if formatted_departure == query_time:
                        status = "Just Left Hub | Delivery Time: TBD".format(departure)

                    print("Package ID: {}  | Status: {}".format(pkg_id, status))

                # display packages that departed Hub by query start time but not yet delivered
                elif formatted_departure <= query_time:
                    if formatted_delivery <= query_time:
                        departure = "Departed Hub at {}".format(departure)
                        status = "Delivered | Delivery Time: {}".format(delivery)
                        print("Package ID: {}  | {} | Status: {} ".format(pkg_id, departure, status))
                    elif formatted_delivery >= query_time:
                        departure = "Departed Hub at {}".format(departure)
                        status = "En Route | Delivery Time: TBD"
                        print("Package ID: {}  | {} | Status: {} ".format(pkg_id, departure, status))
                    else:
                        departure = 'Unknown'
                        status = 'TBD'
                        print("Package ID: {}  | Departure: {} | Status: {}".format(pkg_id, departure, status))

            exit()
    # ########################################################################################## #
        # O(N)
        elif user_key == '2':
            # user enters 2: Get individual package information
            print("------------------------------------")
            print("-- Individual Package Information --")
            print("------------------------------------")
            i_d = input("Enter Package ID: ")
            print("Reminder: Please use military time to denote period (AM/PM)")
            user_end_time = input("Enter time you wish to query (HH:MM format): ")
            user_end_time = user_end_time + ':00'
            (h, m, s) = user_end_time.split(':')
            query_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            for adr in finalize_addresses():
                if str(adr[0]) == i_d:
                    address = adr[1]
                    city = adr[2]
                    state = adr[3]
                    departure = adr[4]
                    delivery = adr[5]

                    (h, m, s) = departure.split(':')
                    formatted_departure = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                    (h, m, s) = delivery.split(':')
                    formatted_delivery = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

                    # O(N)
                    if formatted_departure >= query_time:
                        status = "Leaving on Truck at {}".format(departure)
                        display_single_pkg_info(i_d, address, city, state, status)

                    else:
                        if query_time < formatted_delivery:
                            status = "Not Yet Delivered, departed Hub at {} ".format(departure)
                            display_single_pkg_info(i_d, address, city, state, status)
                        else:
                            status = "Delivered at {}".format(delivery)
                            display_single_pkg_info(i_d, address, city, state, status)

            exit()

        elif user_key == 'x':
            exit()


if __name__ == '__main__':
    display_interface()
