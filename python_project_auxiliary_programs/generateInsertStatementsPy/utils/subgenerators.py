# utils/subgenerators.py
import random, os
from datetime import datetime, timedelta
#import 3rd party module to visualize tables:
    #firsly you need to install tabulate via pip, if you dont have pip you need to install that first.
    #install tabulate: 
    #      pip install tabulate
    #import tabulate: 
    #      from tabulate import tabulate
    # Print using tabulate
    #       print(tabulate(l_rum_typ_dicts, headers="keys"))
from tabulate import tabulate

# source: https://en.wiktionary.org/wiki/Appendix:Swedish_given_names#The_most_common_given_names_in_Sweden_1890_-_2008
_names_male = ["Alexander", "Alf", "Allan", "Anders", "Andreas", "Anton", "Arne", "Arvid", "Axel", "Bengt", "Bertil", "Birger", "Björn", "Bo", "Bror", "Börje", "Carl", "Christer", "Christian", "Daniel", "David", "Einar", "Emanuel", "Emil", "Eric", "Erik", "Ernst", "Evert", "Folke", "Fredrik", "Georg", "Gunnar", "Gustaf", "Gustav", "Göran", "Gösta", "Hans", "Harald", "Harry", "Henrik", "Henry", "Håkan", "Ingemar", "Ingvar", "Ivar", "Jan", "Johan", "Johannes", "John", "Jonas", "Karl", "Kent", "Kjell", "Knut", "Kurt", "Lars", "Leif", "Lennart", "Magnus", "Marcus", "Martin", "Mats", "Mattias", "Michael", "Mikael", "Niklas", "Nils", "Olof", "Olov", "Oskar", "Ove", "Patrik", "Per", "Peter", "Ragnar", "Robert", "Roger", "Roland", "Rolf", "Rune", "Sebastian", "Simon", "Stefan", "Sten", "Stig", "Sven", "Thomas", "Tobias", "Tomas", "Tommy", "Torsten", "Ulf", "Valdemar", "Vilhelm", "William", "Åke"]
_names_female = ["Agneta", "Alice", "Amanda", "Anette", "Anita", "Ann", "Anna", "Annika", "Astrid", "Barbro", "Berit", "Birgit", "Birgitta", "Britt", "Camilla", "Carina", "Caroline", "Cecilia", "Charlotta", "Christina", "Edit", "Elin", "Elisabet", "Elisabeth", "Elsa", "Emma", "Ester", "Eva", "Greta", "Gun", "Gunborg", "Gunhild", "Gunilla", "Gunvor", "Hanna", "Helena", "Ida", "Inga", "Ingeborg", "Ingegerd", "Ingegärd", "Inger", "Ingrid", "Irene", "Jenny", "Johanna", "Julia", "Karin", "Karolina", "Katarina", "Kerstin", "Kristina", "Lena", "Linda", "Linnea", "Linnéa", "Lisa", "Louise", "Maj", "Malin", "Margareta", "Margit", "Maria", "Marie", "Matilda", "Monica", "Märta", "Rut", "Sara", "Signe", "Siv", "Sofia", "Sonja", "Susanne", "Svea", "Therese", "Ulla", "Ulrika", "Viktoria", "Viola", "Yvonne", "Åsa"]
_names = _names_male + _names_female
# source: https://en.wiktionary.org/wiki/Category:Swedish_surnames
_surnames = ["Abrahamsson", "Adamsberg", "Ahlman", "Alexandersson", "Alfvén", "Andersson", "André", "Andreasson", "Apell", "Arvidsson", "Ask", "Axelsson", "Backlund", "Backman", "Backström", "Bengtsson", "Berg", "Berggren", "Berglund", "Bergman", "Bergqvist", "Bergstrand", "Bergström", "Bergvall", "Bernadotte", "Berzelius", "Bildt", "Birgersson", "Björk", "Björklund", "Björkman", "Björn", "Blom", "Blomqvist", "Blomstrand", "Bolund", "Borg", "Boström", "Brovall", "Burman", "Bååth", "Bäcklund", "Bäckström", "Börjeson", "Carlsson", "Cederström", "Cronström", "Dahl", "Dahlberg", "Dahlbäck", "Dahlström", "Danielsson", "Davidsson", "Ehrling", "Ek", "Ekberg", "Ekdahl", "Ekelöf", "Ekerlid", "Ekholm", "Eklund", "Eklöf", "Ekström", "Eliasson", "Engberg", "Englund", "Engström", "Ericsson", "Eriksson", "Erlandsson", "Erlund", "Fagerlund", "Fallström", "Fjäll", "Fontelius", "Forsberg", "Forsman", "Forssell", "Fransson", "Fredriksson", "Friman", "Frisk", "Glad", "Grafström", "Granestrand", "Grönholm", "Grönroos", "Gucci", "Gunnarsson", "Gustafsson", "Gustavsson", "Göransson", "Hammare", "Hammarskjöld", "Hansson", "Haverling", "Hedborg", "Hedenskog", "Hedlund", "Hedman", "Helander", "Helenius", "Helin", "Hellström", "Henriksson", "Hermansson", "Hjelmqvist", "Holm", "Holmberg", "Holmgren", "Holmquist", "Holmström", "Hulth", "Hyltenstam", "Håkansson", "Hård", "Högberg", "Höglund", "Höxter", "Isaksson", "Ishizaki", "Ivarsson", "Jacobsson", "Jakobsson", "Jansson", "Johansson", "Johnson", "Johnsson", "Jonasson", "Jonsson", "Josefsson", "Jäderberg", "Jönsson", "Karlsson", "Kindstrand", "Kjellander", "Kjellberg", "Kjellström", "Kristersson", "Kvist", "Kvisth", "Kwist", "Lagerkvist", "Lagerlöf", "Larsdotter", "Larsson", "Leander", "Lenné", "Lind", "Lindberg", "Lindblad", "Lindblom", "Lindelöf", "Lindén", "Lindfors", "Lindgren", "Lindholm", "Lindqvist", "Lindroos", "Lindström", "Linnaeus", "Linné", "Ljungberg", "Ljungqvist", "Lundberg", "Lundgren", "Lundh", "Lundin", "Lundqvist", "Lundström", "Löfgren", "Magnusson", "Malin", "Malmquist", "Malmström", "Mankell", "Markström", "Martinsson", "Matsson", "Mattsson", "Månsson", "Mårtensson", "Nilsson", "Nobel", "Nobelius", "Norberg", "Nordin", "Nordquist", "Nordqvist", "Nordström", "Norén", "Nyberg", "Nylund", "Nyman", "Nyström", "Nåjde", "Olofsson", "Olsson", "Palm", "Palme", "Palmquist", "Palmqvist", "Parkstad", "Pehrson", "Pehrsson", "Person", "Persson", "Petersson", "Pettersson", "Pourmokhtari", "Quist", "Quisth", "Qvist", "Qvisth", "Qwist", "Rangström", "Rask", "Renström", "Ribbing", "Ringberg", "Roos", "Ros", "Rosberg", "Rosengren", "Rosenqvist", "Rothschild", "Rudbeck", "Rudolfsson", "Rydberg", "Rydbäck", "Rydkvist", "Rydqvist", "Rydstedt", "Rydström", "Rydvall", "Ryttberg", "Råberg", "Rådström", "Sahlin", "Saleh", "Samuelsson", "Sandberg", "Sandelin", "Sandell", "Sandström", "Schyman", "Sellström", "Sievert", "Sirén", "Sjöberg", "Sjöblom", "Sjögren", "Sjökvist", "Sjölund", "Sjöquist", "Sjöqvist", "Skarsgård", "Skog", "Skoglund", "Snellman", "Spahandelin", "Spjuth", "Spångberg", "Stare", "Staxäng", "Stenqvist", "Stenström", "Strand", "Strid", "Ström", "Strömberg", "Ståhl", "Ståhlbrand", "Sundberg", "Sundkvist", "Sundqvist", "Sundström", "Svanstedt", "Svanström", "Svedberg", "Svensson", "Svinhufvud", "Säfström", "Söder", "Söderberg", "Södergren", "Söderström", "Thunberg", "Thörnqvist", "Torvalds", "Tunberg", "Tungel", "Tungelfelt", "Tvilling", "Wahlroos", "Wahlström", "Wallander", "Wallin", "Westerberg", "Westerlund", "Westman", "Wickman", "Widforss", "Wiktorin", "Åberg", "Ågren", "Åhlström", "Åkerblom", "Åkerlund", "Åkerman", "Åkerström", "Åkesson", "Ångström", "Åslund", "Åström", "Ärlig", "Öberg", "Östberg", "Österberg", "Österman", "Östlund", "Östman"]

