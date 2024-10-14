# utils/subgenerators.py
import random, os
from datetime import datetime, timedelta
from typing import List, Dict
#import 3rd party module to visualize tables:
from tabulate import tabulate

# source: https://en.wiktionary.org/wiki/Appendix:Swedish_given_names#The_most_common_given_names_in_Sweden_1890_-_2008
_names_male = ["Alexander", "Alf", "Allan", "Anders", "Andreas", "Anton", "Arne", "Arvid", "Axel", "Bengt", "Bertil", "Birger", "Björn", "Bo", "Bror", "Börje", "Carl", "Christer", "Christian", "Daniel", "David", "Einar", "Emanuel", "Emil", "Eric", "Erik", "Ernst", "Evert", "Folke", "Fredrik", "Georg", "Gunnar", "Gustaf", "Gustav", "Göran", "Gösta", "Hans", "Harald", "Harry", "Henrik", "Henry", "Håkan", "Ingemar", "Ingvar", "Ivar", "Jan", "Johan", "Johannes", "John", "Jonas", "Karl", "Kent", "Kjell", "Knut", "Kurt", "Lars", "Leif", "Lennart", "Magnus", "Marcus", "Martin", "Mats", "Mattias", "Michael", "Mikael", "Niklas", "Nils", "Olof", "Olov", "Oskar", "Ove", "Patrik", "Per", "Peter", "Ragnar", "Robert", "Roger", "Roland", "Rolf", "Rune", "Sebastian", "Simon", "Stefan", "Sten", "Stig", "Sven", "Thomas", "Tobias", "Tomas", "Tommy", "Torsten", "Ulf", "Valdemar", "Vilhelm", "William", "Åke"]
_names_female = ["Agneta", "Alice", "Amanda", "Anette", "Anita", "Ann", "Anna", "Annika", "Astrid", "Barbro", "Berit", "Birgit", "Birgitta", "Britt", "Camilla", "Carina", "Caroline", "Cecilia", "Charlotta", "Christina", "Edit", "Elin", "Elisabet", "Elisabeth", "Elsa", "Emma", "Ester", "Eva", "Greta", "Gun", "Gunborg", "Gunhild", "Gunilla", "Gunvor", "Hanna", "Helena", "Ida", "Inga", "Ingeborg", "Ingegerd", "Ingegärd", "Inger", "Ingrid", "Irene", "Jenny", "Johanna", "Julia", "Karin", "Karolina", "Katarina", "Kerstin", "Kristina", "Lena", "Linda", "Linnea", "Linnéa", "Lisa", "Louise", "Maj", "Malin", "Margareta", "Margit", "Maria", "Marie", "Matilda", "Monica", "Märta", "Rut", "Sara", "Signe", "Siv", "Sofia", "Sonja", "Susanne", "Svea", "Therese", "Ulla", "Ulrika", "Viktoria", "Viola", "Yvonne", "Åsa"]
_names = _names_male + _names_female
# source: https://en.wiktionary.org/wiki/Category:Swedish_surnames
_surnames = ["Abrahamsson", "Adamsberg", "Ahlman", "Alexandersson", "Alfvén", "Andersson", "André", "Andreasson", "Apell", "Arvidsson", "Ask", "Axelsson", "Backlund", "Backman", "Backström", "Bengtsson", "Berg", "Berggren", "Berglund", "Bergman", "Bergqvist", "Bergstrand", "Bergström", "Bergvall", "Bernadotte", "Berzelius", "Bildt", "Birgersson", "Björk", "Björklund", "Björkman", "Björn", "Blom", "Blomqvist", "Blomstrand", "Bolund", "Borg", "Boström", "Brovall", "Burman", "Bååth", "Bäcklund", "Bäckström", "Börjeson", "Carlsson", "Cederström", "Cronström", "Dahl", "Dahlberg", "Dahlbäck", "Dahlström", "Danielsson", "Davidsson", "Ehrling", "Ek", "Ekberg", "Ekdahl", "Ekelöf", "Ekerlid", "Ekholm", "Eklund", "Eklöf", "Ekström", "Eliasson", "Engberg", "Englund", "Engström", "Ericsson", "Eriksson", "Erlandsson", "Erlund", "Fagerlund", "Fallström", "Fjäll", "Fontelius", "Forsberg", "Forsman", "Forssell", "Fransson", "Fredriksson", "Friman", "Frisk", "Glad", "Grafström", "Granestrand", "Grönholm", "Grönroos", "Gucci", "Gunnarsson", "Gustafsson", "Gustavsson", "Göransson", "Hammare", "Hammarskjöld", "Hansson", "Haverling", "Hedborg", "Hedenskog", "Hedlund", "Hedman", "Helander", "Helenius", "Helin", "Hellström", "Henriksson", "Hermansson", "Hjelmqvist", "Holm", "Holmberg", "Holmgren", "Holmquist", "Holmström", "Hulth", "Hyltenstam", "Håkansson", "Hård", "Högberg", "Höglund", "Höxter", "Isaksson", "Ishizaki", "Ivarsson", "Jacobsson", "Jakobsson", "Jansson", "Johansson", "Johnson", "Johnsson", "Jonasson", "Jonsson", "Josefsson", "Jäderberg", "Jönsson", "Karlsson", "Kindstrand", "Kjellander", "Kjellberg", "Kjellström", "Kristersson", "Kvist", "Kvisth", "Kwist", "Lagerkvist", "Lagerlöf", "Larsdotter", "Larsson", "Leander", "Lenné", "Lind", "Lindberg", "Lindblad", "Lindblom", "Lindelöf", "Lindén", "Lindfors", "Lindgren", "Lindholm", "Lindqvist", "Lindroos", "Lindström", "Linnaeus", "Linné", "Ljungberg", "Ljungqvist", "Lundberg", "Lundgren", "Lundh", "Lundin", "Lundqvist", "Lundström", "Löfgren", "Magnusson", "Malin", "Malmquist", "Malmström", "Mankell", "Markström", "Martinsson", "Matsson", "Mattsson", "Månsson", "Mårtensson", "Nilsson", "Nobel", "Nobelius", "Norberg", "Nordin", "Nordquist", "Nordqvist", "Nordström", "Norén", "Nyberg", "Nylund", "Nyman", "Nyström", "Nåjde", "Olofsson", "Olsson", "Palm", "Palme", "Palmquist", "Palmqvist", "Parkstad", "Pehrson", "Pehrsson", "Person", "Persson", "Petersson", "Pettersson", "Pourmokhtari", "Quist", "Quisth", "Qvist", "Qvisth", "Qwist", "Rangström", "Rask", "Renström", "Ribbing", "Ringberg", "Roos", "Ros", "Rosberg", "Rosengren", "Rosenqvist", "Rothschild", "Rudbeck", "Rudolfsson", "Rydberg", "Rydbäck", "Rydkvist", "Rydqvist", "Rydstedt", "Rydström", "Rydvall", "Ryttberg", "Råberg", "Rådström", "Sahlin", "Saleh", "Samuelsson", "Sandberg", "Sandelin", "Sandell", "Sandström", "Schyman", "Sellström", "Sievert", "Sirén", "Sjöberg", "Sjöblom", "Sjögren", "Sjökvist", "Sjölund", "Sjöquist", "Sjöqvist", "Skarsgård", "Skog", "Skoglund", "Snellman", "Spahandelin", "Spjuth", "Spångberg", "Stare", "Staxäng", "Stenqvist", "Stenström", "Strand", "Strid", "Ström", "Strömberg", "Ståhl", "Ståhlbrand", "Sundberg", "Sundkvist", "Sundqvist", "Sundström", "Svanstedt", "Svanström", "Svedberg", "Svensson", "Svinhufvud", "Säfström", "Söder", "Söderberg", "Södergren", "Söderström", "Thunberg", "Thörnqvist", "Torvalds", "Tunberg", "Tungel", "Tungelfelt", "Tvilling", "Wahlroos", "Wahlström", "Wallander", "Wallin", "Westerberg", "Westerlund", "Westman", "Wickman", "Widforss", "Wiktorin", "Åberg", "Ågren", "Åhlström", "Åkerblom", "Åkerlund", "Åkerman", "Åkerström", "Åkesson", "Ångström", "Åslund", "Åström", "Ärlig", "Öberg", "Östberg", "Österberg", "Österman", "Östlund", "Östman"]

