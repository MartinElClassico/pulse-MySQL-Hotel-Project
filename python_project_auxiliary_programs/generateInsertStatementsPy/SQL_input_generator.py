#region import statements
import random
import math
# import our own modules from utils child directory.
from utils import dict_to_sql_insert_str # converts dictionary to sql formatted string
from utils import name_surname_generator, generate_checked_in_or_out, generate_random_timestamp, generate_random_decimal_pricesum, tabulate_print
from utils import write_to_file, generate_random_date, generate_offer_startend_dates, price_intervalls_per_room_type, generate_checkin_checkout_dates
from utils import update_middag_dict_on_bookings 
#endregion

#region global variables
# number of testcases viz. input statements per table
numberOfRooms = 20
# number of "grupp_bokningar"
grupp_bokning_n = 3
# percentage of bookings that should be group bookings:
p_gr_b = 0.50
# number of bookings per group booking
bookings_per_groupb = math.floor(round((numberOfRooms)*p_gr_b)/grupp_bokning_n) # percent of the booking divided by number of group bookings rounded down.

# Store the generated primary key values for foreign key references
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
bokning_ids = []

# Store output from value_for_grupp_bokning_reference for later referal for "faktura"
l_values_generated_gbokning_ref = []
int_current_call_from_factura = 0
l_calls_when_gbokning_not_null = []

# fixed length list of number of bookings assigned to each group booking
boknings_added_per_groupb = [0] * grupp_bokning_n

# a start date so we don't have different ones everywhere:
g_set_start_date = "2024-10-08"

#endregion

# TODO: see if these can be migrated to "utils", ugly and distracting to have them here...
#region AUXILIARY FUNCTIONS

# return "NULL" as reference to "grupp_bokning" in "bokning" when group has been filled
# TODO: DELETE THIS IF NO LONGER NEEDED.
"""
def value_for_grupp_bokning_reference(grupp_bokning_ids):
    global boknings_added_per_groupb
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if boknings_added_per_groupb[grupp_bokning_ids-1] < 3:
            boknings_added_per_groupb[grupp_bokning_ids-1] += 1
            return grupp_bokning_ids
        else: return "NULL" # if it is filled return NULL.
    else: return "NULL"
"""
def value_for_grupp_bokning_reference(grupp_bokning_ids):
    global boknings_added_per_groupb
    global l_values_generated_gbokning_ref
    shouldHaveGroup = random.randint(0, 1)# radomly decide if to assign NULL or to a group foreign ID.
    if shouldHaveGroup:
        if boknings_added_per_groupb[grupp_bokning_ids-1] < grupp_bokning_n:
            boknings_added_per_groupb[grupp_bokning_ids-1] += 1
            l_values_generated_gbokning_ref.append(str(grupp_bokning_ids))#save for faktura table.
            return grupp_bokning_ids
        else: 
            l_values_generated_gbokning_ref.append("NULL") #save for faktura table.
            return "NULL" # if it is filled return NULL.
    else: 
        l_values_generated_gbokning_ref.append("NULL") #save for faktura table.
        return "NULL" 
    
# TODO: DELETE THIS WHEN NEW VERSION WORKS!

def populate_faktura_id_in_boking_queries(bokning_queries):
    for i in range(1, numberOfRooms_gb+1):
        if grupp_bokning_id_current != "NULL":
            bokning_queries[faktura_id] = "NULL"
        else: bokning_queries[faktura_id] = i
    return bokning_queries

# TODO:, old code, might not work? move functionality to a new function!
def value_for_grupp_bokning_reference_faktura():
    global int_current_call_from_factura
    global l_calls_when_gbokning_not_null
    # current grupp_bokning_id as per saved from corresponding program call to value_for_grupp_bokning_reference
    grupp_bokning_id_current = l_values_generated_gbokning_ref[int_current_call_from_factura]
    int_current_call_from_factura += 1 #increment so next call gives the right value.
    return grupp_bokning_id_current
### END OF AUXILIARY FUNCTIONS
#endregion

#region DICTIONARY GENERATORS
# to make data accesible but still editable in case of foreign key conflicts etc.

# ID is not auto increment here: has to be manually assigned.
def generate_rum_typ_dict(p_id):
    max_antal_personer = 1 if p_id == "enkelrum" else 2 if p_id == "dubbelrum" else 4 if p_id == "familjerum" else 0
    rum_typ_dict = {
        'rum_typ_id': p_id,
        'max_antal_personer': max_antal_personer
    }
    return rum_typ_dict

