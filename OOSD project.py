namelist = False
import os
import re

def is_valid_email(email):
    # Regular expression for validating an Email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPress Enter to continue...")
    clear_screen()

def validate_password(password, confirm_password):
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return False
    return True

class Datasystem:
    def __init__(self):
        self.profiledata = []
        self.flood_areas = []
        self.supplies = []
        self.reports_available = False
        self.volunteer_area_mapping = {}

    def encrypt_password(self, password):
        encrypted = []
        for char in password:
            if char.isdigit():
                # Replace digits with corresponding special characters
                special_chars = "!@#$%^&*()"
                encrypted.append(special_chars[int(char)])
            else:
                # Shift character by 5 positions
                encrypted.append(chr(ord(char) + 5))
        return ''.join(encrypted)

    def decrypt_password(self, encrypted_password):
        decrypted = []
        special_chars = "!@#$%^&*()"
        for char in encrypted_password:
            if char in special_chars:
                # Replace special characters back to digits
                decrypted.append(str(special_chars.index(char)))
            else:
                # Shift character back by 5 positions
                decrypted.append(chr(ord(char) - 5))
        return ''.join(decrypted)

    def add_profile(self, profile):
        # Encrypt the password before adding the profile
        profile.password = self.encrypt_password(profile.password)
        self.profiledata.append(profile)

    def get_profiles_by_type(self, type):
        return [profile for profile in self.profiledata if profile.type == type]
    def add_profile(self, profile):
        self.profiledata.append(profile)

    def get_profiles_by_type(self, type):
        return [profile for profile in self.profiledata if profile.type == type]

    def get_profile_by_username(self, username):
        return next((profile for profile in self.profiledata if profile.username == username), None)

    def verify(self, username, password):
        return next((profile for profile in self.profiledata if profile.username == username and profile.password == password), None)

    def add_flood_area(self, area):
        self.flood_areas.append(area)

    def get_flood_area_by_name(self, area_name):
        return next((area for area in self.flood_areas if area['name'] == area_name), None)

    def add_supply(self, supply):
        self.supplies.append(supply)

    def get_supplies(self):
        return self.supplies

    def login(self):
        clear_screen()
        print("\n----- Login -----")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        if not username or not password:
            print("Username and password are required.")
            return None

        if username == "admin" and password == "admin12#":
            print("Login successful! Welcome, Admin.")
            return Admin()

        user = self.verify(username, password)
        if user:
            print(f"Login successful! Welcome, {user.username} ({user.type})")
            return user
        else:
            print("Invalid credentials. Please try again.")
            return None

    def display_all_users(self):
        clear_screen()
        print("\nAll Registered Users:")
        if not self.profiledata:
            print("No users registered.")
            return

    # First, display decrypted passwords
        while True:
            clear_screen()
            print("\nDecrypted Passwords:")
            for index, user in enumerate(self.profiledata, start=1):
                decrypted_password = self.decrypt_password(user.password)  # Decrypt the password
                print(f"{index}. Username: {user.username}, Decrypted Password: {decrypted_password}, Type: {user.type}, Email: {user.email}, Skills: {', '.join(user.skills) if hasattr(user, 'skills') else 'N/A'}")

            choice12 = input("The password is already encrypted. Do you want to see the decrypted passwords? (y/n): ").lower()
    
            if choice12 == "y": 
                clear_screen()
                print("\nEncrypted Passwords:")
                for index, user in enumerate(self.profiledata, start=1):
                    print(f"{index}. Username: {user.username}, Encrypted Password: {user.password}, Type: {user.type}, Email: {user.email}, Skills: {', '.join(user.skills) if hasattr(user, 'skills') else 'N/A'}")
                pause()  # Pause after showing encrypted passwords
                break  # Exit the loop after showing encrypted passwords
            elif choice12 == "n":
                pause()
                break  # Exit the loop if the user chooses not to see encrypted passwords
            else:
                print("Invalid input! Please enter 'y' or 'n'.")
                pause()
                clear_screen()

    def edit_user(self, index):
        if index < 0 or index >= len(self.profiledata):
            print("Invalid user selection.")
            return
        
        user = self.profiledata[index]
        print(f"\nEditing User: {user.username} ({user.type})")
        
        new_username = input(f"Enter new username (current: {user.username}): ").strip()
        if new_username:
            user.username = new_username
        
        new_email = input(f"Enter new email (current: {user.email}): ").strip()
        if new_email:
            user.email = new_email
        
        new_password = input(f"Enter new password (current: {user.password}): ").strip()
        if new_password:
            user.password = new_password
        
        new_skills = input(f"Enter new skills (comma-separated, current: {', '.join(user.skills)}): ").strip()
        if new_skills:
            user.skills = [skill.strip() for skill in new_skills.split(",")]

        print(f"User   {user.username} updated successfully.")
        pause()

    def delete_user(self, index):
        if index < 0 or index >= len(self.profiledata):
            print("Invalid user selection.")
            return
        
        user = self.profiledata.pop(index)
        print(f"User    {user.username} deleted successfully.")
        pause()

    def map_volunteer_to_area(self, volunteer, area_name):
        if area_name not in self.volunteer_area_mapping:
            self.volunteer_area_mapping[area_name] = []
        self.volunteer_area_mapping[area_name].append(volunteer)

    def get_volunteers_in_area(self, area_name):
        return self.volunteer_area_mapping.get(area_name, [])
    
    def generate_report(self):
        clear_screen()
        print("\nGenerating Report for All Flood-Affected Areas...")
        if not self.flood_areas:
            print("No flood areas available to generate reports.")
            return

        total_transportation_cost = 0

        for area in self.flood_areas:
            print(f"Report for Area: {area['name']}")
            print(f"- Severity: {area['severity']}")
            print(f"- Distance: {area['distance']} km")
            print(f"- Supplies Needed:")
            for supply, quantity in area['supplies'].items():
                print(f"  - {supply.capitalize()}: {quantity}")

            distance = area['distance']
            supplies_weight = sum(area['supplies'].values())
            transportation_cost = (Report.BASE_COST_PER_KM * distance) + (Report.COST_PER_KG * supplies_weight)
            total_transportation_cost += transportation_cost

            print(f"- Transportation Cost: ${transportation_cost:.2f}")
            print()

        print(f"Total Transportation Cost for All Areas: ${total_transportation_cost:.2f}")
        self.reports_available = True  # Set the flag to indicate reports are available
        pause()

    def display_report(self):
        if not self.reports_available:
            print("No report available to display.")
            return
        
        print("\nDisplaying Report for Flood-Affected Areas:")
        for area in self.flood_areas:
            print(f"Report for Area: {area['name']}")
            print(f"- Severity: {area['severity']}")
            print(f"- Distance: {area['distance']} km")
            print(f"- Supplies Needed:")
            for supply, quantity in area['supplies'].items():
                print(f"  - {supply.capitalize()}: {quantity}")

            # Calculate transportation cost for display
            distance = area['distance']
            supplies_weight = sum(area['supplies'].values())
            transportation_cost = (Report.BASE_COST_PER_KM * distance) + (Report.COST_PER_KG * supplies_weight)
            print(f"- Transportation Cost: ${transportation_cost:.2f}")
            print()  # Print a newline for better readability


