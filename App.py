# Standard library imports
import logging
import re
import functools
import time
import requests
from time import gmtime, strftime
import datetime
import sys
import atexit



""" Function wrappers for main() """
# Continue running if there is an exception in the main method


def main():
    """
    Extract, Transform, Load
    Access each RentFaster.ca API page individually and store the results in MySQL.
    Built in data cleaning, duplicate entry checking, database error handling, and scheduling.
    """


    i = 0  # Loop counter

    keys = []  # Primary Key List

    j = 0

    while True:
        page = str(i)
        url = 'https://www.rentfaster.ca/api/search.json?keywords=&proximity_type=location-proximity&cur_page=' + \
            page + \
            '&beds=&type=&price_range_adv[from]=null&price_range_adv[to]=null&novacancy=0&city_id=2'
        data = requests.get(url).json()
        # There are multiple keys that can be accessed at this level, we want the listings data
        listings = data['listings']
        # We have reached the last page
        if len(listings) == 0:
            break
        # We have not reached the last page
        i += 1
        #print("Page " + page + " data obtained")

        for listing in listings:

            j += 1

            # Save Primary Key
            keys.append(listing['ref_id'])

            # # Add retrieval date
            # listing['retrieval_date'] = pd.to_datetime(
            #     'today').strftime("%m/%d/%Y")

            # Add position
            listing['position'] = "active"

            # --- Data Cleaning ---

            if 'sq_feet' in listing:
                listing['sq_feet'] = re.sub(
                    "[^0-9]", "", listing['sq_feet'])
            else:
                listing['sq_feet'] = ""

            if 'bedrooms' in listing:
                listing['bedrooms'] = listing['bedrooms'].replace(
                    'bachelor', "0")
            else:
                listing['bedrooms'] = "0"

            # Convert the list to a CSV string
            if 'utilities_included' in listing:


                if 'utilities_included' != False:
                    continue

                    listing['utilities_included'] = ",".join(
                        [str(x) for x in listing['utilities_included']])

                    # Remove whitespace
                    listing['utilities_included'] = listing['utilities_included'].strip(
                    )

                    # Remove trailing comma
                    listing['utilities_included'] = listing['utilities_included'].rstrip(
                        ',')
                # else:
                #     listing['utilities_included'] = ""

            if 'den' not in listing:
                listing['den'] = " "

            if 'baths' not in listing:
                listing['baths'] = " "

            if 'cats' not in listing:
                listing['cats'] = " "

            if 'dogs' not in listing:
                listing['dogs'] = " "

            # --- End Data Cleaning ---

            # db = Database.Database.db_config()[3]

            # Instantiate Object
            # rental = Rental.Rental(listing["ref_id"], listing["userId"], listing["id"], listing["title"], listing["price"], listing["type"],
            #                        listing["sq_feet"], listing["availability"], listing["avdate"], listing[
            #                            "location"], listing["rented"], listing["thumb"], listing["thumb2"],
            #                        listing["slide"], listing["link"], listing["latitude"], listing[
            #                            "longitude"], listing["marker"], listing["address"], listing["address_hidden"],
            #                        listing["city"], listing["province"], listing["intro"], listing[
            #                            "community"], listing["quadrant"], listing["phone"], listing["phone_2"],
            #                        listing["preferred_contact"], listing["website"], listing["email"], listing[
            #                            "status"], listing["bedrooms"], listing["den"], listing["baths"],
            #                        listing["cats"], listing["dogs"], listing['utilities_included'], listing['position'], listing["retrieval_date"])

        f = open("file.txt", "a",encoding="utf-8")
        print(listings, file=f)
        f.close()


    print(j)

# Enter the runtime in sys.argv[1]
if __name__ == "__main__":
    main()


