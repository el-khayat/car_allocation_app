
/***
Note ✅
Check out the github repository to see tje full project 
                    https://github.com/el-khayat/car_allocation_app


to clone the project   
                    https://github.com/el-khayat/car_allocation_app.git
****/


## Car Agency Management Project

### Overview
The Car Allocation  Agency Management project is a Python application designed to manage client information, 
car details, and car allocations for a car agency. 
It provides basic CRUD (Create, Read, Update, Delete) operations for the Client, Car, and Allocation classes. 
The user can choose to work with either a SQLite database version (script_sqlite3.py) or a text file-based version  (script_file.py).

### Project Structure

The project is structured as follows: 

- `script_sqlite3.py`: Contains the main script for the SQLite version.
- `car_allocation.db`: SQLite database file (used by the SQLite version).
- `script_file.py`: Contains the main script for the text file-based version.
- `car.txt`: used to store car informations.
- `client.txt`: used to store client informations.
- `allocation.txt`: used to store allocation informations.


### Usage

   python script_sqlite3.py

            the system will ask you if you want to manage the clients, cars or allocation information
            whene you select your choise then will ask you what operations you want to do (CRUD operations)

            NOTE : the system will use SQLite to store the informations
   
   python script_file.py
            The same thing as the SQLite version but the system will store the informations in a text files
            Note : you can open the text file when you test the  "script_file.py" to to test and see the changes at the same time


