import random
import datetime

# Store the generated primary key values for foreign key references
personal_ids = []
erbjudande_ids = []
faktura_ids = []
rum_ids = []
rum_typ_ids = ["enkelrum", "familjerum", "dubbelrum"]  # Predefined room types
kund_ids = []
huvud_gast_ids = []
rum_pris_ids = []
grupp_bokning_ids = []

# Generate random date between today and a future date within a certain range (e.g., 30 days from today)
def generate_random_date(start_date, days_range):
    return start_date + datetime.timedelta(days=random.randint(0, days_range))

# Generate check-in and check-out dates
def generate_checkin_checkout_dates():
    today = datetime.date.today()
    checkin_date = generate_random_date(today, 30)  # Random check-in within 30 days from today
    checkout_date = checkin_date + datetime.timedelta(days=random.randint(1, 7))  # Random stay between 1-7 days
    return checkin_date, checkout_date

def generate_personal_insert():
    personal_query = """
        INSERT INTO personal (fornamn, efternamn, roll)
        VALUES ('{}', '{}', '{}');
    """
    personal_values = (
        random.choice(['Anna', 'Peter', 'Cecilia', 'David', 'Erik']),  # First names
        random.choice(['Svensson', 'Johansson', 'Karlsson', 'Nilsson', 'Larsson']),  # Last names
        random.choice(['Receptionist', 'Manager', 'Cleaner'])  # Role
    )
    return personal_query.format(*personal_values)

def generate_kund_insert():
    kund_query = """
        INSERT INTO kund (fornamn, efternamn, mejl_address, telefon_nummer)
        VALUES ('{}', '{}', '{}', '{}');
    """
    kund_values = (
        random.choice(['Oskar', 'Ellen', 'Fredrik', 'Lina', 'Sara']),  # First names
        random.choice(['Andersson', 'Berg', 'Eriksson', 'Gustafsson', 'Lind']),  # Last names
        '{}@example.com'.format(random.randint(1000, 9999)),  # Email address
        '+46{}'.format(random.randint(700000000, 799999999))  # Phone number
    )
    return kund_query.format(*kund_values)

def generate_huvud_gast_insert():
    huvud_gast_query = """
        INSERT INTO huvud_gast (fornamn, efternamn, mejl_address, telefon_nummer)
        VALUES ('{}', '{}', '{}', '{}');
    """
    huvud_gast_values = (
        random.choice(['Eva', 'Peter', 'Maria', 'Anders', 'Sofia']),  # First names
        random.choice(['Lund', 'Olsson', 'Persson', 'Nilsson', 'Svensson']),  # Last names
        '{}@example.com'.format(random.randint(1000, 9999)),  # Email address
        '+46{}'.format(random.randint(700000000, 799999999))  # Phone number
    )
    return huvud_gast_query.format(*huvud_gast_values)

def generate_rum_insert():
    rum_query = """
        INSERT INTO rum (rum_typ_id, personal_id, checked_in, checked_out)
        VALUES ('{}', {}, {}, {});
    """
    rum_values = (
        random.choice(rum_typ_ids),  # Room type ID must be "enkelrum", "familjerum", or "dubbelrum"
        random.choice(personal_ids),  # Personal ID must exist in 'personal'
        random.choice([0, 1]),  # Checked in
        random.choice([0, 1])   # Checked out
    )
    return rum_query.format(*rum_values)

def generate_rum_pris_insert():
    rum_pris_query = """
        INSERT INTO rum_pris (rum_typ_id, pris_per_natt, pris_start_datum, pris_slut_datum)
        VALUES ('{}', {}, '{}', '{}');
    """
    rum_pris_values = (
        random.choice(rum_typ_ids),  # Room type ID must be "enkelrum", "familjerum", or "dubbelrum"
        round(random.uniform(100.0, 500.0), 2),  # Price per night
        '2024-10-01',  # Price start date
        '2024-12-31'   # Price end date
    )
    return rum_pris_query.format(*rum_pris_values)

def generate_middag_insert():
    middag_query = """
        INSERT INTO middag (grupp_bokning_id, antal_personer, datum)
        VALUES ({}, {}, '{}');
    """
    middag_values = (
        random.choice(grupp_bokning_ids),  # Group booking ID must exist in 'grupp_bokning'
        random.randint(1, 10),  # Number of people
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date of the meal
    )
    return middag_query.format(*middag_values)

