from contextlib import contextmanager
import logging
import mysql.connector
from logger import setup_logger

logger=setup_logger('db_helper.py')

@contextmanager
def get_db_cursor(commit=False):
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )
    #
    # if connection.is_connected():
    #     print("Connection successful")
    # else:
    #     print("Failed in connecting")

    cursor=connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with{expense_date}")
    with get_db_cursor() as cursor:

        cursor.execute(f"select * from expenses where expense_date = %s",(expense_date,))
        expenses=cursor.fetchall()

        return expenses


def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses(expense_date,amount,category,notes) values(%s,%s,%s,%s)",(expense_date,amount,category,notes)
        )
def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("Delete from expenses where expense_date=%s",(expense_date,)
                       )
def fetch_monthly_expense_summary():
    logger.info(f"fetch_expense_summary_by_months")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT month(expense_date) as expense_month, 
               monthname(expense_date) as month_name,
               sum(amount) as total FROM expenses
               GROUP BY expense_month, month_name;
            '''
        )
        data = cursor.fetchall()
        return data

def fetch_expense_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start:{start_date} end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
        '''select category,sum(amount) as total
	from expenses where expense_date between
    %s and %s
    group by category''',(start_date,end_date)
        )
        data =cursor.fetchall()
        return data

if __name__=="__main__":
    print(fetch_expense_summary("2024-08-01","2024-08-20"))