# Greedy Algorithm
I created this solution December, 2020 using Python v3.8 in the PyCharm IDE.
This exercise was done for *'Data Structures and Algorithms II – C950'* final performance assessment.

## Instructions
A parcel service needs to determine an efficient route and delivery distribution for their daily deliveries, because packages are not currently being consistently delivered by their promised deadline. Daily delivery route has two trucks, three drivers, and an average of 40 packages to deliver each day. Each package has specific criteria and delivery requirements.

Your task is to determine an algorithm, write code, and present a solution where all 40 packages (listed in the attached *“Package File”*) will be delivered on time while meeting each package’s requirements and keeping the **combined total distance traveled under 140 miles for both trucks**. The specific delivery locations are shown on the attached *“Salt Lake City Downtown Map”*, and distances to each location are given in the attached *"Distance Table.”* The intent is to use the program for this specific location and also for many other cities in each state where the parcel service has a presence. As such, you will need to include detailed comments to make your code easy to follow and to justify the decisions you made while writing your scripts.

*Keep in mind that the one should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed in the “Package File,” including what has been delivered and at what time the delivery occurred.*

## Assumptions
- [x] Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.

- [x] The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.

- [x] There are no collisions.

- [x] Two trucks and three drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.

- [x] Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed. 

- [x] The delivery and loading times are instantaneous, i.e., no time passes while at a delivery or when moving packages to a truck at the hub (that time is factored into the calculation of the average speed of the trucks).

- [x] There is up to one special note associated with a package.

- [x] The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S State St., Salt Lake City, UT 84111) until 10:20 a.m.

- [x] The distances provided in the Distance Table are equal regardless of the direction traveled.

- [x] The day ends when all 40 packages have been delivered.
