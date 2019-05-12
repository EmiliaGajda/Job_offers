import pymysql

login = input("Login: ").lower()
haslo = input("Hasło: ").lower()

class DBConect:

    def __init__(self):

        try: #próbuje czy kod działa jak nie działa to przechodzi do except
            HOST        = "localhost"
            USER        = "root"
            HASLO       = "Piwniczanka12!"
            BAZA_DANYCH = "job_offers_db"

            # conn = pymysql.connect(HOST, port = 3306, User... - kiedy zmieniamy port bo się np wywali

            #data = config.read_data()
            #self.conn = pymysql.connect(data["host"], data["user"], data["haslo"], data["baza"], charset="utf8")

            self.conn = pymysql.connect(HOST, USER, HASLO, BAZA_DANYCH, charset="utf8")
            self.entry()
            self.conn.close()

        except pymysql.MySQLError:
            print("Incorrect connection data")

    def entry(self):
        reg_log = input("Do you want to register or logged? R-registration L-Login Q-Quit ").upper()

        if reg_log == "R":
            self.registration()
        elif reg_log == "L":
            self.login()
        elif reg_log == "Q":
            exit()
        else:
            print("Choose correct option")
            self.entry()

    def registration(self):
        global login
        global haslo
        role = input("What's your role? admin/user? ").lower()
        self.kursor = self.conn.cursor()

        if self.finding_login() == ():
            self.kursor.execute("INSERT INTO users_admins (login, password, role) VALUES (%s, %s, %s)", (login, haslo, role))
            print("ok, registered: ", login, " as ", role)
            self.conn.commit()
            if role == "admin":
                self.menu_admin()
            if role == "user":
                self.menu_user()
        else:
            print("User ", login, "already exist")
            self.entry()

    def finding_login(self):
        self.kursor.execute("SELECT login FROM users_admins WHERE login = %s", login)
        found_login = self.kursor.fetchall()
        return found_login

    def login(self):
        global login
        global haslo

        self.kursor = self.conn.cursor()

        self.kursor.execute("SELECT * FROM users_admins WHERE login = %s and password = %s", (login, haslo))
        #pobierz wyniki zapytania select do zmiennej results
        results = self.kursor.fetchall()

        if (len(results) == 1):
            print("OK, logged: ", results[0] [1], "as ", results[0] [3])
            if (results[0][3]) == "admin":
                self.menu_admin()

            if (results[0][3]) == "user":
                self.menu_user()
        else:
            print("Incorrect login or password OR unregistered user/admin")

    def menu_admin(self):
        dec = input("What you want to do? S - Show offers, A - Add offer, D-delete offer, Q - exit ").upper()
        if dec == "S":
            self.select()
            self.login()
        elif dec == "A":
            self.add_offer()
        elif dec == "D":
            self.delete_offer()
        elif dec == "Q":
            exit()
        else:
            print("Wrong choice")
            self.menu_admin()

    def menu_user(self):
        dec = input("What you want to do? S - show, Q - quit ").upper()
        if dec == "S":
            show = input("Show: A - all, O - options, K-skills, C-cities ").upper()
            if show == "A":
                self.select()
                self.login()
            elif show == "O":
                self.options()
            elif show == "K":
                self.skills()
            elif show == "C":
                self.cities()
            else:
                print("Wrong choice")
                self.menu_user()
        elif dec == "Q":
            exit()
        else:
            print("Wrong choice")
            self.menu_user()

    def options(self):
        country      = input("Country (you can press Enter to go to the next option): ").capitalize()
        city         = input("City (you can press Enter to go to the next option): ").capitalize()
        earnings_min = input("Earnings min (you can press Enter to go to the next option): ")
        earnings_max = input("Earnings max (you can press Enter to go to the next option): ")
        skill        = input("Skill (you can press Enter to go to the next option): ")

        self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND city = %s AND earnings BETWEEN %s AND %s AND skill_name = %s", (country, city, earnings_min, earnings_max, skill))
        options_user = self.kursor.fetchall()
        for option in options_user:
            print(option)

    """ here should be options includes blank input
    #all fields are filled
        if country and city and earnings_min and earnings_max and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND city = %s AND earnings BETWEEN %s AND %s AND skill_name = %s", (country, city, earnings_min, earnings_max, skill))
            options_user = self.kursor.fetchall()
            for option in options_user:
                print(option)

    #only country isn't filled
        if country == "" and city and earnings_min and earnings_max and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE city = %s AND earnings BETWEEN %s AND %s AND skill_name = %s", (city, earnings_min, earnings_max, skill))
            options_user = self.kursor.fetchall()

            for option in options_user:
                print(option)

    #only city isn't filled
        if city =="" and country and  earnings_min and earnings_max and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND earnings BETWEEN %s AND %s AND skill_name = %s", (country, earnings_min, earnings_max, skill))
            options_user = self.kursor.fetchall()
            for option in options_user:
                print(option)

    #only earnings min isn't filled
        if earnings_min == ""  and country and city and  earnings_max and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND city = %s AND earnings < %s AND skill_name = %s", (country, city, earnings_max, skill))
            options_user = self.kursor.fetchall()
            for option in options_user:
                print(option)

    #only earnings_max isn't filled
        if earnings_max == "" and country and city and earnings_min and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND city = %s AND earnings > %s AND skill_name = %s", (country, city, earnings_min, skill))
            options_user = self.kursor.fetchall()
            for option in options_user:
                print(option)

    #only skill isn't filled
        if country and city and earnings_min and earnings_max and skill != "":
            self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                                "LEFT JOIN job_offers_with_skills "
                                "on offers.id_offer = job_offers_with_skills.id_offer "
                                "LEFT JOIN skills "
                                "on job_offers_with_skills.id_skill = skills.id_skill "
                                "LEFT JOIN companies "
                                "on offers.id_company = companies.id_company "
                                "WHERE country = %s AND city = %s AND earnings BETWEEN %s AND %s AND skill_name = %s", (country, city, earnings_min, earnings_max, skill))
            options_user = self.kursor.fetchall()
            for option in options_user:
                print(option)
                
        self.menu_user()"""

    def skills(self):
        self.kursor.execute("SELECT DISTINCT skill_name FROM skills")
        for skill in self.kursor.fetchall():
            print(skill)
        self.login()

    def cities(self):
        self.kursor.execute("SELECT DISTINCT city FROM companies")
        for city in self.kursor.fetchall():
            print(city)
        self.login()

    def select(self):
        self.kursor.execute("SELECT offers.id_offer, job_position, earnings, company_name, country, city, skill_name FROM offers "
                            "LEFT JOIN job_offers_with_skills "
                            "on offers.id_offer = job_offers_with_skills.id_offer "
                            "LEFT JOIN skills "
                            "on job_offers_with_skills.id_skill = skills.id_skill "
                            "LEFT JOIN companies "
                            "on offers.id_company = companies.id_company")

        offers = self.kursor.fetchall()
        for offer in offers:
           print(offer)

    def add_offer(self):
        title = input("Job position: ").capitalize()
        earnings = input("Earnings (average): ")
        skill_py = input("Main skill: ")
        company_name_py = input("Company name: ")
        country_py = input("Country: ").capitalize()
        city_py = input("City: ").capitalize()

    #company search - if there is no company then adding
        self.kursor.execute("SELECT id_company, country, city FROM companies "
                            "WHERE company_name = %s AND country = %s AND city = %s", (company_name_py, country_py, city_py))
        found_companies = self.kursor.fetchall()
        if found_companies == ():
            self.kursor.execute("INSERT INTO companies (company_name, country, city) "
                                "VALUES (%s, %s, %s)", (company_name_py, country_py, city_py))
            self.conn.commit()
            print("Company has been added")

        self.kursor.execute("SELECT id_company FROM companies "
                            "WHERE company_name = %s", company_name_py)
        found_id_company = self.kursor.fetchall()

    #skills search - if there is no skill then adding
        self.kursor.execute("SELECT id_skill, skill_name FROM skills WHERE skill_name = %s", skill_py)
        found_skills = self.kursor.fetchall()
        if found_skills == ():
           self.kursor.execute("INSERT INTO skills (skill_name) "
                               "VALUES (%s)", skill_py)
           self.conn.commit()
           print("Skill has been added")

        self.kursor.execute("SELECT id_skill FROM skills "
                            "WHERE skill_name = %s", skill_py)
        found_id_skill = self.kursor.fetchall()

        self.kursor.execute("INSERT INTO offers (job_position, id_company, earnings) "
                            "VALUES (%s, %s, %s)", (title, found_id_company, earnings))
        self.conn.commit()

        self.kursor.execute("INSERT INTO job_offers_with_skills (id_offer, id_skill) "
                            "VALUES ((SELECT id_offer FROM offers "
                            "WHERE job_position = %s AND id_company = %s AND earnings = %s), %s)",
                            (title, found_id_company, earnings, found_id_skill))
        print("Added job offer as ", title, "with", skill_py, "in ", company_name_py, city_py)
        self.conn.commit()
        self.menu_admin()

    def delete_offer(self):
        self.select()
        offer_id = int(input("Offer ID: "))
        self.kursor.execute("DELETE FROM job_offers_with_skills WHERE id_offer = %s", offer_id)
        self.kursor.execute("DELETE FROM offers WHERE id_offer = %s", offer_id)

        remove = input("Are you sure to delete this offer? Y/N").upper()
        if remove == "Y":
            self.conn.commit()
            print("Offer removed")
            self.menu_admin()
        elif remove == "N":
            print("Not removed")
            self.conn.rollback()
            self.menu_admin()
        else:
            print("Not removed. Try again (wrong decision")
            self.delete_offer()

    """
    def searching_companies(self):
        self.kursor.execute("SELECT id_company, country, city FROM companies "
                            "WHERE company_name = %s AND country = %s AND city = %s", (company_name_py, country_py, city_py))
        found_companies = self.kursor.fetchall()
        return found_companies

    def searching_skills(self):
        self.kursor.execute("SELECT id_skill, skill_name FROM skills WHERE skill_name = %s", skill_py)
        found_skills = self.kursor.fetchall()
        return found_skills
    """


db = DBConect()