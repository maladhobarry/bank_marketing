import pandas as pd
from bank_marketing.sqlite_db.generics import create_connection


class BankMarketingDAL:
    def __init__(self, db_file):
        conn = create_connection(db_file)
        self.campaign_missions = CampaignMission(conn)
        self.customers = Customer(conn)
        self.loans = Loan(conn)
        self.mortgages = Mortgage(conn)


class CampaignMission:
    def __init__(self, conn):
        self.conn = conn
        self.attrs = [
            "comm_date",
            "comm_year",
            "comm_month",
            "comm_day",
            "comm_type",
            "curr_outcome",
            "comm_duration",
            "curr_n_contact",
            "days_since_last_campaign",
            "last_n_contact",
            "last_outcome",
            "customer_id",
        ]

    def insert(self, campaign_mission, commit=True):
        """Insert a new campaign_mission"""
        sql = """ INSERT INTO campaignMissions(customer_id,comm_date,comm_type,comm_month,comm_day,curr_n_contact,days_since_last_campaign,last_n_contact,last_outcome,comm_duration,curr_outcome,comm_year)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, campaign_mission)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def fetch_all_done(self, to_dict=False, to_dataframe=False):
        """Query all rows in the campaignMissions table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT comm_date,comm_year,comm_month,comm_day,comm_type,curr_outcome,comm_duration,curr_n_contact,days_since_last_campaign,last_n_contact,last_outcome,customer_id \
                    FROM campaignMissions WHERE comm_duration IS NOT NULL AND curr_outcome IS NOT NULL"
        )

        rows = cur.fetchall()
        if to_dict:
            return [{k: v for k, v in zip(self.attrs, row)} for row in rows]
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_all_not_done(self, to_dict=False, to_dataframe=False):
        """Query all rows in the campaignMissions table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT comm_date,comm_year,comm_month,comm_day,comm_type,curr_outcome,comm_duration,curr_n_contact,days_since_last_campaign,last_n_contact,last_outcome,customer_id\
                    FROM campaignMissions WHERE comm_duration IS NULL AND curr_outcome IS NULL"
        )

        rows = cur.fetchall()
        if to_dict:
            return [{k: v for k, v in zip(self.attrs, row)} for row in rows]
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_by_date(self, date, to_dict=False, to_dataframe=False):
        """Query all rows in the campaignMissions table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT comm_date,comm_year,comm_month,comm_day,comm_type,curr_outcome,comm_duration,curr_n_contact,days_since_last_campaign,last_n_contact,last_outcome,customer_id \
                    FROM campaignMissions WHERE comm_date=?",
            (date,),
        )

        rows = cur.fetchall()
        if to_dict:
            return [{k: v for k, v in zip(self.attrs, row)} for row in rows]
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_all(self, to_dict=False, to_dataframe=False):
        """Query all rows in the campaignMissions table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT comm_date,comm_year,comm_month,comm_day,comm_type,curr_outcome,comm_duration,curr_n_contact,days_since_last_campaign,last_n_contact,last_outcome,customer_id \
                     FROM campaignMissions"
        )

        rows = cur.fetchall()
        if to_dict:
            return [{k: v for k, v in zip(self.attrs, row)} for row in rows]
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows


class Customer:
    def __init__(self, conn):
        self.conn = conn
        self.attrs = ["id", "first_name", "last_name", "email", "phone", "age", "job", "marital", "education"]

    def insert(self, customer, commit=True):
        """Insert a new customer"""
        sql = """ INSERT INTO customers(id,first_name,last_name,email,phone,age,job,marital,education)
                VALUES(?,?,?,?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, customer)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def fetch_all(self, to_dict=False, to_dataframe=False):
        """Query all rows in the customers table"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM customers")

        rows = cur.fetchall()
        if to_dict:
            return [{k: v for k, v in zip(self.attrs, row)} for row in rows]
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_one(self, id, to_dict=False):  # noqa
        """Query all rows in the customers table"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM customers WHERE id=?", (id,))

        row = cur.fetchone()
        if to_dict:
            return {k: v for k, v in zip(self.attrs, row)}
        return row


class Loan:
    def __init__(self, conn):
        self.conn = conn
        self.attrs = ["status", "start_date", "due_date", "amount_due", "default_penalties", "customer_id"]

    def insert(self, loan, commit=True):
        """Insert a new loan"""
        sql = """ INSERT INTO loans(customer_id,status,start_date,due_date,amount_due,default_penalties)
                VALUES(?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, loan)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def fetch_by_customer(self, customer_id, to_dataframe=False):
        """Query all rows in the loans table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT status,start_date,due_date,amount_due,default_penalties,customer_id \
                     FROM loans WHERE customer_id=?",
            (customer_id,),
        )

        rows = cur.fetchall()
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_all(self, to_dataframe=False):
        """Query all rows in the loans table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT status,start_date,due_date,amount_due,default_penalties,customer_id \
                     FROM loans"
        )

        rows = cur.fetchall()
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows


class Mortgage:
    def __init__(self, conn):
        self.conn = conn
        self.attrs = ["status", "start_date", "due_date", "amount_due", "default_penalties", "customer_id"]

    def insert(self, mortgage, commit=True):
        """Insert a new mortgage"""
        sql = """ INSERT INTO mortgages(customer_id,status,start_date,due_date,amount_due,default_penalties)
                VALUES(?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, mortgage)
        if commit:
            self.conn.commit()
        return cur.lastrowid

    def fetch_by_customer(self, customer_id, to_dataframe=False):
        """Query all rows in the mortgages table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT status,start_date,due_date,amount_due,default_penalties,customer_id \
                    FROM mortgages WHERE customer_id=?",
            (customer_id,),
        )

        rows = cur.fetchall()
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows

    def fetch_all(self, to_dataframe=False):
        """Query all rows in the mortgages table"""
        cur = self.conn.cursor()
        cur.execute(
            "SELECT status,start_date,due_date,amount_due,default_penalties,customer_id \
                     FROM mortgages"
        )

        rows = cur.fetchall()
        if to_dataframe:
            return pd.DataFrame(rows, columns=self.attrs)
        return rows
