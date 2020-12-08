import csv
import datetime
from map import Map

# Address, distance, attribute info for 40 packages
package_tbl = 'WGUPS_Package_File.csv'
address_tbl = 'WGUPS_Address_Table.csv'
distance_tbl = 'WGUPS_Distance_Numbers.csv'

# using open() we can get the data to parse from each file
with open(distance_tbl) as dn:
    distance_table = list(csv.reader(dn))

with open(address_tbl) as at:
    # Get delivery addresses from csv
    address_table = list(csv.reader(at))
    # Nested truck inventory packages
    truck_one = []
    truck_two = []
    truck_three = []
    # Truck route ordered by ideal next stop
    truck_one_route_vertices = []
    truck_two_route_vertices = []
    truck_three_route_vertices = []

    # O(1)
    def path_leg_distance(i, j):
        # Use row/col indexing to current leg distance
        leg = distance_table[i][j]
        if leg == "":
            leg = distance_table[j][i]

        return float(leg)

    # O(1) Total Distance Function
    def increment_leg_distance(i, j, sum_of_legs):
        # use indexing to increment distance sum for algorithm comparison
        leg = distance_table[i][j]
        if leg == "":
            leg = distance_table[j][i]

        return sum_of_legs + float(leg)

    # 0(N)
    def snapshot_current_time(distance, truck_list):
        # get time of current moment for package in inventory
        # use miles / 18 mph (truck speed) to get time in hours
        snapshot = distance / 18
        snapshot_in_minutes = "{0:02.0f}:{1:02.0f}".format(*divmod(snapshot * 60, 60))
        final_time = "{}:00".format(snapshot_in_minutes)
        truck_list.append(final_time)
        total = datetime.timedelta()

        # use timedelta to return a time we can use comparison operators on
        for i in truck_list:
            (h, m, s) = i.split(':')
            total += datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
        return total

    # Greedy Algorithm - make optimal choice at each step (after each stop)
    # next vertex is assigned based on current vertex

    # O(N^2)
    def greedy_route(path, delivery_number, location_now):
        # estimate optimal path distance
        optimal_path = 15
        vertex = 0

        # for each location along delivery path
        for idx in path:
            # if new_length is less than old length,
            # set new length equal to distance between vertices
            leg_length = int(idx[1])
            if path_leg_distance(location_now, leg_length) <= optimal_path:
                optimal_path = path_leg_distance(location_now, leg_length)
                vertex = leg_length
        # for each location in delivery path
        for idx in path:
            # if leg is optimized, determine which truck to load
            if path_leg_distance(location_now, int(idx[1])) == optimal_path:
                # append index and vertex, use recursion to loop back for next leg
                if delivery_number == 1:
                    truck_one.append(idx)
                    truck_one_route_vertices.append(idx[1])
                    location_now = vertex
                    path.pop(path.index(idx))
                    greedy_route(path, 1, location_now)
                elif delivery_number == 2:
                    truck_two.append(idx)
                    truck_two_route_vertices.append(idx[1])
                    location_now = vertex
                    path.pop(path.index(idx))
                    greedy_route(path, 2, location_now)
                elif delivery_number == 3:
                    truck_three.append(idx)
                    truck_three_route_vertices.append(idx[1])
                    location_now = vertex
                    path.pop(path.index(idx))
                    greedy_route(path, 3, location_now)

    # O(N)
    def get_address():
        return address_table

    # First vertex is always 0 (hub)
    truck_one_route_vertices.insert(0, '0')
    truck_two_route_vertices.insert(0, '0')
    truck_three_route_vertices.insert(0, '0')