def _shuffle_list(l_ints: List[int]) -> List[int]:
    return random.sample(l_ints, len(l_ints))

def tabulate_print(l_dict2tabulate: List[Dict], table_name: str, context_str: str) -> None:
    header2print = "\n" + table_name + "  -  " + context_str
    print(header2print)
    print(tabulate(l_dict2tabulate, headers="keys"))

# TODO: this could be done a lot cleaner... old code from string handling and not dict handling.
def value_for_grupp_bokning_reference(grupp_bokning_ids, bookings_added_per_groupb, grupp_bokning_n):
    #global bookings_added_per_groupb
    #global l_values_generated_gbokning_ref
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if bookings_added_per_groupb[grupp_bokning_ids-1] < grupp_bokning_n:
            bookings_added_per_groupb[grupp_bokning_ids-1] += 1
            return grupp_bokning_ids, bookings_added_per_groupb
        else: 
            return "NULL", bookings_added_per_groupb  # if it is filled return NULL.
    else: 
        return "NULL", bookings_added_per_groupb  

def update_middag_dict_on_bookings(l_middag_dicts, l_bokning_dicts):
    for middag_dict in l_middag_dicts: 
        for bokning_dict in l_bokning_dicts:
            if bokning_dict['grupp_bokning_id'] == middag_dict['grupp_bokning_id']:
                checkin_f_b = bokning_dict['datum_incheck']
                checkout_f_b = bokning_dict['datum_utcheck']
                delta_timedelta = checkout_f_b - checkin_f_b # store the difference between the two
                random_delta_s = random.randint(0, int(delta_timedelta.total_seconds())) # random seconds within interval.
                random_timestamp_interval = checkin_f_b + timedelta(seconds=random_delta_s)
                middag_dict['datum'] = random_timestamp_interval
                break # no need to check more in bokning dict now that we found our match

