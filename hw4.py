import sqlite3
import csv # Use this to read the csv file


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
        
    Parameters
    ----------
    Connection
    """
    con = sqlite3.connect(db_file)
    return con
'''    
connect = create_connection('B7_DB.db')
curr = connect.cursor()
curr.execute("SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee LEFT OUTER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE (datetime('now')-Employee.BirthDate)>=50")
for row in curr:
    eid=row[0]
    print(eid)
    curr.execute("Update ConstructorEmployee Set SalaryPerDay=? WHERE ConstructorEmployee.EID=?;",(100,eid,))
    connect.commit()
    print(row)

'''
def update_employee_salaries(conn, increase):
    """

    Parameters
    ----------
    conn: Connection
    increase: float
    """
    #over_50 = "SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee INNER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE ((strftime('%Y', 'now') + strftime('%j', 'now') / 365.2422) - (strftime('%Y', Employee.BirthDate) + strftime('%j', Employee.BirthDate) / 365.2422)AS INT)>50"
    over50="SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee LEFT OUTER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE (datetime('now')-Employee.BirthDate)>=50"
    str_raise="Update ConstructorEmployee Set SalaryPerDay=?"# WHERE ConstructorEmployee.EID=?;"
    cur = conn.cursor()
    raise_by = increase/100#if its 3% make it 0.03
    cur1=cur.execute(over50)
    for emp in cur1:
        updated_sal = emp[-1] + (emp[-1]*(increase/100))
        eid=emp[0]
        cur.execute("Update ConstructorEmployee Set SalaryPerDay=? WHERE ConstructorEmployee.EID=?;",(updated_sal,eid,))
    conn.commit()
    #return
    
'''
curr.execute("SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee LEFT OUTER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE (datetime('now')-Employee.BirthDate)>=50")
for row in curr:
    eid=row[0]
    print(eid)
    curr.execute("Update ConstructorEmployee Set SalaryPerDay=? WHERE ConstructorEmployee.EID=?;",(100,eid,))
    curr.execute("Update ConstructorEmployee Set SalaryPerDay=? WHERE ConstructorEmployee.EID=?;",(100,eid,))
    connect.commit()
    print(row)


update_employee_salaries(connect, 3)

curr.execute("SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee LEFT OUTER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE (datetime('now')-Employee.BirthDate)>=50")
for row in curr:
    eid=row[0]
    print(eid)
    curr.execute("Update ConstructorEmployee Set SalaryPerDay=? WHERE ConstructorEmployee.EID=?;",(100,eid,))
    connect.commit()
    print(row)
'''

def get_employee_total_salary(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    int
    """
    cur = conn.cursor()
    salary_sum = "SELECT SalaryPerDay from ConstructorEmployee"
    con_salary = cur.execute(salary_sum)
    total_salary = 0 
    for i in con_salary:
        total_salary = total_salary + i[0]
    
    #print(total_salary)
    return total_salary


def get_total_projects_budget(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    float
    """
    cur = conn.cursor()
    budget_sum = "SELECT Budget FROM Project"
    con_budget = cur.execute(budget_sum)
    total_budget = 0 
    for i in con_budget:
        total_budget = total_budget + i[0]
        
    #print(total_budget)
    return total_budget
    


def calculate_income_from_parking(conn, year):
    """
    Parameters
    ----------
    conn: Connection
    year: str

    Returns
    -------
    float
    """
    cur = conn.cursor()
    costs_per_car = cur.execute("SELECT Cost FROM CarParking WHERE StartTime like ?", (year+"%",))
    income = 0
    for i in costs_per_car:
        income = income + i[0]
    #print (income)
    return income


def get_most_profitable_parking_areas(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    list[tuple]

    """
    cur = conn.cursor()
    best_park = cur.execute("SELECT AID AS ParkingAreaID , sum(Cost) AS Income FROM CarParking GROUP BY AID ORDER BY Income DESC , AID DESC")
    tuple_parking_list = []
    for i in best_park:
        tuple_parking_list.append(i)
    what_we_need = tuple_parking_list[0:5]
    return what_we_need
        

def get_number_of_distinct_cars_by_area(conn):
    """
    Parameters
    ----------
    conn: Connection

    Returns
    -------
    list[tuple]

    """
    cur = conn.cursor()
    car_numbers = cur.execute("SELECT AID  AS ParkingAreaID , count(DISTINCT(CID)) AS DistinctCarNumber FROM CarParking GROUP BY AID ORDER BY DistinctCarNumber DESC")
    #print(car_numbers.fetchall())
    return car_numbers.fetchall()

def add_employee(conn, eid, firstname, lastname, birthdate, street_name, number, door, city):
    """
    Parameters
    ----------
    conn: Connection
    eid: int
    firstname: str
    lastname: str
    birthdate: datetime
    street_name: str
    number: int
    door: int
    city: str
    """
    #cur = conn.cursor()
    #cur.excute("INSERT into [Employee] ([EID],[FirstName], [LastName],[BirthDate], [StreetName], [Number], [Door], [City]) VALUES (?,?,?,?,?,?,?,?)" , (eid , firstname, lastname , birthdate , street_name , number , door ,city))
    

def load_neighborhoods(conn, csv_path):
    """

    Parameters
    ----------
    conn: Connection
    csv_path: str
    """
    sql_query = "INSERT OR IGNORE INTO Neighborhood (NID,Name) VALUES (?,?)"
    cur = conn.cursor()
    with open(csv_path,'r') as csv_file:
        reader = csv.reader(csv_file)
        #next(reader) - no headline
        for line in reader:
            cur.execute(sql_query,(line[0],line[1]))
        conn.commit()
    return


#
#connection = create_connection('B7_DB.db')
#cur = connection.cursor()
##sala = cur.execute("SELECT SalaryPerDay from ConstructorEmployee")
##total_sala = 0 
##for i in sala:
##    total_sala = total_sala + int(i[0])
##    print(total_sala)
##get_employee_total_salary(connection)
#
##get_total_projects_budget(connection)
#
##calculate_income_from_parking(connection," 2019")
##get_number_of_distinct_cars_by_area(connection)
#get_most_profitable_parking_areas(connection)
#update_employee_salaries(connection, 3)
#emp = cur.execute("SELECT ConstructorEmployee.* FROM ConstructorEmployee")
#emp1 = cur.execute("SELECT Employee.* FROM Employee")
#check = cur.execute("SELECT Employee.* , ConstructorEmployee.CompanyName,ConstructorEmployee.SalaryPerDay FROM Employee LEFT OUTER JOIN ConstructorEmployee ON Employee.EID=ConstructorEmployee.EID WHERE (strftime('%Y', 'now') + strftime('%j', 'now') / 365) - (strftime('%Y', Employee.BirthDate) + strftime('%j', Employee.BirthDate) / 365)>=50")
#nei = cur.execute("SELECT * FROM Neighborhood")
#print("Before")
#for i in nei:
#    print (i)
#load_neighborhoods(connection,'neighborhoods.csv')
#cur = connection.cursor()
#nei = cur.execute("SELECT * FROM Neighborhood")

#print("After")
#for i in nei:
#    print (i)
#connection.close();