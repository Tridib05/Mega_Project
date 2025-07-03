import tkinter as tk                               # Import the Tkinter library for GUI
from tkinter import messagebox                     # Import messagebox for pop-up dialogs
import pandas as pd                                # Import pandas for data handling
import matplotlib.pyplot as plt                    # Import matplotlib for plotting graphs

# Load the dataset (CSV file with player stats)
# Reads the CSV file containing T20 World Cup player data into a pandas DataFrame
# Make sure the file path and column names match your CSV
# 'player' column should contain player names, 'Runs' column should contain run totals

data = pd.read_csv(r"C:/Users/TRIDIB BHUNIA/Desktop/Python/Project/T20 WCC Data Analytics/t20_wc_data.csv")

# Create main app window
root = tk.Tk()                                                           # Create the main application window
root.title("\U0001F3CF T20 World Cup Cricket Analytics")                 # Set the window title with a cricket emoji
root.geometry("800x500")                                                 # Set the window size (width x height)

# Search function: Finds and displays player info based on user input
def search_player():
    name = entry.get().strip().lower()                                   # Get the player name entered by the user, make it lowercase
    # Search for players whose name contains the input string (case-insensitive)
    result = data[data['player'].str.lower().str.contains(name)]
    if result.empty:
        # If no player is found, show a pop-up message
        messagebox.showinfo("Not Found", "No player found.")
    else:
        # If found, clear previous output and display the result in the text box
        output_text.delete("1.0", tk.END)                                
        output_text.insert(tk.END, result.to_string(index=False))          # Insert the found player's stats into the text box
    
# Graph function: Shows top 5 run scorers in a bar chart
def show_top_run_scorers():
    # Sort the data by 'Runs' in descending order and get the top 5 players
    top_players = data.sort_values(by="Runs", ascending=False).head(5)
    plt.figure(figsize=(8, 5))                       # Set the size of the plot
    # Create a bar chart with player names on X-axis and runs on Y-axis
    plt.bar(top_players['player'], top_players['Runs'], color="skyblue")
    plt.title("Top 5 Run Scorers")                   # Set the chart title
    plt.xlabel("Player")                             # Label for X-axis
    plt.ylabel("Runs")                               # Label for Y-axis
    plt.tight_layout()                               # Adjust layout to fit everything
    plt.show()                                       # Display the plot in a new window

# Additional Info/Help Button function
def show_info():
    info = (
        "T20 World Cup Cricket Data Analytics\n\n"
        "- Search for any player by name to see their stats.\n"
        "- Click 'Top 5 Run Scorers Graph' to view a bar chart of the highest run scorers.\n\n"
        "Required Libraries:\n"
        "- pandas: For data handling\n"
        "- matplotlib: For plotting graphs\n"
        "- tkinter: For the GUI (comes with Python)\n\n"
        "Make sure your CSV file has columns: 'player' and 'Runs'.\n"
        "You can add more features, like searching by country, or showing more graphs!\n")
    messagebox.showinfo("About & Help", info)

# GUI Components
label = tk.Label(root, text="Enter Player Name:", font=("Arial", 14))                  # Label above the entry box
label.pack(pady=10)                                                                    # Add some vertical padding

entry = tk.Entry(root, font=("Arial", 14), width=30)                  # Entry box for user to type player name
entry.pack()                                                          # Place the entry box in the window

search_btn = tk.Button(root, text="Search", font=("Arial", 12), command=search_player)               # Button to search for player
search_btn.pack(pady=5)                                                                              # Add some vertical padding

graph_btn = tk.Button(root, text="Top 5 Run Scorers Graph", font=("Arial", 12), command=show_top_run_scorers)         # Button to show graph
graph_btn.pack(pady=5)                                                # Add some vertical padding

info_btn = tk.Button(root, text="Info / Help", font=("Arial", 12), command=show_info)           # Add an Info/Help button to the GUI
info_btn.pack(pady=5)                                                 # Add some vertical padding

output_text = tk.Text(root, height=10, width=80)                      # Text box to display player info/results
output_text.pack(pady=10)                                             # Add some vertical padding

root.mainloop()  
# Start the Tkinter event loop (keeps the window open)
# This line keeps the application running, waiting for user interactions
# When the user closes the window, the application will exit    
# End of the script
# This is the end of the T20 World Cup Cricket Data Analytics application
# This application allows users to search for T20 World Cup players and view their stats
# It also provides a graphical representation of the top 5 run scorers in T20 World Cup history
# Make sure to have the required libraries installed (pandas, matplotlib, tkinter)  
# and the CSV file in the correct path for the application to work properly
# Enjoy analyzing T20 World Cup cricket data!
# This application is a simple yet effective way to explore player statistics and visualize performance trends
# Feel free to modify and enhance the application with additional features or data visualizations
# Happy coding and enjoy your cricket analytics journey!