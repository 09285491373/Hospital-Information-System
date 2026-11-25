import mysql.connector


def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Revup123",  # 👈 Your password
            database="mydb",
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None


def view_report():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Added m.patient_type to the SELECT query
            query = """
                SELECT p.patient_id, p.first_name, p.last_name, m.diagnosis, m.treatment, m.patient_type 
                FROM patients p
                LEFT JOIN medical_records m ON p.patient_id = m.patient_id
                """
            cursor.execute(query)
            results = cursor.fetchall()

            print("\n--- Patient Summary Report ---")
            for row in results:
                print(
                    f"ID: {row[0]} | Name: {row[1]} {row[2]} | Diagnosis: {row[3]} | Treatment: {row[4]} | Type: {row[5]}"
                )
            print("------------------------------")
        except mysql.connector.Error as err:
            print(f"Error fetching report: {err}")
        finally:
            conn.close()


def add_medical_record():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            p_id = input("Enter Patient ID: ")
            diag = input("Enter Diagnosis: ")
            doc = input("Enter Treatment/Doctor Name: ")

            # New input for Inpatient/Outpatient
            print("\nSelect Patient Type:")
            print("1. Inpatient")
            print("2. Outpatient")
            type_choice = input("Select a1n option (1-2): ")
            p_type = "Inpatient" if type_choice == "1" else "Outpatient"

            # Added patient_type to the INSERT statement
            query = "INSERT INTO medical_records (patient_id, diagnosis, treatment, patient_type) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (p_id, diag, doc, p_type))
            conn.commit()
            print("Medical record added successfully.")
        except mysql.connector.Error as err:
            print(f"Error adding record: {err}")
        finally:
            conn.close()


def edit_diagnosis():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            record_id = input("Enter Patient ID to edit: ")
            new_diag = input("Enter New Diagnosis: ")

            query = "UPDATE medical_records SET diagnosis = %s WHERE patient_id = %s"
            cursor.execute(query, (new_diag, record_id))
            conn.commit()
            print("Diagnosis updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error updating diagnosis: {err}")
        finally:
            conn.close()


# NEW FUNCTION: Deletes a specific medical record
def delete_record():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            print("\n--- Delete Medical Record ---")
            record_id = input(
                "Enter Record ID to delete (or Patient ID if mapping 1:1): "
            )

            # Warning prompt
            confirm = input(
                f"Are you sure you want to delete record {record_id}? (y/n): "
            )
            if confirm.lower() != "y":
                print("Deletion canceled.")
                return

            # Note: This deletes from medical_records using patient_id.
            # If you want to delete by record_id, change `patient_id` to `record_id` below.
            query = "DELETE FROM medical_records WHERE patient_id = %s"
            cursor.execute(query, (record_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print("Record deleted successfully.")
            else:
                print("No record found with that ID.")

        except mysql.connector.Error as err:
            print(f"Error deleting record: {err}")
        finally:
            conn.close()


def register_new_patient():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")
            phone = input("Enter Phone Number: ")

            query = "INSERT INTO patients (first_name, last_name, dob, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (first_name, last_name, dob, phone))
            conn.commit()
            print("Patient registered successfully.")
        except mysql.connector.Error as err:
            print(f"Error registering patient: {err}")
        finally:
            conn.close()


def main_menu():
    while True:
        print("\n--- Hospital Management System ---")
        print("1. View Patient Report")
        print("2. Add New Medical Record")
        print("3. Edit Existing Diagnosis")
        print("4. Register New Patient")
        print("5. Delete Medical Record")  # Added Delete option
        print("6. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_report()
        elif choice == "2":
            add_medical_record()
        elif choice == "3":
            edit_diagnosis()
        elif choice == "4":
            register_new_patient()
        elif choice == "5":
            delete_record()  # Call the new function
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main_menu()