#region import statements
import random
import datetime
import math
# import our own modules from utils child directory.
from utils import dict_to_sql_insert_str
from utils import name_surname_generator, generate_checked_in_or_out, generate_random_timestamp, generate_random_decimal_pricesum
from utils import write_to_file
#endregion

#region handle number of INSERT statements generated
# number of testcases viz. input statements per table
numberOfRooms = 20
# number of "grupp_bokningar"
numberOfRooms_gb = 3
# percentage of bookings that should be group bookings:
p_gr_b = 0.50
# number of bookings per group booking
bookings_per_groupb = math.floor(round((numberOfRooms)*p_gr_b)/numberOfRooms_gb) # 50 percent of the booking divided by number of group bookings rounded down.
#endregion

#region global values for auxiliary purposes
#region Store the generated primary key values for foreign key references
personal_ids = []
erbjudande_ids = []
faktura_ids = []
rum_ids = []
rum_typ_ids = []  # Has predefined room types
kund_ids = []
huvud_gast_ids = []
rum_pris_ids = []
grupp_bokning_ids = []
erbjudande_ids = []
middag_ids = []
forsaljning_ids = []
booking_ids = []

#endregion

#region Store output from value_for_grupp_bokning_reference for later referal for "faktura"
l_values_generated_gbokning_ref = []
int_current_call_from_factura = 0
l_calls_when_gbooking_not_null = []
#endregion

# fixed length list of number of bookings assigned to each group booking
bookings_added_per_groupb = [0] * numberOfRooms_gb

# a start date so we don't have different ones everywhere:
g_set_start_date = "2024-10-08"
#endregion

# TODO: see if these can be migrated to "utils", ugly and distracting to have them here...
#region AUXILIARY FUNCTIONS

# AUXILIARY TABLE FUNCTIONS:::

# returns fixed keys for entity but also returns populates dict.
def generate_all_rum_typ_dicts():
    n_of_room_types = 3
    room_type_ids = ["enkelrum", "dubbelrum", "familjerum"]
    room_type_max_people = [1, 2, 4]
    rum_typ_dicts = []
    for i in range(n_of_room_types):
        rum_typ_dicts.append(generate_rum_typ_dict(room_type_ids[i], room_type_max_people[i]))
    return room_type_ids, rum_typ_dicts

# Generate random date between today and a future date within a certain range (e.g., 30 days from today)
def generate_random_date(start_date, days_range):
    return start_date + datetime.timedelta(days=random.randint(0, days_range))

# Generate offer price start and end date
def generate_offer_startend_dates():
    today = datetime.date.today()
    offer_start = generate_random_date(today, 90)  # Random start date of offer within 90 days from today
    offer_end = offer_start + datetime.timedelta(days=random.randint(5, 14))  # Random end date of offer between 5-14 days after offer start
    return offer_start, offer_end

# Generate check-in and check-out dates
def generate_checkin_checkout_dates():
    today = datetime.date.today()
    checkin_date = generate_random_date(today, 30)  # Random check-in within 30 days from today
    checkout_date = checkin_date + datetime.timedelta(days=random.randint(1, 7))  # Random stay between 1-7 days
    return checkin_date, checkout_date

# generate price intervalls for each room based on it's roop type
def price_intervalls_per_room_type(room_type_id):
    if room_type_id == "enkelrum":
        return round(random.uniform(400.0, 550.0), 2)
    if room_type_id == "dubbelrum":
        return round(random.uniform(600.0, 950.0), 2)
    if room_type_id == "familjerum":
        return round(random.uniform(1000.0, 1400.0), 2)

