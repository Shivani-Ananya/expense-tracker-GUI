import sqlite3
conn = sqlite3.connect("expense_tracker.db")

cursor = conn.cursor()

cursor.execute ('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT NOT NULL
            )
    ''')
conn.commit()


while True:
    print("\n==== Options =====")
    print("1. Add")
    print("2. View")
    print("3. Delete")
    print("4. Filter View")
    print("5. Exit")

    choice = input("Enter your choice (1-4): ").strip()
    if choice == '1':
        user_date = input("Enter Date (YYYY-MM-DD): ")
        user_category = input("Enter Category: ")
        user_amount = float(input("Enter Your amount: "))
        user_note = input("Enter note: ")

        cursor.execute ('''
            INSERT INTO expenses (date, category, amount, note)
            VALUES (?, ?, ?, ?)
        ''', (user_date, user_category, user_amount, user_note))

        conn.commit()
        print("Your records have been collected successfuly!")
        
    elif choice == '2':
        cursor.execute ('''
                        SELECT * FROM expenses
                        ORDER BY date DESC
                        ''')
        records = cursor.fetchall()
        print("\n Your Expenses (Most Recent First):")
        total = 0
        for record in records:
                total += record[3]
                print(f"ID: {record[0]} | date: {record[1]} | Category: {record[2]} | Amount: ₹{record[3]} | Note: {record[4]}")
                print(f"\n Tota Expenses:  ₹{total}")
                    
    elif choice == '3':
        delete_id = input("Enter the ID of expense to Delete: ")
        cursor.execute  ('''
                DELETE FROM expenses
                WHERE id = ?
                ''', (delete_id,))
        conn.commit()
        print(f"Expense with Id {delete_id} deleted Successfully!")

    elif choice == '4':
        while True:
            print("1. View by Date")
            print("2. View by Category")
            print("3. Back")

            select = input("Enter your choice (1-3): ").strip()
            if select=='1':
                enter_date = input("Enter the search date (YYYY-MM-DD): ")
                cursor.execute ('''
                        SELECT * FROM expenses
                        WHERE date = ?
                        ''', (enter_date,))
                data = cursor.fetchall()
                if data:
                    for row in data:
                        print(row)
                else:
                    print("No matching records are found!")

            elif select=='2':
                enter_category = input("Enter the Category to Search: ")
                cursor.execute ('''
                        SELECT * FROM expenses
                        WHERE category = ?
                        ''', (enter_category,))
                data = cursor.fetchall()
                if data:
                    for row in data:
                        print(row)
                else:
                    print("No matching records are found!")

            elif select == '3':
                print("Exiting filter view!")
                break
            else:
                print("Invalid Choice!")
                           
            
    elif choice == '5':
         print("Exiting... Bye boss")
         break

    else:
        print("Invalid choice! Try again.")

conn.close()   