def generate_erbjudande_dict(p_id):
    # Generate random erbjudande values
    start_datum, slut_datum = generate_offer_startend_dates()  # Get random dates
    erbjudande_dict = {
        #NOTE:  discount to work by fixed deduction since this is test data. Normally this would be manually entered and used manually as well.
        #random.choice(rum_typ_ids),  # Room type ID must be "enkelrum", "familjerum", or "dubbelrum"
        'erbjudande_id': p_id,
        'prisavdrag': round(random.uniform(100.0, 300.0), 2),  # Price per X deduction
        'villkor': 'PLACEHOLDER villkor',  # Placeholder condition
        'start_datum': start_datum,  
        'slut_datum': slut_datum  
    }
    return erbjudande_dict

def generate_personal_dict(p_id):
    # Generate random personal values
    name, surname = name_surname_generator()
    personal_dict = {
        'personal_id': p_id,
        'fornamn': name,
        'efternamn': surname,
        'roll': random.choice(['Receptionist', 'Manager', 'Cleaner'])  
    }
    return personal_dict

def generate_kund_dict(p_id):
    # Generate random values for the kund dictionary
    name, surname = name_surname_generator()
    kund_dict = {
        'kund_id': p_id,
        'fornamn': name,
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return kund_dict

def generate_huvud_gast_dict(p_id):
    # Generate random values for the huvud_gast dictionary
    name, surname = name_surname_generator()
    huvud_gast_dict = {
        'huvud_gast_id': p_id,
        'fornamn': name,  
        'efternamn': surname, 
        'mejl_address': '{}@example.com'.format(random.randint(1000, 9999)),  
        'telefon_nummer': '+46{}'.format(random.randint(700000000, 799999999))  
    }
    return huvud_gast_dict

# foreign keys used: rum_typ_ids, personal_ids
def generate_rum_dict(p_id):
    # Generate random values for the rum dictionary
    b_check_in, b_check_out = generate_checked_in_or_out() # gives either true of false on either one.
    rum_dict = {
        'rum_id': p_id,
        'rum_typ_id': random.choice(rum_typ_ids),  # Room type ID (e.g., "enkelrum", "familjerum", "dubbelrum")
        'personal_id': random.choice(personal_ids),  # Personal ID must exist in 'personal'
        'checked_in': b_check_in,  # Checked in (0 or 1)
        'checked_out': b_check_out  # Checked out (0 or 1)
    }
    return rum_dict

# foreign keys used: rum_typ_ids
def generate_rum_pris_dict(p_id):
    rum_typ_id = random.choice(rum_typ_ids)
    pris_per_natt = price_intervalls_per_room_type(rum_typ_id)  # TODO: old function
    pris_start_datum, pris_slut_datum = generate_offer_startend_dates() # TODO: old function
    
    rum_pris_dict = {
        'rum_pris_id': p_id,
        'rum_typ_id': rum_typ_id,  
        'pris_per_natt': pris_per_natt,  
        'pris_start_datum': pris_start_datum,  
        'pris_slut_datum': pris_slut_datum  
    }
    
    return rum_pris_dict

# foreign keys used: grupp_bokning_ids
def generate_middag_dict(p_id):
    middag_dict = {
        'middag_id': p_id,
        'grupp_bokning_id': random.choice(grupp_bokning_ids),  # always has to have grupp_bokning_id to exist
        'antal_personer': random.randint(1, 10),  
        'datum': "UPDATED LATER VIA MAIN"  # FIXME: Placeholder for date of the meal, updated later since dependent on bookings
    }
    return middag_dict

# foreign keys used: personal_ids
def generate_faktura_dict(p_id):
    faktura_dict = {
        'faktura_id': p_id,
        'personal_id': random.choice(personal_ids),  
        'erbjudande_id': random.choice(erbjudande_ids),
        'grupp_bokning_id': "UPDATED LATER VIA MAIN"  # FIXME: updated later via main, depends on grupp_bokning
    }
    return faktura_dict

# foreign keys used: rum_id, personal_id, faktura_id
def generate_forsaljning_dict(p_id):
    summa = generate_random_decimal_pricesum(50,500,2)
    datum = generate_random_date(g_set_start_date, 30)
    
    forsaljning_dict = {
        'forsaljning_id': p_id,
        'rum_id': random.choice(rum_ids),
        'personal_id': random.choice(personal_ids),
        'faktura_id': random.choice(faktura_ids),
        'summa': summa,
        'datum': datum
    }
    return forsaljning_dict

# foreign keys used: rum_ids, kund_ids, huvud_gast_ids, personal_ids, grupp_bokning_ids
# FIXME: bokning_datum kan vara i framtiden relativt checkin_date, känns inte rätt
def generate_bokning_dict(p_id):
    checkin_date, checkout_date = generate_checkin_checkout_dates()  # Get random dates
    grupp_bokning_assigned_value = value_for_grupp_bokning_reference(random.choice(grupp_bokning_ids))  # Returns null or fk_grupp_bokning
    bokning_timestamp = generate_random_timestamp(g_set_start_date, 30) 
    bokning_dict = {
        'bokning_id': p_id,
        'rum_id': random.choice(rum_ids),  
        'kund_id': random.choice(kund_ids),  
        'huvud_gast_id': random.choice(huvud_gast_ids),  
        'personal_id': random.choice(personal_ids),  
        'rum_pris_id': random.choice(rum_pris_ids),  
        'grupp_bokning_id': grupp_bokning_assigned_value,  # Group booking ID, either an ID or NULL
        'faktura_id': "NULL",  # FIXME: Placeholder for faktura ID, fixed later, either ID or NULL, is NULL when group id has ID.
        'datum_incheck': checkin_date,  # Randomized check-in date
        'datum_utcheck': checkout_date,  # Randomized check-out date
        'bokning_datum': bokning_timestamp,  # Booking date, randomly generated
        'antal_gaster': random.randint(1, 4)  # Number of guests
    }
    return bokning_dict

def generate_grupp_bokning_dict(p_id):
    grupp_bokning_dict = {
        'grupp_bokning_id': p_id,
        'personal_id': random.choice(personal_ids) 
    }
    return grupp_bokning_dict
#endregion

#region INSERT STATEMENT STRING GENERATOR:::

# INPUTS:
#   table_name: name of table for insert statement
#   dict: the dictionary to be converted to an SQL insert statement
#   b_p_key_auto_increment: boolean, if the primary key is auto increment --> true; otherwise --> false.
def generate_insert_statement(table_name, dict, b_p_key_auto_increment):
    return dict_to_sql_insert_str(table_name, dict, b_p_key_auto_increment)

#endregion

#

# FIXME: have not updated this part yet....
# made all dict functions 
def main():
    # global values with IDs so we can keep track of foreign IDs etc.
    global personal_ids, erbjudande_ids, faktura_ids, rum_ids, kund_ids, huvud_gast_ids, rum_pris_ids, grupp_bokning_ids, erbjudande_ids
    global middag_ids, forsaljning_ids, bokning_ids, rum_typ_ids

    #region number of entities per entity-type, based on NumberOfRooms
    rum_typ_n = 3 # hardcoded as per specification to 3.
    erbjudande_n = math.floor(numberOfRooms/4) # 25% of number of rooms.
    personal_n = math.floor(numberOfRooms/4) # 25% of number of rooms.
    huvud_gast_n = numberOfRooms # same as number of rooms, since same in number of bookings.
    kund_n = numberOfRooms # NOTE: for now keep the same, see if break or not.
    rum_pris_n = numberOfRooms # same as number of rooms.
    rum_n = numberOfRooms # same as number of rooms.
    faktura_n = numberOfRooms # same as number of rooms.
    #grupp_bokning_n = grupp_boking_n  # has different amount, see global value at start. # TODO: move globals to here.
    middag_n = grupp_bokning_n*2 # we thinks it's resonable that every group has two dinners. 
    forsaljning_n = math.floor(numberOfRooms/4) # 25 % of number of rooms: only 25% of guests buy stuff and put on room bill.
    booking_n = numberOfRooms # same as number of rooms.
    #endregion

    #region generate all autoincrement primary ids as ref for foreign key etc.
    rum_typ_ids = ["enkelrum", "dubbelrum", "familjerum"]
    erbjudande_ids = list(range(1, erbjudande_n+1)) 
    personal_ids = list(range(1, personal_n+1)) 
    huvud_gast_ids = list(range(1, huvud_gast_n+1)) 
    kund_ids = list(range(1, kund_n+1)) 
    rum_pris_ids = list(range(1, rum_pris_n+1)) 
    rum_ids = list(range(1, rum_n+1)) 
    faktura_ids = list(range(1, faktura_n+1)) 
    grupp_bokning_ids = list(range(1, grupp_bokning_n+1))
    middag_ids = list(range(1, middag_n+1)) 
    forsaljning_ids = list(range(1, forsaljning_n+1)) 
    bokning_ids = list(range(1, booking_n+1)) 
    #endregion

    #region Generate all the dictionaries and tabulate the results to visualize them:

    l_rum_typ_dicts = [generate_rum_typ_dict(rum_typ_ids[i]) for i in range(rum_typ_n)]
    tabulate_print(l_rum_typ_dicts, "rum_typ", "pre_processing")
    l_erbjudande_dicts = [generate_erbjudande_dict(erbjudande_ids[i]) for i in range(erbjudande_n)]
    tabulate_print(l_erbjudande_dicts, "erbjudande", "pre_processing")
    l_personal_dicts = [generate_personal_dict(personal_ids[i]) for i in range(personal_n)]
    tabulate_print(l_personal_dicts, "personal", "pre_processing")
    l_huvud_gast_dicts = [generate_huvud_gast_dict(huvud_gast_ids[i]) for i in range(huvud_gast_n)]
    tabulate_print(l_huvud_gast_dicts, "huvud_gast", "pre_processing")
    l_kund_dicts = [generate_kund_dict(kund_ids[i]) for i in range(kund_n)]
    tabulate_print(l_kund_dicts, "kund", "pre_processing")
    l_rum_pris_dicts = [generate_rum_pris_dict(rum_pris_ids[i]) for i in range(rum_pris_n)]
    tabulate_print(l_rum_pris_dicts, "rum_pris_typ", "pre_processing")
    l_rum_dicts  = [generate_rum_dict(rum_ids[i]) for i in range(rum_n)]
    tabulate_print(l_rum_dicts, "rum", "pre_processing")
    l_faktura_dicts = [generate_faktura_dict(faktura_ids[i]) for i in range(faktura_n)]
    tabulate_print(l_faktura_dicts, "faktura", "pre_processing")
    l_grupp_bokning_dicts = [generate_grupp_bokning_dict(grupp_bokning_ids[i]) for i in range(grupp_bokning_n)]
    tabulate_print(l_grupp_bokning_dicts, "grupp_bokning", "pre_processing")
    l_middag_dicts = [generate_middag_dict(middag_ids[i]) for i in range(middag_n)]
    tabulate_print(l_middag_dicts, "middag", "pre_processing")
    l_forsaljning_dicts = [generate_forsaljning_dict(forsaljning_ids[i]) for i in range(forsaljning_n)]
    tabulate_print(l_forsaljning_dicts, "forsaljning", "pre_processing")
    l_bokning_dicts = [generate_bokning_dict(bokning_ids[i]) for i in range(booking_n)]
    tabulate_print(l_bokning_dicts, "bokning", "pre_processing")
    #endregion


    #region TODO: update dictionaries with values:

    # update middag with date for dinner based on bookings:
    # functions like this:
    """ fetches the check_in and check_out DATE from l_booking_dicts that has a group booking,
    then creates a TIMESTAMP within that DATE interval and sets it to l_middag_dicts[datum]"""
    update_middag_dict_on_bookings(l_middag_dicts, l_bokning_dicts)
    tabulate_print(l_middag_dicts, "middag", "after: update_middag_dict_on_bookings")

    #  Populates faktura with group IDS where it should have it. NOTE: will probably break.
    # functions like this:
    # TODO: migrate this functionality to below function
    """ checks if a booking has a group_booking and if it has that, gives the ID to factura.grupp_bokning_id
            if it does have a group_booking_ID then it just assigns it with NULL instead"""
    #for i in range(faktura_n): l_faktura_dicts[i]['grupp_bokning_id'] = value_for_grupp_bokning_reference_faktura()
    #bokning_queries = populate_faktura_id_in_boking_queries(bokning_queries)

    # update bokning_dicts with factura dict AND update faktura_dicts.
    # functions like this:
    """ Check: if a booking has a group booking then it sets factura_id to NULL in bokning << UPDATES BOOKING *
                    AND updates factura with that group booking ID  << UPDATES FAKTURA * 
                        AND saves (list: l_factura_id_w_gb) which factura_id has a group booking assigned to it.
                else sets factura_id to an factura_id in bokning that doesn't (EXIST IN list: l_factura_id_w_gb)
                    have a group_booking assigned to it in a factura entity. """
    """def update_bokning_and_faktura(l_bokning_dicts, l_faktura_dicts):
        # NOTE: faktura_id in bokning_dict is always "NULL" before this function call
        # NOTE: grupp_bokning_ID in faktura_dict is always "NULL" before this function call
        l_factura_id_w_gb = [] # store which factura IDs have a group booking assigned
        for bokning_dict in l_bokning_dicts:
            # get group_bokning_id, if none to be found, get "Null"
            g_bokning_id_f_bokning = bokning_dict.get('grupp_bokning_id', 'Null')
            if g_bokning_id_f_bokning != 'NULL':
                bokning_dict['faktura_id'] = 'NULL'
                # we create grupp_bokning_id reference in the faktura_dict instead!
                for faktura_dict in l_faktura_dicts:
                    if faktura_dict['grupp_bokning_id'] == 'NULL': #will always be null first itt but not after.
                        faktura_dict['grupp_bokning_id'] = g_bokning_id_f_bokning
                    else: pass # do nothing, viz. keep it as null.
                l_factura_id_w_gb.append(bokning_dict['faktura_id']) 
                # TODO: HAD TO BREAK HERE TO CHANGE LOGIC FOR HOW DICTIONARIES ARE INCLUDED TO INCLUDE PRIMARY KEY!    
    """
    #endregion

    #region create strings with all the sql queries for write to file!
    
    # generate room_type queries
    rum_typ_queries = [generate_insert_statement("rum_typ", l_rum_typ_dicts[i], False) for i in range(rum_typ_n)]

    # Generate 'erbjudande' queries.
    erbjudande_queries = [generate_insert_statement("erbjudande", l_erbjudande_dicts[i], True) for i in range(erbjudande_n)]

    # Generate 'personal' queries
    personal_queries = [generate_insert_statement("personal", l_personal_dicts[i], True) for i in range(personal_n)]

    # Generate 'huvud_gast' queries 
    huvud_gast_queries = [generate_insert_statement("huvud_gast", l_huvud_gast_dicts[i], True) for i in range(huvud_gast_n)]

    # Generate 'kund' queries 
    kund_queries = [generate_insert_statement("kund", l_kund_dicts[i], True) for i in range(kund_n)]

    # Generate 'rum_pris' queries 
    rum_pris_queries = [generate_insert_statement("rum_pris", l_rum_pris_dicts[i], True) for i in range(rum_pris_n)]

    # Generate 'rum' queries 
    rum_queries = [generate_insert_statement("rum", l_rum_dicts[i], True) for i in range(rum_n)]

    # Generate 'faktura' queries 
    faktura_queries = [generate_insert_statement("faktura", l_faktura_dicts[i], True) for i in range(faktura_n)]

    # Generate 'grupp_bokning' queries 
    grupp_bokning_queries = [generate_insert_statement("grupp_bokning", l_grupp_bokning_dicts[i], True) for i in range(grupp_bokning_n)]

    # generate middag queries
    middag_queries = [generate_insert_statement("middag", l_middag_dicts[i], True) for i in range(middag_n)]

    # generate forsaljning queries
    forsaljning_queries = [generate_insert_statement("forsaljning", l_forsaljning_dicts[i], True) for i in range(forsaljning_n)]

    # Generate booking queries
    bokning_queries = [generate_insert_statement("bokning", l_bokning_dicts[i], True) for i in range(booking_n)]

    #endregion

    #region Write to text files

    write_to_file('1_rum_typ_inserts.txt', rum_typ_queries)
    write_to_file('2_erbjudande_inserts.txt', erbjudande_queries)
    write_to_file('3_personal_inserts.txt', personal_queries)
    write_to_file('4_huvud_gast_inserts.txt', huvud_gast_queries)
    write_to_file('5_kund_inserts.txt', kund_queries)
    write_to_file('6_rum_pris_inserts.txt', rum_pris_queries)
    write_to_file('7_rum_inserts.txt', rum_queries)
    write_to_file('8_faktura_inserts.txt', faktura_queries)
    write_to_file('9_grupp_bokning_inserts.txt', grupp_bokning_queries)
    write_to_file('10_middag_inserts.txt', middag_queries)
    write_to_file('11_forsaljning_inserts.txt', forsaljning_queries)
    write_to_file('12_bokning_inserts.txt', bokning_queries)

    #endregion

if __name__ == '__main__':
    main()