# update bokning_dicts with factura dict AND update faktura_dicts.
    # functions like this:
    """ Check: if a booking has a group booking then it updates factura with that group booking ID  << UPDATES FAKTURA * 
                        AND saves (list: l_factura_id_w_gb) which factura_id has a group booking assigned to it.
                else sets factura_id to an factura_id in bokning that doesn't (EXIST IN list: l_factura_id_w_gb)
                    have a group_booking assigned to it in a factura entity. """
def update_bokning_and_faktura_for_grupp_bokning(l_bokning_dicts: List[Dict], l_faktura_dicts: List[Dict]) -> None:
        # NOTE: faktura_id in bokning_dict is always "NULL" before this function call
        # NOTE: grupp_bokning_ID in faktura_dict is always "NULL" before this function call
        l_factura_id_w_gb = [] # store which factura IDs have a group booking assigned
        for bokning_dict in l_bokning_dicts:
            # update factura_dict with the right group_id
            if bokning_dict['grupp_bokning_id'] != 'NULL':
                for faktura_dict in l_faktura_dicts:
                    if faktura_dict['grupp_bokning_id'] == 'NULL':
                        faktura_dict['grupp_bokning_id'] = bokning_dict['grupp_bokning_id']
                        l_factura_id_w_gb.append(faktura_dict['faktura_id']) #save this as to not assign it for booking without group.
                        break # break out of for loop since we now found what we were looking for.
            # update bokning_dict with non group booking assigned faktura_id when the booking isn't a group booking:
        # we need a new for loop for this to make sure the list is fully populated first:
        for bokning_dict in l_bokning_dicts:
            # update bokning_dict with the right faktura_id
            if bokning_dict['grupp_bokning_id'] == 'NULL':
                for faktura_dict in l_faktura_dicts:
                    if faktura_dict['faktura_id'] not in l_factura_id_w_gb:
                        bokning_dict['faktura_id'] = faktura_dict['faktura_id']
                        break # break out of for loop since we now found what we were looking for.

def update_faktura_for_erbjudande_id(l_faktura_dicts: List[Dict], fakt_w_erb_n: int):
    count_erbjudande = 0 # also works as index!
    max_w_erbjudande = len(l_faktura_dicts) - fakt_w_erb_n
    l_faktura_ids = [item['faktura_id'] for item in l_faktura_dicts]
    random_order_ids = _shuffle_list(l_faktura_ids) # shuffle them around to make it random!
    while count_erbjudande < max_w_erbjudande:
        for faktura in l_faktura_dicts:
            random_f_id = random_order_ids[count_erbjudande]
            if (faktura['erbjudande_id'] != 'NULL' and
            count_erbjudande < max_w_erbjudande and
            faktura['faktura_id'] == random_f_id):
                faktura['erbjudande_id'] = 'NULL'
                count_erbjudande += 1