# New generate_faktura_insert function
def generate_faktura_insert():
    faktura_query = """
        INSERT INTO faktura (personal_id, erbjudande_id)
        VALUES ({}, {});
    """
    faktura_values = (
        random.choice(personal_ids),  # Reuse existing personal ID
        random.randint(1, 20)  # Assuming erbjudande IDs are within this range
    )
    return faktura_query.format(*faktura_values)

def generate_bokning_insert():
    bokning_query = """
        INSERT INTO bokning (rum_id, kund_id, huvud_gast_id, personal_id, rum_pris_id, grupp_bokning_id, 
                             datum_incheck, datum_utcheck, booking_datum, antal_gaster)
        VALUES ({}, {}, {}, {}, {}, {}, '{}', '{}', '{}', {});
    """
    checkin_date, checkout_date = generate_checkin_checkout_dates()  # Get random dates
    bokning_values = (
        random.choice(rum_ids),  # Room ID must exist in 'rum'
        random.choice(kund_ids),  # Customer ID must exist in 'kund'
        random.choice(huvud_gast_ids),  # Main guest ID must exist in 'huvud_gast'
        random.choice(personal_ids),  # Personal ID must exist in 'personal'
        random.randint(1, 20),  # Assuming room price IDs are within this range
        random.choice(grupp_bokning_ids),  # Group booking ID must exist in 'grupp_bokning'
        checkin_date,  # Randomized check-in date
        checkout_date,  # Randomized check-out date
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Booking date
        random.randint(1, 4)  # Number of guests
    )
    return bokning_query.format(*bokning_values)

def generate_grupp_bokning_insert():
    grupp_bokning_query = """
        INSERT INTO grupp_bokning (personal_id, faktura_id)
        VALUES ({}, {});
    """
    grupp_bokning_values = (
        random.choice(personal_ids),  # Reuse existing personal ID
        random.choice(faktura_ids)   # Reuse existing invoice ID
    )
    return grupp_bokning_query.format(*grupp_bokning_values)

def write_to_file(filename, queries):
    with open(filename, 'w', encoding='utf-8') as file:
        for query in queries:
            file.write(query + '\n')
    print(f"Data written to {filename}")

def main():
    global personal_ids, erbjudande_ids, faktura_ids, rum_ids, kund_ids, huvud_gast_ids, rum_pris_ids, grupp_bokning_ids

    # Generate 'personal' table so we have IDs to reference
    personal_queries = [generate_personal_insert() for _ in range(20)]
    personal_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for personal

    # Generate 'rum_typ' table with predefined values
    rum_typ_queries = [
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('enkelrum', 1);",
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('familjerum', 4);",
        "INSERT INTO rum_typ (rum_typ_id, max_antal_personer) VALUES ('dubbelrum', 2);"
    ]

    # Generate 'kund' table so we have IDs to reference
    kund_queries = [generate_kund_insert() for _ in range(20)]
    kund_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for kund

    # Generate 'huvud_gast' table so we have IDs to reference
    huvud_gast_queries = [generate_huvud_gast_insert() for _ in range(20)]
    huvud_gast_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for huvud_gast

    # Generate 'rum_pris' table so we have IDs to reference
    rum_pris_queries = [generate_rum_pris_insert() for _ in range(20)]
    rum_pris_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for rum_pris

    # Generate 'rum' table so we have IDs to reference
    rum_queries = [generate_rum_insert() for _ in range(20)]
    rum_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for rum

    # Generate 'faktura' table so we have IDs to reference
    faktura_queries = [generate_faktura_insert() for _ in range(20)]
    faktura_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for faktura

    # Generate 'grupp_bokning' table so we have IDs to reference
    grupp_bokning_queries = [generate_grupp_bokning_insert() for _ in range(20)]
    grupp_bokning_ids = list(range(1, 21))  # Assuming auto-increment starts at 1 for grupp_bokning

    # Generate other queries
    bokning_queries = [generate_bokning_insert() for _ in range(20)]
    middag_queries = [generate_middag_insert() for _ in range(20)]

    # Write to text files
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
