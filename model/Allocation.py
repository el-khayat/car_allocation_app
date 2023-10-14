import sqlite3

class Allocation:
    def __init__(self, allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id):
        self.id = allocation_id
        self.date = allocation_date
        self.price = allocation_price
        self.nbr_days = allocation_nbr_days
        self.client_id = client_id
        self.car_id = car_id

  #----------------------------------------------save  in database and file-----------------------------------------------------      

    def save(self):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO allocations (date, price, nbr_days, client_id, car_id) VALUES (?, ?, ?, ?, ?)",
                       (self.date, self.price, self.nbr_days, self.client_id, self.car_id))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()


    def save_file(self):
            with open('data/allocations.txt', 'a') as file:
                allocation_data = f"{self.id},{self.date},{self.price},{self.nbr_days},{self.client_id},{self.car_id}\n"
                file.write(allocation_data)

  #---------------------------------------------------------------------------------------------------      
  #-------------------------------------------Update in databse and in file--------------------------------------------------------      
    def update(self):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE allocations SET date=?, price=?, nbr_days=?, client_id=?, car_id=? WHERE id=?",
                       (self.date, self.price, self.nbr_days, self.client_id, self.car_id, self.id))
        conn.commit()
        conn.close()

    def update_file(self):
            with open('data/allocations.txt', 'r') as file:
                lines = file.readlines()
            with open('data/allocations.txt', 'w') as file:
                for line in lines:
                    data = line.split(',')
                    if int(data[0]) == self.id:
                        line = f"{self.id},{self.date},{self.price},{self.nbr_days},{self.client_id},{self.car_id}\n"
                    file.write(line)
  #---------------------------------------------------------------------------------------------------      
  #----------------------------------------------delete in database and file-----------------------------------------------------      
    @classmethod
    def delete(cls, allocation_id):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM allocations WHERE id=?", (allocation_id,))
        conn.commit()
        conn.close()

    @classmethod
    def delete_file(cls, allocation_id):
        with open('data/allocations.txt', 'r') as file:
            lines = file.readlines()

        with open('data/allocations.txt', 'w') as file:
            for line in lines:
                data = line.split(',')
                if int(data[0]) != int(allocation_id):  # Convert allocation_id to an integer
                    file.write(line)

  #---------------------------------------------------------------------------------------------------      
  #----------------------------------------get all in database and file-----------------------------------------------------------      
    @staticmethod
    def get_all_allocations():
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM allocations")
        rows = cursor.fetchall()
        conn.close()

        allocations = []
        for row in rows:
            allocation = Allocation(row[0], row[1], row[2], row[3], row[4], row[5])
            allocations.append(allocation)

        return allocations
    @classmethod
    def get_all_allocations_file(cls):
        allocations = []
        with open('data/allocations.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                allocations.append(cls(int(data[0]), data[1], float(data[2]), int(data[3]), int(data[4]), int(data[5])))
        return allocations


  #---------------------------------------------------------------------------------------------------      
  #----------------------------------------get by id in database and file-----------------------------------------------------------      
    @classmethod
    def get_allocation_by_id(cls, allocation_id):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM allocations WHERE id=?", (allocation_id,))
        row = cursor.fetchone()
        conn.close()
        if row is not None:
            return cls(*row)
        else:
            return None


    @classmethod
    def get_allocation_by_id_file(cls, allocation_id):
        with open('data/allocations.txt', 'r') as file:
            for line in file:
                data = line.strip().split(',')
                if int(data[0]) == int(allocation_id):
                    return cls(int(data[0]), data[1], float(data[2]), int(data[3]), int(data[4]), int(data[5]))
        return None

  #---------------------------------------------------------------------------------------------------      