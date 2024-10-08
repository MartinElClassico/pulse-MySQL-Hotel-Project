#region import statements
import random
import datetime
import math
# import our own modules from utils child directory.
from utils import dict_to_sql_insert_str
from utils import name_surname_generator
#endregion

#region handle number of INSERT statements generated
# number of testcases viz. input statements per table
numberOfInputs = 20
# number of "grupp_bokningar"
numberOfInputs_gb = 3
# percentage of bookings that should be group bookings:
p_gr_b = 0.50
# number of bookings per group booking
bookings_per_groupb = math.floor(round((numberOfInputs)*p_gr_b)/numberOfInputs_gb) # 50 percent of the booking divided by number of group bookings rounded down.
#endregion

# TODO: do these really need to be global? At least think about it...
#region global values for auxiliary purposes
#region Store the generated primary key values for foreign key references
personal_ids = []
erbjudande_ids = []
faktura_ids = []
rum_ids = []
rum_typ_ids = ["enkelrum", "familjerum", "dubbelrum"]  # Predefined room types
kund_ids = []
huvud_gast_ids = []
rum_pris_ids = []
grupp_bokning_ids = []
erbjudande_ids = []
#endregion

#region Store output from value_for_grupp_bokning_reference for later referal for "faktura"
l_values_generated_gbokning_ref = []
int_current_call_from_factura = 0
l_calls_when_gbooking_not_null = []
#endregion

# fixed length list of number of bookings assigned to each group booking
bookings_added_per_groupb = [0] * numberOfInputs_gb
#endregion

# TODO: see if these can be migrated to "utils", ugly and distracting to have them here...
#region AUXILIARY FUNCTIONS

# AUXILIARY TABLE FUNCTIONS:::
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
    for i in range(1, numberOfInputs_gb+1):
        if grupp_bokning_id_current != "NULL":
            bokning_queries[faktura_id] = "NULL"
        else: bokning_queries[faktura_id] = i
    return bokning_queries

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
        #TODO: how do we really want the discount to work? Need to revise
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

def generate_rum_dict(rum_typ_ids, personal_ids):
    # Generate random values for the rum dictionary
    rum_dict = {
        'rum_typ_id': random.choice(rum_typ_ids),  # Room type ID (e.g., "enkelrum", "familjerum", "dubbelrum")
        'personal_id': random.choice(personal_ids),  # Personal ID must exist in 'personal'
        #TODO: fix logic for this so it can only be one at a time
        'checked_in': random.choice([0, 1]),  # Checked in (0 or 1)
        'checked_out': random.choice([0, 1])  # Checked out (0 or 1)
    }
    return rum_dict

def generate_rum_pris_dict(rum_typ_ids):
    # Generate random values for the rum_pris dictionary
    rum_typ_id = random.choice(rum_typ_ids)
    pris_per_natt = price_intervalls_per_room_type(rum_typ_id)  
    pris_start_datum, pris_slut_datum = generate_offer_startend_dates()
    
    rum_pris_dict = {
        'rum_typ_id': rum_typ_id,  
        'pris_per_natt': pris_per_natt,  
        'pris_start_datum': pris_start_datum,  
        'pris_slut_datum': pris_slut_datum  
    }
    
    return rum_pris_dict

# TODO: how many instances of middag should we make? Right now every group booking has a lot of dinnners...
def generate_middag_dict(grupp_bokning_ids):
    middag_dict = {
        'grupp_bokning_id': random.choice(grupp_bokning_ids),  
        'antal_personer': random.randint(1, 10),  
        # TODO: make (or refer to) auto generator for date of meal.  
        'datum': "2024-10-14"  # Date of the meal
    }
    return middag_dict

def generate_faktura_dict(personal_ids):
    faktura_dict = {
        'personal_id': random.choice(personal_ids),  
        # TODO: erbjudande_id shouldn't be auto generated like this?
        'erbjudande_id': random.randint(1, 20),  # Assuming erbjudande IDs are within this range
        'grupp_bokning_id': "UPDATED LATER VIA MAIN"  
    }
    return faktura_dict

