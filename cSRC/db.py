import sqlite3
from datetime import datetime

class Contract:
    route = 'db.sqlite3'

    def __init__(self, id:int , contract:str ,date_created:datetime,pings=0,latest_block=0,total_calls=0,total_buy=0):
        self.id = id
        self.contract = contract
        self.date_created = date_created
        self.pings = pings
        self.latest_block =latest_block
        self.total_calls = total_calls
        self.total_buy = total_buy

    def create(self):
        conn = sqlite3.connect(Contract.route)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO contract_data (id , contract , date_created ,pings,latest_block,total_calls,total_buy)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.id,
              self.contract,
              self.date_created,
              self.pings,
              self.latest_block,
              self.total_calls,
              self.total_buy))

        conn.commit()
        conn.close()

    @staticmethod
    def get_user_by_id(id):
        conn = sqlite3.connect(Contract.route)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contract_data WHERE id = ?', (id,))
        result = cursor.fetchone()

        if result:
            (id, contract , date_created ,pings,latest_block,total_calls,total_buy) = result

            user = Contract(
                id=id,
                contract=contract,
                date_created=date_created,
                pings=pings,
                latest_block=latest_block,
                total_calls=total_calls,
                total_buy=total_buy
            )

            conn.close()
            return user

        conn.close()
        return None

    def save(self):
        conn = sqlite3.connect(Contract.route)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE contract_data SET
            contract=? , date_created=? ,pings=?,latest_block=?,total_calls=?,total_buy=?
            WHERE id=?
        ''', (
              self.contract,
              self.date_created,
              self.pings,
              self.latest_block,
              self.total_calls,
              self.total_buy,
              self.id
            ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_users():
        conn = sqlite3.connect(Contract.route)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contract_data')
        results = cursor.fetchall()

        users = []
        for result in results:
            (id, contract , date_created ,pings,latest_block,total_calls,total_buy) = result

            user = Contract(
                id=id,
                contract=contract,
                date_created=date_created,
                pings=pings,
                latest_block=latest_block,
                total_calls=total_calls,
                total_buy=total_buy
            )

            users.append(user)

        conn.close()
        return users

    @staticmethod
    def query_database(field_name, field_data):
        conn = sqlite3.connect(Contract.route)
        cursor = conn.cursor()

        query = f"SELECT * FROM contract_data WHERE {field_name} = ?;"
        cursor.execute(query, (field_data,))
        rows = cursor.fetchall()
        r = []
        for row in rows:
            (id, contract , date_created ,pings,latest_block,total_calls,total_buy) = row
            contract__ = Contract(
                    id=id,
                    contract=contract,
                    date_created=date_created,
                    pings=pings,
                    latest_block=latest_block,
                    total_calls=total_calls,
                    total_buy=total_buy
                )
            conn.close()
            r.append(contract__)

        def first():
            return r[0]

        return r 
    def delete(self):
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM contract_data WHERE id = ?', (self.id,))

        conn.commit()
        conn.close()