# return "NULL" as reference to "grupp_bokning" in "bokning" when group has been filled
"""
def value_for_grupp_bokning_reference(grupp_bokning_ids):
    global bookings_added_per_groupb
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if bookings_added_per_groupb[grupp_bokning_ids-1] < 3:
            bookings_added_per_groupb[grupp_bokning_ids-1] += 1
            return grupp_bokning_ids
        else: return "NULL" # if it is filled return NULL.
    else: return "NULL"
"""
def value_for_grupp_bokning_reference(grupp_bokning_ids):
    global bookings_added_per_groupb
    global l_values_generated_gbokning_ref
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if bookings_added_per_groupb[grupp_bokning_ids-1] < 3:
            bookings_added_per_groupb[grupp_bokning_ids-1] += 1
            l_values_generated_gbokning_ref.append(str(grupp_bokning_ids))#save for faktura table.
            return grupp_bokning_ids
        else: 
            l_values_generated_gbokning_ref.append("NULL") #save for faktura table.
            return "NULL" # if it is filled return NULL.
    else: 
        l_values_generated_gbokning_ref.append("NULL") #save for faktura table.
        return "NULL" 
    
def populate_faktura_id_in_boking_queries(bokning_queries):
    for i in range(1, numberOfRooms_gb+1):
        if grupp_bokning_id_current != "NULL":
            bokning_queries[faktura_id] = "NULL"
        else: bokning_queries[faktura_id] = i
    return bokning_queries

# note, old code, might not work?
def value_for_grupp_bokning_reference_faktura():
    global int_current_call_from_factura
    global l_calls_when_gbooking_not_null
    # current grupp_bokning_id as per saved from corresponding program call to value_for_grupp_bokning_reference
    grupp_bokning_id_current = l_values_generated_gbokning_ref[int_current_call_from_factura]
    int_current_call_from_factura += 1 #increment so next call gives the right value.
    return grupp_bokning_id_current
### END OF AUXILIARY FUNCTIONS
#endregion

#region DICTIONARY GENERATORS
# to make data accesible but still editable in case of foreign key conflicts etc.
def generate_erbjudande_dict():
    # Generate random erbjudande values
    start_datum, slut_datum = generate_offer_startend_dates()  # Get random dates
    erbjudande_dict = {
        #NOTE:  discount to work by fixed deduction since this is test data. Normally this would be manually entered and used manually as well.
        #random.choice(rum_typ_ids),  # Room type ID must be "enkelrum", "familjerum", or "dubbelrum"
        'prisavdrag': round(random.uniform(100.0, 300.0), 2),  # Price per X deduction
        'villkor': 'PLACEHOLDER villkor',  # Placeholder condition
        'start_datum': start_datum,  
        'slut_datum': slut_datum  
    }
    return erbjudande_dict

def generate_personal_dict():
    # Generate random personal values
    name, surname = name_surname_generator()
    personal_dict = {
        'fornamn': name,
        'efternamn': surname,
        'roll': random.choice(['Receptionist', 'Manager', 'Cleaner'])  
    }
    return personal_dict