# Parse packages from WGU package file
with open(package_tbl) as pf:
    pkg_file = csv.reader(pf)

    # Construct Hash Map
    hash_map = Map()
    tt_deadline = '10:30:00'
    n_deadline = '9:00:00'
    group_deliveries = ['13', '15', '19', '29', '30', '31', '34', '37', '40']
    low_priority = ['21', '22', '23', '24', '26', '27']
    # Lists for main display reference
    pkg_time_list = []
    pkg_adr_list = []
    packages_on_trucks = []

    # Lists for three deliveries
    truck_one_inventory = []
    truck_two_inventory = []
    truck_three_inventory = []

    # O(1)
    # Functions to compare loads
    def get_truck_one_inventory():
        return truck_one_inventory

    def get_truck_two_inventory():
        return truck_two_inventory

    def get_truck_three_inventory():
        return truck_three_inventory

    # O(N)
    # for each row in our package info file
    for row in pkg_file:
        # Parse package attributes into variables
        pkg_id = row[0]
        pkg_address = row[1]
        pkg_city = row[2]
        pkg_state = row[3]
        pkg_zip = row[4]
        deadline = row[5]
        pkg_weight = row[6]
        pkg_note = row[7]
        departure_time = ''
        address_location = ''
        pkg_status = 'At hub'

        # place variables in an ordered list to hash
        hash_values = [pkg_id, address_location, pkg_address, pkg_city, pkg_state, pkg_zip, deadline, pkg_weight,
                       pkg_note, departure_time, pkg_status]

        # Truck One - Special Packages
        # check if deadline is 9am or package id is a group delivery required package
        if deadline == '9:00:00' or pkg_id in group_deliveries:
            # add it to lists if so
            truck_one_inventory.append(hash_values)
            packages_on_trucks.append(pkg_id)
        # check if 'must be delivered' is in packages special note
        elif "Must be delivered" in pkg_note:
            truck_one_inventory.append(hash_values)
            packages_on_trucks.append(pkg_id)

        # Truck Two - Special Packages
        # Packages delayed on flight, packages with Truck 2 Requirement
        # check if packages special note is delayed and deadline is 10:30:00 or truck 2 required
        elif 'Delayed' in pkg_note and deadline == '10:30:00' or 'truck 2' in pkg_note:
            truck_two_inventory.append(hash_values)
            packages_on_trucks.append(pkg_id)

        # Truck Three - Special Packages
        # Package with wrong address (corrected at 10:20am)
        # find package 9 and any other delayed packages with no deadlines
        elif "Wrong address" in pkg_note or 'Delayed' in pkg_note:
            truck_three_inventory.append(hash_values)
            packages_on_trucks.append(pkg_id)
        # check if package id is in low priority (no special requirements)
        elif pkg_id in low_priority:
            truck_three_inventory.append(hash_values)
            packages_on_trucks.append(pkg_id)

        # Load Remainder of inventory not yet assigned
        # if package id has no been added to a truck yet,
        if pkg_id not in packages_on_trucks:
            # determine which truck to add package to based on truck capacity and other trucks inventory size
            if len(truck_one_inventory) != 16 and len(truck_one_inventory) <= len(truck_three_inventory):
                truck_one_inventory.append(hash_values)
                packages_on_trucks.append(pkg_id)
            elif len(truck_two_inventory) != 16 and len(truck_two_inventory) < len(truck_one_inventory):
                truck_two_inventory.append(hash_values)
                packages_on_trucks.append(pkg_id)
            else:
                # if truck one and truck two are full, fill the rest into truck three
                if len(truck_three_inventory) != 16:
                    truck_three_inventory.append(hash_values)
                    packages_on_trucks.append(pkg_id)

        # Populate Hash Map values
        hash_map.insert(pkg_id, hash_values)

    # All simple - 0(1) Constant
    # Functions to pass updated values between files
    def get_truck_one_vertices():
        return truck_one_route_vertices

    def get_truck_one_full_list():
        return truck_one

    def get_truck_two_vertices():
        return truck_two_route_vertices

    def get_truck_two_full_list():
        return truck_two

    def get_truck_three_vertices():
        return truck_three_route_vertices

    def get_truck_three_full_list():
        return truck_three

    def get_map():
        return hash_map

    # O(N)
    def finalize_package_timelines():
        # nested list of index, departure and delivery time
        # loop through each trucks full list of deliveries
        for pkg in get_truck_one_full_list():
            # for each package, pull information for separate list
            pkg_time_list.append([int(pkg[0]), pkg[9], pkg[10]])
        for pkg in get_truck_two_full_list():
            pkg_time_list.append([int(pkg[0]), pkg[9], pkg[10]])
        for pkg in get_truck_three_full_list():
            pkg_time_list.append([int(pkg[0]), pkg[9], pkg[10]])

        # sort list before returning
        pkg_time_list.sort()
        return pkg_time_list

    # O(N)
    def finalize_addresses():
        # same process as finalize_package_timelines()
        # to get: index, address, city, state, index, departure, delivery time
        for pkg in get_truck_one_full_list():
            pkg_adr_list.append([int(pkg[0]), pkg[2], pkg[3], pkg[4], pkg[9], pkg[10]])
        for pkg in get_truck_two_full_list():
            pkg_adr_list.append([int(pkg[0]), pkg[2], pkg[3], pkg[4], pkg[9], pkg[10]])
        for pkg in get_truck_three_full_list():
            pkg_adr_list.append([int(pkg[0]), pkg[2], pkg[3], pkg[4], pkg[9], pkg[10]])

        return pkg_adr_list