def tabulate_print(l_str2tabulate, table_name, condition):
    header2print = "\n" + table_name + "  -  " + condition
    print(header2print)
    print(tabulate(l_str2tabulate, headers="keys"))



def name_surname_generator():
    name = random.choice(_names)  # First names
    surname = random.choice(_surnames)  # Last names
    return name, surname

def generate_checked_in_or_out():
    b_checked_in = random.choice(["FALSE", "TRUE"])
    if b_checked_in == "FALSE":
        b_checked_out = "TRUE"
    else:
        b_checked_out = "FALSE"
    return b_checked_in, b_checked_out

def generate_random_timestamp(i_s_date, i_e_date_days):
    # Parse the input start date
    start_date = datetime.strptime(i_s_date, "%Y-%m-%d")
    
    # Generate a random number of days between 0 and i_e_date_days
    random_days = random.randint(0, i_e_date_days)
    
    # Generate random time (hours, minutes, seconds, microseconds)
    # total number of seconds in a day: 24 * 60 * 60
    random_seconds_in_day = random.randint(0, 24 * 60 * 60)
    
    # Calculate the random timestamp by adding random_days and random time to start_date
    random_timestamp = start_date + timedelta(days=random_days, seconds=random_seconds_in_day)
    
    # Return the random timestamp as a string in "YYYY-MM-DD HH:MM:SS" format
    return random_timestamp.strftime("%Y-%m-%d %H:%M:%S")

