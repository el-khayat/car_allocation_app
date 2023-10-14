class Allocation:
    def __init__(self, allocation_id, allocation_date, allocation_price, allocation_nbr_days, client_id, car_id):
        self.id = allocation_id
        self.date = allocation_date
        self.price = allocation_price
        self.nbr_days = allocation_nbr_days
        self.client_id = client_id
        self.car_id = car_id

    def save(self):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO allocations (date, price, nbr_days, client_id, car_id) VALUES (?, ?, ?, ?, ?)",
                       (self.date, self.price, self.nbr_days, self.client_id, self.car_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def update(self):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE allocations SET date=?, price=?, nbr_days=?, client_id=?, car_id=? WHERE id=?",
                       (self.date, self.price, self.nbr_days, self.client_id, self.car_id, self.id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, allocation_id):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM allocations WHERE id=?", (allocation_id,))
        conn.commit()
        conn.close()

    @classmethod
    def get_all_allocations(cls):
        conn = sqlite3.connect('db/car_allocation_db.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM allocations")
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

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