#region check dates and make sure they're right:

# Helper function to generate a random datetime within a given range
def _random_date(start: datetime, end: datetime) -> datetime:
    """Generate a random datetime between `start` and `end`."""
    time_delta = end - start
    random_seconds = random.randint(0, int(time_delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

# Validation function to ensure generated dates follow the rules
def _validate_dates(erbjudande: Dict, pris: Dict, bokning: Dict, middag: Dict) -> bool:
    """Ensure generated dates are valid according to your rules."""
    # Check the offer period
    if not (erbjudande['start_datum'] <= bokning['bokning_datum'] <= erbjudande['slut_datum']):
        return False
    # Check the price period
    if not (pris['start_datum'] <= bokning['bokning_datum'] < pris['slut_datum']):
        return False
    # Check booking and check-in/out dates
    if not (bokning['bokning_datum'] <= bokning['datum_incheck'] < bokning['datum_utcheck']):
        return False
    # Check if the dinner date is within the check-in and check-out dates
    if not (bokning['datum_incheck'] <= middag['datum'] <= bokning['datum_utcheck']):
        return False
    
    return True

# Function to update date ranges for lists of dictionaries
def update_date_range(
    lower_limit: datetime, 
    upper_limit: datetime, 
    l_erbjudande_dict: List[Dict], 
    l_bokning_dict: List[Dict], 
    l_pris_dict: List[Dict], 
    l_middag_dict: List[Dict]
) -> None:
    """
    Updates the dates for the lists of dictionaries according to the specified rules:
    
    1. Erbjudande_t-start <= bokning_t-bookingDate <= erbjudande_t-slut
    2. Pris_t-start <= bokning_t-bookingDate < pris_t-slut
    3. Bokning_t-bokning_datum <= bokning_t-checkin_date < bokning_t-checkout_date
    4. Bokning_t-checkin_date <= middag_t-datum <= bokning_t-checkout_date
    """
    # Iterate over the lists safely, ensuring that shorter lists do not cause index errors
    for i in range(max(len(l_erbjudande_dict), len(l_bokning_dict), len(l_pris_dict), len(l_middag_dict))):
        # Safely get elements from each list, defaulting to empty dictionaries if out of range
        erbjudande = l_erbjudande_dict[i] if i < len(l_erbjudande_dict) else {}
        bokning = l_bokning_dict[i] if i < len(l_bokning_dict) else {}
        pris = l_pris_dict[i] if i < len(l_pris_dict) else {}
        middag = l_middag_dict[i] if i < len(l_middag_dict) else {}

        # Keep generating valid dates until all conditions are satisfied
        while True:
            # Generate random dates within the valid range
            erbjudande['start_datum'] = _random_date(lower_limit, upper_limit)
            erbjudande['slut_datum'] = _random_date(erbjudande['start_datum'], upper_limit)
            
            pris['start_datum'] = _random_date(lower_limit, upper_limit)
            pris['slut_datum'] = _random_date(pris['start_datum'], upper_limit)
            
            bokning['bokning_datum'] = _random_date(lower_limit, upper_limit)
            bokning['datum_incheck'] = _random_date(bokning['bokning_datum'], upper_limit)
            bokning['datum_utcheck'] = _random_date(bokning['datum_incheck'], upper_limit)
            
            middag['datum'] = _random_date(bokning['datum_incheck'], bokning['datum_utcheck'])
            
            # Validate the generated dates
            if _validate_dates(erbjudande, pris, bokning, middag):
                break

        # Update the lists with the newly generated dates
        if i < len(l_erbjudande_dict):
            l_erbjudande_dict[i] = erbjudande
        if i < len(l_bokning_dict):
            l_bokning_dict[i] = bokning
        if i < len(l_pris_dict):
            l_pris_dict[i] = pris
        if i < len(l_middag_dict):
            l_middag_dict[i] = middag

def change_key_name_in_l(dict_l: List[Dict], old_key_n: str, new_key_n: str) -> None:
    for my_dict in dict_l:
        my_dict[new_key_n] = my_dict.pop(old_key_n)

#endregion 

def conv_timestamp2datetime_l(l_x_dict: List[Dict], key_name: str) -> None:
    for dict in l_x_dict:
        print("DATATYPE IS:\t" + str(type(dict[key_name])))
        dict[key_name] = dict[key_name].replace(microsecond=0)

def conv_timestamp2date_l(l_x_dict: List[Dict], key_name: str) -> None:
    for dict in l_x_dict:
        dict[key_name] = dict[key_name].date()


def name_surname_generator() -> tuple[str, str]:
    name = random.choice(_names)  # First names
    surname = random.choice(_surnames)  # Last names
    return name, surname

def generate_checked_in_or_out() -> tuple[str, str]:
    b_checked_in = random.choice(["FALSE", "TRUE"])
    if b_checked_in == "FALSE":
        b_checked_out = "TRUE"
    else:
        b_checked_out = "FALSE"
    return b_checked_in, b_checked_out

def generate_random_timestamp(i_s_date: str, i_e_date_days: str) -> datetime:
    # Parse the input start date
    if isinstance(i_s_date, datetime):
        start_date = i_s_date
    else:
        start_date = datetime.strptime(i_s_date, "%Y-%m-%d")
    
    # Generate a random number of days between 0 and i_e_date_days
    
    random_days = random.randint(0, int(i_e_date_days))
    
    # Generate random time (hours, minutes, seconds, microseconds)
    # total number of seconds in a day: 24 * 60 * 60
    random_seconds_in_day = random.randint(0, 24 * 60 * 60)
    
    # Calculate the random timestamp by adding random_days and random time to start_date
    random_timestamp = start_date + timedelta(days=random_days, seconds=random_seconds_in_day)
    
    # Return the random timestamp
    return random_timestamp

# Generate random date between today and a future date within a certain range (e.g., 30 days from today)
def generate_random_date(start_date, days_range) -> datetime:
    # parse string to a datetime object
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Generate a random number of days and add it to start_date
    return start_date + timedelta(days=random.randint(0, days_range))

# Generate offer price start and end date
def generate_offer_startend_dates()-> tuple[datetime, datetime]:
    today = datetime.today()
    offer_start = generate_random_date(today, 90)  # Random start date of offer within 90 days from today
    offer_end = offer_start + timedelta(days=random.randint(5, 14))  # Random end date of offer between 5-14 days after offer start
    return offer_start, offer_end

# Generate check-in and check-out dates
def generate_checkin_checkout_dates() -> tuple[datetime, datetime]:
    today = datetime.today()
    checkin_date = generate_random_date(today, 30)  # Random check-in within 30 days from today
    checkout_date = checkin_date + timedelta(days=random.randint(1, 7))  # Random stay between 1-7 days
    return checkin_date, checkout_date

# e.g. input = 100.11, 500, 2
# e.g. output = 432.11
def generate_random_decimal_pricesum(l_limit, u_limit, n_of_dec_places: int) -> float:
    random_value = random.uniform(l_limit, u_limit)
    return round(random_value, n_of_dec_places)

# generate price intervalls for each room based on it's roop type
def price_intervalls_per_room_type(room_type_id: str) -> float:
    if room_type_id == "enkelrum":
        return round(random.uniform(400.0, 550.0), 2)
    if room_type_id == "dubbelrum":
        return round(random.uniform(600.0, 950.0), 2)
    if room_type_id == "familjerum":
        return round(random.uniform(1000.0, 1400.0), 2)

# write string to a created output directory with date and time of runtime as part of it's name.
def write_to_file(filename: str, queries: str) -> None:
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    folder_name = f"output_{current_time}"
    
    # Get the parent directory of the current directory
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the folder in the parent directory
    full_folder_path = os.path.join(parent_directory, folder_name)
    os.makedirs(full_folder_path, exist_ok=True)
    
    full_path = os.path.join(folder_name, filename)
    print(str(full_path))
    
    with open(full_path, 'w', encoding='utf-8') as file:
        for query in queries:
            file.write(query + '\n')
    
    print(f"Data written to {full_path}")