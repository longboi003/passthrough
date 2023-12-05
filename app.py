from flask import Flask, request, render_template
import sqlite3
#Initialize the app from Flask
app = Flask(__name__)
#Connects to the database and creates it if it doesn't exist
with sqlite3.connect("inventory.db") as con:
    con.execute('CREATE TABLE IF NOT EXISTS Inventory(category TEXT, description TEXT, price TEXT, code TEXT)')
    con.commit()
#Flask route for the home page
@app.route('/')
#Function to run when the home page is loaded
def home():
    return render_template('entryWebsite.html')
#Flask route for the add page
@app.route('/inventoryadd', methods=['GET', 'POST'])

def inventory_add():
    #If the user submits the form it sets the inputs to python variables
    if request.method == 'POST':
        category = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        code = request.form.get('code')
        #Connects to the database and inserts the variables into the table
        with sqlite3.connect("inventory.db") as con:
            con.execute("INSERT INTO Inventory (category, description, price, code) VALUES (?, ?, ?, ?)",
                  (category, description, price, code))
            con.commit()

        #Returns the user to the home page if they submit the form
        return render_template('entryWebsite.html')
    #If the user doesn't submit the form it returns the add page
    else:
        return render_template('inventoryadd.html')
#Flask route for the view page
@app.route('/inventoryview')
def inventory_view():
    #sets whatever the user searched for equal to a variable
    search= request.args.get('search')
    #Connects to the database and gets all the data from the table
    with sqlite3.connect("inventory.db") as con:
        #If the user searched for something it selects the data that matches what they searched for otherwise it selects all the data
        c=con.cursor()
        if search:
            c.execute("SELECT * FROM Inventory WHERE category LIKE ? OR description LIKE ? OR price LIKE ? OR code LIKE ?",
                  (search,search,search,search))
        else:
            c.execute("SELECT * FROM Inventory")
            #Sets the data equal to a variable
        items = c.fetchall()
    #Returns the view page with the data from the database
    return render_template('inventoryview.html', items=items)

if __name__ == '__main__':
    app.run()