class Authority:
    def __init__(self, username, password, email, organization_name, type="Authority"):
        self.username = username
        self.password = password
        self.email = email
        self.organization_name = organization_name
        self.type = type

    def register(self, datasystem):
        clear_screen()
        print("\nRegistering as Authority...")
        if datasystem.get_profile_by_username(self.username):
            print("Account already exists. Please choose a different username.")
            return

        self.email = input("Enter your email address: ").strip()
        if not self.email:
            print("Email is required.")
            return
        self.password = input("Create your password: ").strip()
        confirm_password = input("Confirm your password: ").strip()
        if self.password != confirm_password:
            print("Passwords do not match. Please try again.")
            pause()
            return
        clear_screen()
        datasystem.add_profile(self)
        print(f"Registration successful! Welcome, {self.username}.")
        pause()

    def dashboard(self, flood_ops, datasystem, supply_ops):
        while True:
            clear_screen()
            print("\nAuthority Dashboard:")
            print("1. Manage Flood Affected Areas")
            print("2. Register Supply")
            print("3. Track Supply")
            print("4. View Report")
            print("5. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                flood_ops.dashboard(datasystem)
                pause()
            elif choice == "2":
                supply_ops.register_supply(datasystem)
                pause()
            elif choice == "3":
                supply_ops.track_supply()
                pause()
            elif choice == "4":
                self.view_report(datasystem)
                pause()
            elif choice == "5":
                print("Logging out...")
                pause()
                break
            else : 
                print("Invalid Input!!! Please try again")
                pause()
                clear_screen()

    def view_report(self, datasystem):
        if datasystem.reports_available:
            print("\nViewing Report...")
            datasystem.display_report()  # Call a method to display the report
        else:
            print("No report available to view. Please ask the Admin to generate a report.")

class Volunteer:
    def __init__(self, username, password, email, skills, type="Volunteer"):
        self.username = username
        self.password = password
        self.email = email
        self.skills = skills
        self.type = type
        self.availability = False
        self.area = None

    def register(self, datasystem):
        clear_screen()
        print("\nRegistering as Volunteer...")
        if datasystem.get_profile_by_username(self.username):
            print("Account already exists. Please choose a different username.")
            return

        self.email = input("Enter your email address: ").strip()
        if not self.email or not is_valid_email(self.email):
            print("Invalid email format. Please enter a valid email address.")
            return

        skills = input("Enter your skills (comma-separated): ").strip()
        self.skills = [skill.strip() for skill in skills.split(",")]
    
        self.password = input("Create your password: ").strip()
        
        confirm_password = input("Confirm your password: ").strip()
       
        if self.password != confirm_password:
            print("Passwords do not match. Please try again.")
            return
        datasystem.add_profile(self)
        clear_screen()
        print(f"Registration successful! Welcome, {self.username}.")
        pause()

    def register_availability(self, datasystem):
        clear_screen()
        print("\nRegistering Availability...")
        if not datasystem.flood_areas:
            print("No flood-affected areas available.")
            return

        print("Available Flood-Affected Areas:")
        for index, area in enumerate(datasystem.flood_areas, start= 1):
            print(f"{index}. {area['name']} (Severity: {area['severity']}, Distance: {area['distance']} km)")

        try:
            choice = int(input("Select the index of the flood-affected area you want to register for: ")) - 1
            if choice < 0 or choice >= len(datasystem.flood_areas):
                print("Invalid selection. Please try again.")
                pause()
                return
            self.area = datasystem.flood_areas[choice]['name']
            self.availability = True
            datasystem.map_volunteer_to_area(self.username, self.area)
            print(f"Availability registered for area '{self.area}'.")
            self.view_volunteer_list(datasystem)
            pause()
          
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            pause()
 
    def view_volunteer_list(self, datasystem):
        clear_screen()
        print("\nViewing Volunteer List for Area:", self.area)
        if not self.area:
            print("You need to register your availability first.")
            pause()
            return

        volunteers_in_area = datasystem.get_volunteers_in_area(self.area)
        
        if not volunteers_in_area:
            print("No other volunteers registered for this area.")
            pause()
            return

        print("Volunteers registered for this area:")
        for volunteer in volunteers_in_area:
            print(f"- {volunteer} (Skills: {', '.join([v.skills for v in datasystem.profiledata if v.username == volunteer][0])})")  
        pause()

    def dashboard(self, flood_ops, datasystem):
        while True:
            clear_screen()
            print("\nVolunteer Dashboard:")
            print("1. Manage Flood Affected Areas")
            print("2. View Volunteer List")
            print("3. Register Availability")
            print("4. View Report")
            print("5. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                flood_ops.dashboard(datasystem)
                pause()
            elif choice == "2":
                if self.availability:
                    self.view_volunteer_list(datasystem)
                    pause()
                else:
                    print("You should register availability first.")
                    pause()
                    continue  
            elif choice == "3":
                self.register_availability(datasystem)
                pause()
            elif choice == "4":
                self.view_report(datasystem)
                pause()
            elif choice == "5":
                print("Logging out...")
                pause()
                break
            else : 
                print("Invalid Input . Please try again.")
                pause()
                clear_screen()
                
    def view_report(self, datasystem):
        if datasystem.reports_available:
            print("\nViewing Report...")
            datasystem.display_report()  # Call a method to display the report
        else:
            print("No report available to view. Please ask the Admin to generate a report.")

class Admin(Datasystem):
    def __init__(self, username="admin", password="user12#", type="Admin"):
        super().__init__()
        self.username = username
        self.password = password
        self.type = type

    def dashboard(self, flood_ops, datasystem, supply_ops):
        while True:
            clear_screen()
            print("\nAdmin Dashboard:")
            print("1. Manage Flood Affected Areas")
            print("2. View Users")
            print("3. Generate Report")
            print("4. View Report")
            print("5. Edit Users")
            print("6. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                flood_ops.dashboard(datasystem)
                pause()
            elif choice == "2":
                datasystem.display_all_users()
                pause()
            elif choice == "3":
                Admin.generate_report(datasystem)
                pause()
            elif choice == "4":
                self.view_report(datasystem)
                pause()
            elif choice == "5":
                self.manage_users(datasystem)
                pause()
            elif choice == "6":
                print("Logging out...")
                pause()
                break
            else :
                print("Invalid choice. Please try again.")
                pause() 
                clear_screen()

    def manage_users(self, datasystem):
        while True:
            clear_screen()
            datasystem.display_all_users()
            print("0. Exit to Admin Dashboard")
            choice = input("Enter the number of the user to edit/delete or 0 to exit: ").strip()

            if choice == "0":
                break

            try:
                index = int(choice) - 1
                action = input("Enter 'edit' to edit or 'delete' to delete the user: ").strip().lower()

                if action == "edit":
                    datasystem.edit_user(index)
                elif action == "delete":
                    datasystem.delete_user(index)
                else:
                    print("Invalid action. Please enter 'edit' or 'delete'.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def view_report(self, datasystem):
        if datasystem.reports_available:
            print("\nViewing Report...")
            datasystem.display_report()  # Call a method to display the report
        else:
            print("No report available to view. Please ask the Admin to generate a report.")

    @staticmethod
    def generate_report(datasystem):
        clear_screen()
        print("\nGenerating Report for All Flood-Affected Areas...")
        if not datasystem.flood_areas:
            print("No flood areas available to generate reports.")
            return

        for area in datasystem.flood_areas:
            print(f"Report for Area: {area['name']}")
            print(f"- Severity: {area['severity']}")
            print(f"- Distance: {area['distance']} km")
            print(f"- Supplies Needed:")
            for supply, quantity in area['supplies'].items():
                print(f"  - {supply.capitalize()}: {quantity}")
            print()  # Print a newline for better readability
         # Calculate transportation cost for display
            distance = area['distance']
            supplies_weight = sum(area['supplies'].values())
            transportation_cost = (Report.BASE_COST_PER_KM * distance) + (Report.COST_PER_KG * supplies_weight)
            print(f"- Transportation Cost: ${transportation_cost:.2f}")
            print()  # Print a newline for better readability
        datasystem.reports_available = True
        print("Reports generated successfully.")
        pause()

class Report:
    BASE_COST_PER_KM = 7
    COST_PER_KG = 8

    def __init__(self, flood_area):
        self.flood_area = flood_area

    def generate(self):
        print(f"Generating report for area: {self.flood_area['name']}")
        distance = self.flood_area.get('distance', 0)
        supplies_weight = sum(self.flood_area.get('supplies', {}).values())
        transportation_cost = (self.BASE_COST_PER_KM * distance) + (self.COST_PER_KG * supplies_weight)

        print(f"Report Summary:")
        print(f"- Distance: {distance} km")
        print(f"- Total Weight of Supplies: {supplies_weight} kg")
        print(f"- Transportation Cost: ${transportation_cost:.2f}")

class FloodAffected:
    def __init__(self):
        self.flood_areas = []

    def add_area(self, datasystem):
        clear_screen()
        print("\nAdding new flood-affected area...")

        name = input("Enter the name of the flood area: ").strip()
        if datasystem.get_flood_area_by_name(name):
            print(f"Area '{name}' already exists.")
            return

        severity = input("Enter the severity of the flood (1-5): ").strip()
        if not severity.isdigit() or not (1 <= int(severity) <= 5):
            print("Invalid severity. Please enter a number between 1 and 5.")
            return
        severity = int(severity)

        try:
            distance = float(input("Enter the distance between the terminal hub and the flood area (in kilometers): ").strip())
            if distance < 0:
                print("Distance cannot be negative.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number for distance.")
            return

        supplies = {
            "shelter": 0,
            "food": 0,
            "medicine": 0,
            "clothes": 0
        }

        print("Enter the resource quantities needed:")
        for supply in supplies:
            try:
                quantity = int(input(f"Enter the quantity needed for {supply}: ").strip())
                if quantity < 0:
                    print(f"Invalid quantity for {supply}. Quantity cannot be negative.")
                    return
                supplies[supply] = quantity
            except ValueError:
                print(f"Invalid input for {supply}. Please enter a valid number.")
                return

        datasystem.add_flood_area({
            "name": name,
            "severity": severity,
            "distance": distance,
            "supplies": supplies
        })

        print(f"Flood area '{name}' added successfully.")
        pause()

    def view_areas(self, datasystem):
        clear_screen()
        print("\nView Flood Areas:")
        if datasystem.flood_areas:
            print("0. Exit to the main menu")
            for index, area in enumerate(datasystem.flood_areas, start=1):
                print(f"{index}. Area: {area['name']}, Severity: {area['severity']}, Distance: {area['distance']} km")
                print("   Resources Needed:")
                for resource, quantity in area['supplies'].items():
                    print(f"      {resource.capitalize()}: {quantity} (Current needed: {quantity})")
        else:
            print("No flood areas available.")
        pause()

    def edit_area(self, datasystem):
        clear_screen()
        print("\nEditing a flood-affected area...")
        self.view_areas(datasystem)
        try:
            index = int(input("Enter the index of the area to edit(or 0 to exit): ").strip()) - 1
            if index == -1:
                return
            elif index < 0 or index >= len(datasystem.flood_areas):
                print("Invalid selection. Please try again.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        area = datasystem.flood_areas[index]
        print(f"Editing {area['name']}...")

        area['name'] = input(f"Enter new name (current: {area['name']}): ").strip() or area['name']

        severity = input(f"Enter new severity (current: {area['severity']}): ").strip()
        if severity.isdigit() and 1 <= int(severity) <= 5:
            area['severity'] = int(severity)

        try:
            distance = input(f"Enter new distance (current: {area['distance']} km): ").strip()
            if distance:
                distance = float(distance)
                if distance >= 0:
                    area['distance'] = distance
        except ValueError:
            print("Invalid distance input. Keeping the current value.")

        print("Enter updated resource quantities (leave blank to keep current values):")
        for supply in area['supplies']:
            try:
                quantity = input(f"Enter new quantity for {supply} (current: {area['supplies'][supply]}): ").strip()
                if quantity:
                    quantity = int(quantity)
                    if quantity >= 0:
                        area['supplies'][supply] = quantity
            except ValueError:
                print(f"Invalid input for {supply}. Keeping the current value.")

        print(f"Flood area '{area['name']}' updated successfully.")
        pause()

    def delete_area(self, datasystem):
        clear_screen()
        print("\nDeleting a flood-affected area...")
        self.view_areas(datasystem)

        try:
            index = int(input("Enter the index of the area to delete(or 0 to exit): ").strip()) - 1
            if index == -1:
                return
            if index < 0 or index >= len(datasystem.flood_areas):
                print("Invalid selection. Please try again.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        area = datasystem.flood_areas.pop(index)
        print(f"Flood area '{area['name']}' deleted successfully.")
        pause()

    def dashboard(self, datasystem):
        while True:
            clear_screen()
            print("\nFlood Affected Area Dashboard:")
            print("1. View Flood Areas")
            print("2. Add New Flood Area")
            print("3. Edit Flood Area")
            print("4. Delete Flood Area")
            print("5. Exit to Main Menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.view_areas(datasystem)
            elif choice == "2":
                self.add_area(datasystem)
            elif choice == "3":
                self.edit_area(datasystem)
            elif choice == "4":
                self.delete_area(datasystem)
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select a valid option.")

class SupplyManagement:
    def __init__(self):
        self.supplies = []
        self.tracking_number_counter = 1

    def register_supply(self, datasystem):
        clear_screen()
        print("\nRegistering new supply...")
        
        print("Available Flood-Affected Areas:")
        for index, area in enumerate(datasystem.flood_areas, start=1):
            print(f"{index}. {area['name']} (Severity: {area['severity']})")

        try:
            area_choice = int(input("Select the index of the flood-affected area for the supply: ")) - 1
            if area_choice < 0 or area_choice >= len(datasystem.flood_areas):
                print("Invalid selection. Please try again.")
                return
            selected_area = datasystem.flood_areas[area_choice]
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        supply_types = ["shelter", "food", "medicine", "clothes"]
        print("Choose a supply type:")
        for idx, supply in enumerate(supply_types, 1):
            print(f"{idx}. {supply.capitalize()}")
        
        try:
            choice = int(input("Enter the number corresponding to the supply type: ").strip())
            if choice < 1 or choice > len(supply_types):
                print("Invalid choice. Please try again.")
                return
            supply_type = supply_types[choice - 1]
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        try:
            quantity = int(input(f"Enter the quantity for {supply_type}: ").strip())
            if quantity <= 0:
                print("Quantity must be a positive number.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        tracking_number = f"S{self.tracking_number_counter:05}"
        self.tracking_number_counter += 1

        self.supplies.append({
            "type": supply_type,
            "quantity": quantity,
            "tracking_number": tracking_number,
            "area": selected_area['name'],
            "severity": selected_area['severity']
        })

        print(f"Supply registered successfully with Tracking Number: {tracking_number}")

        transportation_cost = self.calculate_transportation_cost(selected_area['severity'], quantity)
        print(f"Transportation Cost for this supply: ${transportation_cost:.2f}")
        pause()

    def calculate_transportation_cost(self, severity, quantity):
        base_cost_per_item = 10
        return base_cost_per_item * severity * quantity

    def track_supply(self):
        clear_screen()
        print("\nTracking supplies...")
        
        if not self.supplies:
            print("No supplies have been registered yet.")
            pause()
            return

        print("Registered Supplies:")
        for idx, supply in enumerate(self.supplies, 1):
            print(f"{idx}. Type: {supply['type'].capitalize()}, Quantity: {supply['quantity']}, Tracking Number: {supply['tracking_number']}, Area: {supply['area']}, Severity: {supply['severity']}")

        try:
            supply_index = int(input("Enter the number of the supply to view details: ").strip()) - 1
            if supply_index < 0 or supply_index >= len(self.supplies):
                print("Invalid selection. Please try again.")
                pause()
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            pause()
            return

        selected_supply = self.supplies[supply_index]
        print(f"Tracking Supply: {selected_supply['type'].capitalize()}")
        print(f"Quantity: {selected_supply['quantity']}, Tracking Number: {selected_supply['tracking_number']}, Area: {selected_supply['area']}, Severity: {selected_supply['severity']}")
        pause()

    def dashboard(self, datasystem):
        while True:
            clear_screen()
            print("\nSupply Management Dashboard:")
            print("1. Register Supply")
            print("2. Exit to Main Menu")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.register_supply(datasystem)
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please select a valid option.")

# Main program
datasystem = Datasystem()
flood_ops = FloodAffected()
supply_ops = SupplyManagement()
admin_instance = Admin()

volunteer1 = Volunteer("volunteer1", "password1", "volunteer1@example.com", ["first aid", "logistics"])
volunteer2 = Volunteer("volunteer2", "password2", "volunteer2@example.com", ["cooking", "shelter management"])

authority = Authority("authority1", "password3", "authority@example.com", "Relief Organization")

datasystem.add_profile(volunteer1)
datasystem.add_profile(volunteer2)
datasystem.add_profile(authority)

flood_area1 = {
    "name": "Area A",
    "severity": 5,
    "distance": 10.0,
    "supplies": {
        "shelter": 50,
        "food": 200,
        "medicine": 30,
        "clothes": 100
    }
}

flood_area2 = {
    "name": "Area B",
    "severity": 3,
    "distance": 15.0,
    "supplies": {
        "shelter": 20,
        "food": 100,
        "medicine": 10,
        "clothes": 50
    }
}

flood_area3 = {
    "name": "Area C",
    "severity": 4,
    "distance": 5.0,
    "supplies": {
        "shelter": 30,
        "food": 150,
        "medicine": 20,
        "clothes": 80
    }
}

datasystem.add_flood_area(flood_area1)
datasystem.add_flood_area(flood_area2)
datasystem.add_flood_area(flood_area3)

while True:
    clear_screen()
    print("\n--- Flood Management System ---")
    print("1. Register Account")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        account_type = input("Choose account type (Volunteer /Authority): ").strip().lower()

        username = input("Enter username: ").strip()

        if account_type == "volunteer":
            volunteer = Volunteer(username, "", "", [])  # Password is empty initially
            volunteer.register(datasystem)
        elif account_type == "authority":
            organization_name = input("Enter organization name: ").strip()
            authority = Authority(username, "", "", organization_name)  # Password is empty initially
            authority.register(datasystem)
        else:
            print("Invalid account type. You can only register as Volunteer or Authority.")

    elif choice == "2":
        user = datasystem.login()
        if user:
            if user.type.lower() == "volunteer":  # Ensure case-insensitive check
                volunteer.dashboard(flood_ops, datasystem)
            elif user.type.lower() == "authority":  # Ensure case-insensitive check
                authority.dashboard(flood_ops, datasystem, supply_ops)  # Use the existing authority instance
            elif user.type.lower() == "admin":  # Ensure case-insensitive check
                admin_instance.dashboard(flood_ops, datasystem, supply_ops)  # Use the instance created
    elif choice == "3":
        print("Exiting the Flood Management System....")
        break
    else:
        print("Invalid choice. Please select a valid option.")
