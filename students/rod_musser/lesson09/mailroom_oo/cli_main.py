#!/usr/bin/env python3
import sys
from donor_models import DonorCollection

welcome_prompt = "\n".join(("Welcome to the Local Charity Mail Room System",
                            "Please choose from the following options:",
                            "1 - Send a Thank You",
                            "2 - Create a Report",
                            "3 - Quit",
                            ">>> "))

donor_collection = DonorCollection()


def main():
    """
    Provides an menu for the user to select which action they would like to take.
    """
    while True:
        response = input(welcome_prompt)
        try:
            response = int(response)
        except ValueError:
            print("Input must be a number.  Please try again.")
            continue
        menu_selection = main_menu_items.get(response)
        if menu_selection is None:
            print("Not a valid option!")
        else:
            menu_selection()


def send_thank_you():
    """
    Asking this user to enter the name of a donor
    and prints out a thank you letter for the donation.

    If the donor does no exist in the donor database,
    it will add it to the donor database.

    If the user types 'list',
    it will list all the donors int eh donor database.
    """
    response = input("Please enter a full name: ")
    if response.lower() == "list":
        print(donor_collection.list_donors())
        send_thank_you()
    else:
        existing_donor_name = donor_collection.has_donor(response)
        if existing_donor_name is None:
            is_new_donor = input("Donor not found.  Is this a new donor? (y/n) ")
            if is_new_donor.lower() == 'n':
                send_thank_you()
                return
        else:
            # use existing donor name
            response = existing_donor_name
        need_amount = True
        while need_amount:
            amount = input("Please enter the donation amount: ")
            try:
                donor_collection.add_donation(response, amount)
            except ValueError as ve:
                print(ve)
                continue
            need_amount = False
            # print(get_letter_text(generate_letter_data(response)))


def print_report():
    """
    Prints a report list each donor's name, their total contributions, total number of gifts,
    and average gift amount
    """
    # print("Donor Name" + (' ' * 16) + ("| Total Given | Num Gifts | Avergage Gift"))
    # print("-" * 68)
    # row = "{name:<26s} ${total:=12.2f}  {num:10d} ${avg:14.2f}".format
    # for donor in get_report():
    #     print(row(name=donor[0], total=donor[1], num=donor[2], avg=donor[3]))


def exit_program():
    """
    Closes the program
    """
    print("You made a difference today.  Have a good one!")
    sys.exit()


# Main menu choices presented to the user.
main_menu_items = {
    1: send_thank_you,
    2: print_report,
    3: exit_program
}

if __name__ == "__main__":
    main()