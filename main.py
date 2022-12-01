#Jared-Michael Torres
#Student ID: 000961916
#WGU-C950
#10/05/22
#The time complexity of the whole Parcel Service program runs in time complexity of O(n^2)

import packageDelivery

#main.py runs in time complexity of O(n)

def main():
    # Time Complexity: O(n)
    while True:
        print("\nEnter a # selection to view a package list:")
        print("[1] View a list of all packages.")
        print("[2] Check delivery status based on time.")
        print("[3] Total miles traveled to deliver packages.")
        print("[4] Quit!")
        response = input("Enter selection here>>> ")

        if response == str(1):
            # Time Complexity: O(n)
            packageDelivery.main(response)
            continue
        elif response == str(2):
            print("\n**Enter time in hh:mm::ss format using 24 hour time. ex. 1pm = 13:00:00")
            # Time Complexity: O(1)
            time = input("Enter time: ")
            packageDelivery.main(time)
            continue
        elif response == str(3):
            packageDelivery.main(response)
            continue
        elif response == str(4):
            exit()
        else:
            print("Please submit a valid response.")

main()