def generate_kund_dict():
    # Generate random values for the kund dictionary
    name, surname = name_surname_generator()
    kund_dict = {
        'fornamn': name,
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return kund_dict

def generate_huvud_gast_dict():
    # Generate random values for the huvud_gast dictionary
    name, surname = name_surname_generator()
    huvud_gast_dict = {
        'fornamn': name,  
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return huvud_gast_dict

# foreign keys used: rum_typ_ids, personal_ids
def generate_rum_dict():
    # Generate random values for the rum dictionary
    b_check_in, b_check_out = generate_checked_in_or_out() # gives either true of false on either one.
    rum_dict = {
        'rum_typ_id': random.choice(rum_typ_ids),  # Room type ID (e.g., "enkelrum", "familjerum", "dubbelrum")
        'personal_id': random.choice(personal_ids),  # Personal ID must exist in 'personal'
        'checked_in': b_check_in,  # Checked in (0 or 1)
        'checked_out': b_check_out  # Checked out (0 or 1)
    }
    return rum_dict

# ID is not auto increment here: has to be manually assigned.
def generate_rum_typ_dict(rum_typ_id_inp, max_antal_personer_inp):
    rum_typ_dict = {
        'rum_typ_id': rum_typ_id_inp,
        'max_antal_personer': max_antal_personer_inp
    }
    return rum_typ_dict

# foreign keys used: rum_typ_ids
def generate_rum_pris_dict():
    rum_typ_id = random.choice(rum_typ_ids)
    pris_per_natt = price_intervalls_per_room_type(rum_typ_id)  # TODO: old function
    pris_start_datum, pris_slut_datum = generate_offer_startend_dates() # TODO: old function
    
    rum_pris_dict = {
        'rum_typ_id': rum_typ_id,  
        'pris_per_natt': pris_per_natt,  
        'pris_start_datum': pris_start_datum,  
        'pris_slut_datum': pris_slut_datum  
    }
    
    return rum_pris_dict


# foreign keys used: grupp_bokning_ids
def generate_middag_dict():
    middag_dict = {
        'grupp_bokning_id': random.choice(grupp_bokning_ids),  
        'antal_personer': random.randint(1, 10),  
        'datum': "UPDATED LATER VIA MAIN"  # FIXME: Placeholder for date of the meal, updated later since dependent on bookings
    }
    return middag_dict


# foreign keys used: personal_ids
def generate_faktura_dict():
    faktura_dict = {
        'personal_id': random.choice(personal_ids),  
        'erbjudande_id': random.choice(erbjudande_ids),
        'grupp_bokning_id': "UPDATED LATER VIA MAIN"  # FIXME: updated later
    }
    return faktura_dict

# foreign keys used: rum_id, personal_id, faktura_id
def generate_forsaljning_dict():
    summa = generate_random_decimal_pricesum(50,500,2)
    datum = generate_random_date(g_set_start_date, 30)
    
    forsaljning_dict = {
        'rum_id': random.choice(rum_ids),
        'personal_id': random.choice(personal_ids),
        'faktura_id': random.choice(faktura_ids),
        'summa': summa,
        'datum': datum
    }
    return forsaljning_dict

# foreign keys used: rum_ids, kund_ids, huvud_gast_ids, personal_ids, grupp_bokning_ids
def generate_bokning_dict():
    checkin_date, checkout_date = generate_checkin_checkout_dates()  # Get random dates
    grupp_bokning_assigned_value = value_for_grupp_bokning_reference(random.choice(grupp_bokning_ids))  # Returns null or fk_grupp_bokning
    booking_timestamp = generate_random_timestamp(g_set_start_date, 30) 
    bokning_dict = {
        'rum_id': random.choice(rum_ids),  
        'kund_id': random.choice(kund_ids),  
        'huvud_gast_id': random.choice(huvud_gast_ids),  
        'personal_id': random.choice(personal_ids),  
        'rum_pris_id': random.choice(rum_pris_ids),  
        'grupp_bokning_id': grupp_bokning_assigned_value,  # Group booking ID, either an ID or NULL
        'faktura_id': "faktura_id",  # FIXME: Placeholder for faktura ID, fixed later, either ID or NULL, is NULL when group id has ID.
        'datum_incheck': checkin_date,  # Randomized check-in date
        'datum_utcheck': checkout_date,  # Randomized check-out date
        'booking_datum': generate_random_timestamp,  # Booking date, randomly generated
        'antal_gaster': random.randint(1, 4)  # Number of guests
    }
    return bokning_dict

def generate_grupp_bokning_dict(personal_ids):
    grupp_bokning_dict = {
        'personal_id': random.choice(personal_ids) 
    }
    return grupp_bokning_dict
#endregion

#region INPUT STATEMENT GENERATORS:::

def generate_rum_typ_insert(dict):
    return dict_to_sql_insert_str("rum_typ", dict)

def generate_erbjudande_insert(dict):
    return dict_to_sql_insert_str("erbjudande", dict)

def generate_personal_insert(dict):
    return dict_to_sql_insert_str("personal", dict)

def generate_kund_insert(dict):
    return dict_to_sql_insert_str("kund", dict)

def generate_huvud_gast_insert(dict):
    return dict_to_sql_insert_str("huvud_gast", dict)

def generate_rum_insert(dict):
    return dict_to_sql_insert_str("rum", dict)
    
def generate_rum_pris_insert(dict):
    return dict_to_sql_insert_str("rum_pris", dict)

def generate_middag_insert(dict):
    return dict_to_sql_insert_str("middag", dict)

def generate_faktura_insert(dict):
    return dict_to_sql_insert_str("faktura", dict)

def generate_bokning_insert(dict):
    return dict_to_sql_insert_str("bokning", dict)

def generate_grupp_bokning_insert(dict):
    return dict_to_sql_insert_str("grupp_bokning", dict)
#endregion



# FIXME: have not updated this part yet....
# made all dict functions 
def main():
    # global values with IDs so we can keep track of foreign IDs etc.
    global personal_ids, erbjudande_ids, faktura_ids, rum_ids, kund_ids, huvud_gast_ids, rum_pris_ids, grupp_bokning_ids, erbjudande_ids
    global middag_ids, forsaljning_ids, booking_ids, rum_typ_ids

    #region number of entities per entity-type, based on NumberOfRooms
    erbjudande_n = numberOfRooms/4 # 25% of number of rooms.
    personal_n = numberOfRooms/4 # 25% of number of rooms.
    huvud_gast_n = numberOfRooms # same as number of rooms, since same in number of bookings.
    kund_n = numberOfRooms # NOTE: for now keep the same, see if break or not.
    rum_pris_n = numberOfRooms # same as number of rooms.
    rum_n = numberOfRooms # same as number of rooms.
    faktura_n = numberOfRooms # same as number of rooms.
    grupp_boking_n = grupp_bokning_ids  # has different amount, see global value at start. # NOTE: move globals to here.
    middag_n = numberOfRooms_gb*2 # we thinks it's resonable that every group has two dinners. 
    forsaljning_n = numberOfRooms/4 # 25 % of number of rooms: only 25% of guests buy stuff and put on room bill.
    booking_n = numberOfRooms # same as number of rooms.
    #endregion


    #region generate all autoincrement primary ids as ref for foreign key etc.
    erbjudande_ids = list(range(1, erbjudande_n+1)) 
    personal_ids = list(range(1, personal_n+1)) 
    huvud_gast_ids = list(range(1, huvud_gast_n+1)) 
    kund_ids = list(range(1, kund_n+1)) 
    rum_pris_ids = list(range(1, rum_pris_n+1)) 
    rum_ids = list(range(1, rum_n+1)) 
    faktura_ids = list(range(1, faktura_n+1)) 
    grupp_bokning_ids = list(range(1, grupp_boking_n+1))
    middag_ids = list(range(1, middag_n+1)) 
    forsaljning_ids = list(range(1, forsaljning_n+1)) 
    booking_ids = list(range(1, booking_n+1)) 
    #endregion

    #array_keys = [personal_ids, erbjudande_ids, faktura_ids, rum_ids, kund_ids, huvud_gast_ids, rum_pris_ids, grupp_bokning_ids, erbjudande_ids]
    #dict_of_primary_keys = call_function(array_keys)

    #region Generate all the dictionaries.

    rum_typ_ids, l_rum_typ_dicts = generate_all_rum_typ_dicts() # auxiliary function handles creation of multiples of this - not quantity numberOfRooms
    l_erbjudande_dicts = [generate_erbjudande_dict() for _ in range(erbjudande_n)]
    l_personal_dicts = [generate_personal_dict() for _ in range(personal_n)]
    l_huvud_gast_dicts = [generate_huvud_gast_dict() for _ in range(huvud_gast_n)]
    l_kund_dicts = [generate_kund_dict() for _ in range(kund_n)]
    l_rum_pris_dicts = [generate_rum_pris_dict() for _ in range(rum_pris_n)]
    l_rum_dicts  = [generate_rum_dict() for _ in range(rum_n)]
    l_faktura_dicts = [generate_faktura_dict() for _ in range(faktura_n)]
    l_grupp_bokning_dicts = [generate_grupp_bokning_dict() for _ in range(grupp_boking_n)]
    l_middag_dicts = [generate_middag_dict() for _ in range(middag_n)]
    l_forsaljning_dicts = [generate_forsaljning_dict() for _ in range(forsaljning_n)]
    l_bokning_dicts = [generate_bokning_dict() for _ in range(booking_n)]
    #endregion

    #region TODO: update dictionaries with values:

    # TODO: update middag with date for dinner based on bookings:
    # functions like this:
    """ fetches the check_in and check_out DATE from l_booking_dicts that has a group booking,
        then creates a TIMESTAMP within that DATE interval and sets it to l_middag_dicts[datum]"""
    for _ in range(middag_n): 


    #  Populates faktura with group IDS where it should have it. NOTE: will probably break.
    # functions like this:
    # TODO: migrate this functionality to below function
    """ checks if a booking has a group_booking and if it has that, gives the ID to factura.grupp_bokning_id
        if it does have a group_booking_ID then it just assigns it with NULL instead"""
    for _ in range(faktura_n): l_faktura_dicts[grupp_bokning_id] = value_for_grupp_bokning_reference_faktura()
    #bokning_queries = populate_faktura_id_in_boking_queries(bokning_queries)

    # update bokning_dicts with factura dict AND update faktura_dicts.
    # functions like this:
    """ Check: if a booking has a group booking then it sets factura_id to NULL in bokning << UPDATES BOOKING *
                    AND updates factura with that group booking ID  << UPDATES FAKTURA * 
                        AND saves (list: l_factura_id_w_gb) which factura_id has a group booking assigned to it.
                else sets factura_id to an factura_id in bokning that doesn't (EXIST IN list: l_factura_id_w_gb)
                    have a group_booking assigned to it in a factura entity. """
    

    #endregion
    
    #region old code for generating queries, need to be revised before runtime!
    # Generate 'personal' table so we have IDs to reference
    personal_queries = [generate_personal_insert(personal_dicts(i)) for i in range(numberOfRooms)]

    # Generate 'erbjudande' table so we have IDs to reference
    erbjudande_queries = [generate_erbjudande_insert() for _ in range(numberOfRooms)]

    # Generate 'kund' table so we have IDs to reference
    kund_queries = [generate_kund_insert() for _ in range(numberOfRooms)]

    # Generate 'huvud_gast' table so we have IDs to reference
    huvud_gast_queries = [generate_huvud_gast_insert() for _ in range(numberOfRooms)]

    # Generate 'rum_pris' table so we have IDs to reference
    rum_pris_queries = [generate_rum_pris_insert() for _ in range(numberOfRooms)]

    # Generate 'rum' table so we have IDs to reference
    rum_queries = [generate_rum_insert() for _ in range(numberOfRooms)]

    # Generate 'faktura' table so we have IDs to reference
    faktura_queries = [generate_faktura_insert() for _ in range(numberOfRooms)]

    # Generate 'grupp_bokning' table so we have IDs to reference
    grupp_bokning_queries = [generate_grupp_bokning_insert() for _ in range(numberOfRooms_gb)]

    # Generate other queries
    bokning_queries = [generate_bokning_insert() for _ in range(numberOfRooms)]
    #endregion



    # Write to text files
    write_to_file('erbjudande_inserts.txt', erbjudande_queries)
    write_to_file('personal_inserts.txt', personal_queries)
    write_to_file('rum_typ_inserts.txt', rum_typ_queries)
    write_to_file('kund_inserts.txt', kund_queries)
    write_to_file('huvud_gast_inserts.txt', huvud_gast_queries)
    write_to_file('rum_pris_inserts.txt', rum_pris_queries)
    write_to_file('rum_inserts.txt', rum_queries)
    write_to_file('faktura_inserts.txt', faktura_queries)
    write_to_file('grupp_bokning_inserts.txt', grupp_bokning_queries)
    write_to_file('bokning_inserts.txt', bokning_queries)
    write_to_file('middag_inserts.txt', middag_queries)

if __name__ == '__main__':
    main()