# Generate random date between today and a future date within a certain range (e.g., 30 days from today)
def generate_random_date(start_date, days_range):
    # parse string to a datetime object
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    
    # Generate a random number of days and add it to start_date
    return start_date + timedelta(days=random.randint(0, days_range))

# Generate offer price start and end date
def generate_offer_startend_dates():
    today = datetime.today()
    offer_start = generate_random_date(today, 90)  # Random start date of offer within 90 days from today
    offer_end = offer_start + timedelta(days=random.randint(5, 14))  # Random end date of offer between 5-14 days after offer start
    return offer_start, offer_end

# Generate check-in and check-out dates
def generate_checkin_checkout_dates():
    today = datetime.today()
    checkin_date = generate_random_date(today, 30)  # Random check-in within 30 days from today
    checkout_date = checkin_date + timedelta(days=random.randint(1, 7))  # Random stay between 1-7 days
    return checkin_date, checkout_date

# e.g. input = 100.11, 500, 2
# e.g. output = 432.11
def generate_random_decimal_pricesum(l_limit, u_limit, n_of_dec_places):
    random_value = random.uniform(l_limit, u_limit)
    return round(random_value, n_of_dec_places)

# generate price intervalls for each room based on it's roop type
def price_intervalls_per_room_type(room_type_id):
    if room_type_id == "enkelrum":
        return round(random.uniform(400.0, 550.0), 2)
    if room_type_id == "dubbelrum":
        return round(random.uniform(600.0, 950.0), 2)
    if room_type_id == "familjerum":
        return round(random.uniform(1000.0, 1400.0), 2)

# write string to a created output directory with date and time of runtime as part of it's name.
def write_to_file(filename, queries):
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