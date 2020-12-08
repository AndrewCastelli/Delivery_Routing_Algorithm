import data_parse

# Truck One Departs at start of day (8:00)
# in order to return to hub to do truck three deliveries
truck_one_departure_time = ['8:00:00']
truck_one_full_mileage = 0
truck_one_deliveries = []
truck_one_package_miles = []
# Truck Two Departs at 9:30 to account for
# 'will not arrive to depot until 9:05 am' packages
truck_two_departure_time = ['9:05:00']
truck_two_full_mileage = 0
truck_two_deliveries = []
truck_two_package_miles = []
# Truck Three Departs arbitrarily with remaining packages
# (as long as truck 1 deliveries are complete (9:19) )
truck_three_departure_time = ['10:30:00']
truck_three_full_mileage = 0
truck_three_deliveries = []
truck_three_package_miles = []

# ##################################################### #
# ----------------- Truck One Start ------------------- #

# O(N)
for idx, value in enumerate(data_parse.truck_one_inventory):
    # loop through indexed truck one inventory to set departure times
    data_parse.get_truck_one_inventory()[idx][9] = truck_one_departure_time[0]
    truck_one_deliveries.append(data_parse.get_truck_one_inventory()[idx])

# O(N^2)
for idx, adr in enumerate(truck_one_deliveries):
    # loop through indexed truck one delivery addresses,
    # when loop matches address file, append miles and id for incrementation
    for pkg_adr in data_parse.get_address():
        if adr[2] == pkg_adr[2]:
            truck_one_package_miles.append(adr[0])
            truck_one_deliveries[idx][1] = pkg_adr[0]

#                 \\ Path Truck One //
# Call greedy algorithm to determine path for truck one
data_parse.greedy_route(truck_one_deliveries, 1, 0)

# O(N)
for idx in range(len(data_parse.get_truck_one_vertices()) - 1):
    # Truck One Mileage
    truck_one_full_mileage = data_parse.increment_leg_distance(
                              int(data_parse.get_truck_one_vertices()[idx]),
                              int(data_parse.get_truck_one_vertices()[idx + 1]),
                              truck_one_full_mileage)
    # Get departure and delivery time for truck one packages
    deliver_package = data_parse.snapshot_current_time(data_parse.path_leg_distance(
                      int(data_parse.get_truck_one_vertices()[idx]),
                      int(data_parse.get_truck_one_vertices()[idx + 1])),
                      truck_one_departure_time)
    # Fill statuses for truck one deliveries
    data_parse.get_truck_one_full_list()[idx][10] = (str(deliver_package))
    data_parse.get_map().overwrite_value(int(data_parse.get_truck_one_full_list()[idx][0]),
                                         truck_one_deliveries)

# ------------------ Truck One End -------------------- #
# ##################################################### #
# ##################################################### #
# ----------------- Truck Two Start ------------------- #

# O(N)
for idx, value in enumerate(data_parse.truck_two_inventory):
    # loop through indexed truck two inventory to set departure times
    data_parse.truck_two_inventory[idx][9] = truck_two_departure_time[0]
    truck_two_deliveries.append(data_parse.truck_two_inventory[idx])

# O(N^2)
for idx, adr in enumerate(truck_two_deliveries):
    # loop through indexed truck one delivery addresses,
    # when loop matches address file, append miles and id
    for pkg_adr in data_parse.get_address():
        if adr[2] == pkg_adr[2]:
            truck_two_package_miles.append(adr[0])
            truck_two_deliveries[idx][1] = pkg_adr[0]

#                \\ Path Truck Two //
# Call greedy algorithm to determine path for truck two
data_parse.greedy_route(truck_two_deliveries, 2, 0)

# O(N)
for idx in range(len(data_parse.get_truck_two_vertices()) - 1):
    # Truck Two Mileage
    truck_two_full_mileage = data_parse.increment_leg_distance(
                              int(data_parse.get_truck_two_vertices()[idx]),
                              int(data_parse.get_truck_two_vertices()[idx + 1]),
                              truck_two_full_mileage)
    # Get truck two package timing and mileage
    deliver_package = data_parse.snapshot_current_time(data_parse.path_leg_distance(
                      int(data_parse.get_truck_two_vertices()[idx]),
                      int(data_parse.get_truck_two_vertices()[idx + 1])),
                      truck_two_departure_time)
    # Fill statuses
    data_parse.get_truck_two_full_list()[idx][10] = (str(deliver_package))
    data_parse.get_map().overwrite_value(int(data_parse.get_truck_two_full_list()[idx][0]),
                                         truck_two_deliveries)

# ------------------ Truck Two End -------------------- #
# ##################################################### #
# ##################################################### #
# ---------------- Truck Three Start ------------------ #

# O(N)
for idx, value in enumerate(data_parse.get_truck_three_inventory()):
    # loop through indexed truck three inventory to set departure times
    data_parse.get_truck_three_inventory()[idx][9] = truck_three_departure_time[0]
    truck_three_deliveries.append(data_parse.get_truck_three_inventory()[idx])

# O(N^2)
for idx, adr in enumerate(truck_three_deliveries):
    for pkg_adr in data_parse.get_address():
        if adr[2] == pkg_adr[2]:
            truck_three_package_miles.append(adr[0])
            truck_three_deliveries[idx][1] = pkg_adr[0]

#                \\ Path Truck Three //
# Call greedy algorithm to determine path for truck three
data_parse.greedy_route(truck_three_deliveries, 3, 0)

# O(N)
for idx in range(len(data_parse.get_truck_three_vertices()) - 1):
    # Truck Three Mileage
    truck_three_full_mileage = data_parse.increment_leg_distance(
                                int(data_parse.get_truck_three_vertices()[idx]),
                                int(data_parse.get_truck_three_vertices()[idx + 1]),
                                truck_three_full_mileage)
    # Get truck three package timing and mileage
    deliver_package = data_parse.snapshot_current_time(data_parse.path_leg_distance(
                                        int(data_parse.get_truck_three_vertices()[idx]),
                                        int(data_parse.get_truck_three_vertices()[idx + 1])),
                                        truck_three_departure_time)
    # Fill statuses
    data_parse.get_truck_three_full_list()[idx][10] = (str(deliver_package))
    data_parse.get_map().overwrite_value(int(data_parse.get_truck_three_full_list()[idx][0]),
                                         truck_three_deliveries)

# ------------------ Truck Three End ------------------ #
# ##################################################### #


# O(1)
def finalize_mileage():
    # Add mileage from each truck together to return total miles travelled by all trucks
    total_mileage = truck_one_full_mileage + \
                    truck_two_full_mileage + \
                    truck_three_full_mileage
    return total_mileage