def generate_bokning_dict(rum_ids, kund_ids, huvud_gast_ids, personal_ids, grupp_bokning_ids):
    checkin_date, checkout_date = generate_checkin_checkout_dates()  # Get random dates
    grupp_bokning_assigned_value = value_for_grupp_bokning_reference(random.choice(grupp_bokning_ids))  # Returns null or fk_grupp_bokning

    bokning_dict = {
        'rum_id': random.choice(rum_ids),  
        'kund_id': random.choice(kund_ids),  
        'huvud_gast_id': random.choice(huvud_gast_ids),  
        'personal_id': random.choice(personal_ids),  
        'rum_pris_id': random.randint(1, 20),  # Assuming room price IDs are within this range
        'grupp_bokning_id': grupp_bokning_assigned_value,  # Group booking ID, either an ID or NULL
        'faktura_id': "faktura_id",  # Placeholder for faktura ID, fixed later
        'datum_incheck': checkin_date,  # Randomized check-in date
        'datum_utcheck': checkout_date,  # Randomized check-out date
        #TODO: fix this, cannot be now:
        'booking_datum': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Booking date
        'antal_gaster': random.randint(1, 4)  # Number of guests
    }
    return bokning_dict

def generate_grupp_bokning_dict(personal_ids):
    grupp_bokning_dict = {
        'personal_id': random.choice(personal_ids) 
    }
    return grupp_bokning_dict

#region INPUT STATEMENT GENERATORS:::


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

def write_to_file(filename, queries):
    with open(filename, 'w', encoding='utf-8') as file:
        for query in queries:
            file.write(query + '\n')
    print(f"Data written to {filename}")

# TODO: have not updated this part yet....
# made all dict functions 
def main():
    global personal_ids, erbjudande_ids, faktura_ids, rum_ids, kund_ids, huvud_gast_ids, rum_pris_ids, grupp_bokning_ids, erbjudande_ids

    # Generate 'personal' table so we have IDs to reference
    personal_queries = [generate_personal_insert() for _ in range(numberOfInputs)]
    personal_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for personal

    # Generate 'rum_typ' table with predefined values
    rum_typ_queries = [
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('enkelrum', 1);",
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('familjerum', 4);",
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('dubbelrum', 2);"
    ]
    # Generate 'erbjudande' table so we have IDs to reference
    erbjudande_queries = [generate_erbjudande_insert() for _ in range(numberOfInputs)]
    erbjudande_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for kund

    # Generate 'kund' table so we have IDs to reference
    kund_queries = [generate_kund_insert() for _ in range(numberOfInputs)]
    kund_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for kund

    # Generate 'huvud_gast' table so we have IDs to reference
    huvud_gast_queries = [generate_huvud_gast_insert() for _ in range(numberOfInputs)]
    huvud_gast_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for huvud_gast

    # Generate 'rum_pris' table so we have IDs to reference
    rum_pris_queries = [generate_rum_pris_insert() for _ in range(numberOfInputs)]
    rum_pris_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for rum_pris

    # Generate 'rum' table so we have IDs to reference
    rum_queries = [generate_rum_insert() for _ in range(numberOfInputs)]
    rum_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for rum

    # Generate 'faktura' table so we have IDs to reference
    faktura_queries = [generate_faktura_insert() for _ in range(numberOfInputs)]
    faktura_ids = list(range(1, numberOfInputs+1))  # Assuming auto-increment starts at 1 for faktura

    # Generate 'grupp_bokning' table so we have IDs to reference
    grupp_bokning_queries = [generate_grupp_bokning_insert() for _ in range(numberOfInputs_gb)]
    grupp_bokning_ids = list(range(1, numberOfInputs_gb+1))  # Assuming auto-increment starts at 1 for grupp_bokning

    # Generate other queries
    bokning_queries = [generate_bokning_insert() for _ in range(numberOfInputs)]
    middag_queries = [generate_middag_insert() for _ in range(numberOfInputs)]

    # !!! problem, det är inte dict som kommer tillbaka utan str... 
    #   returna dict också på dessa?
    for _ in range(numberOfInputs): faktura_queries[grupp_bokning_id] = value_for_grupp_bokning_reference_faktura()
    bokning_queries = populate_faktura_id_in_boking_queries(bokning_queries)

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
