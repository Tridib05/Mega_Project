# Required Imports  
import tkinter as tk    
from tkinter import messagebox, ttk
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import pytz
import requests
from PIL import Image, ImageTk
from  timezonefinder import TimezoneFinder     

# Initialize main window
root = tk.Tk()
root.title("Weather App 5")  # Title of the window
root.geometry("750x470+300+200")  # Width x Height + X + Y position on screen
root.resizable(False, False)  # Disable resizing of the window
root.config(bg="#202731")  # Set background color

# Function to fetch weather data
def getWeather():
    city = textfield.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    geolocator = Nominatim(user_agent="weather-app")
    location = geolocator.geocode(city)
    if not location:
        messagebox.showerror("Error", "City not found.")
        return
    obj = TimezoneFinder()
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)
    if not result:
        messagebox.showerror("Error", "Timezone not found.")
        return
    timezone_label.config(text=result)
    long_lat_label.config(text=f"{round(location.latitude, 4)}°N {round(location.longitude, 4)}°E")
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock_label.config(text=current_time)
    
    api_key ="4e31747189a1f593fea26e607f7ca753"
    api = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(api)
    try:
        json_data = response.json()
    except Exception as e:
        messagebox.showerror("Error", f"Could not parse weather data.\n{e}")
        return
    if not isinstance(json_data, dict) or 'list' not in json_data:
        messagebox.showerror("Error", f"Could not fetch weather data. API response: {json_data}")
        return
    
    # Current Weather from first forecast
    try:
        current = json_data['list'][0]
        temp = current['main']['temp']
        humidity = current['main']['humidity']
        pressure = current['main']['pressure']
        wind_speed = current['wind']['speed']
        description = current['weather'][0]['description']

        temperature_label.config(text=f"{temp}°C")
        humidity_label.config(text=f"{humidity}%")
        pressure_label.config(text=f"{pressure} hPa")
        wind_speed_label.config(text=f"{wind_speed} m/s")
        description_label.config(text=f"{description}")
    except Exception as e:
        temperature_label.config(text="N/A")
        humidity_label.config(text="N/A")
        pressure_label.config(text="N/A")
        wind_speed_label.config(text="N/A")
        description_label.config(text="N/A")
        messagebox.showerror("Error", f"Could not fetch weather data.\n{e}")
    
    # Daily forecast - pick 12:00 PM entries
    daily_data = []
    for entry in json_data['list']:
        if '12:00:00' in entry['dt_txt']:
            daily_data.append(entry)
    icons = []
    temps = []
    for i in range(5):
        if i >= len(daily_data):
            break
        icon_code = daily_data[i]['weather'][0]['icon']
        try:
            img = Image.open(f"icon/{icon_code}@2x.png").resize((50, 50))
            icon_img = ImageTk.PhotoImage(img)
        except Exception:
            icon_img = None
        icons.append(icon_img)
        # temp_max is day, temp_min is night, feels_like is feels
        temp_max = daily_data[i]['main'].get('temp_max', 'N/A')
        temp_min = daily_data[i]['main'].get('temp_min', 'N/A')
        feels = daily_data[i]['main'].get('feels_like', 'N/A')
        temps.append((temp_max, temp_min, feels))

    day_widget = [
        (first_image, day1_label, day1_temp_label),
        (second_image, day2_label, day2_temp_label),
        (third_image, day3_label, day3_temp_label),
        (fourth_image, day4_label, day4_temp_label),
        (fifth_image, day5_label, day5_temp_label)
    ]

    for i, (img_label, day_label, temp_label) in enumerate(day_widget):
        if i >= len(icons):
            img_label.config(image='')
            temp_label.config(text="N/A")
            day_label.config(text="")
            continue
        if icons[i] is not None:
            img_label.config(image=icons[i])
            img_label.image = icons[i]
        else:
            img_label.config(image='')
        # Show Day, Night, Feels (old style, no wraplength)
        temp_max, temp_min, feels = temps[i]
        temp_label.config(text=f"Day: {temp_max}°C\nNight: {temp_min}°C\nFeels: {feels}°C")
        future_date = datetime.now() + timedelta(days=i)
        day_label.config(text=future_date.strftime("%A"))


# Set App Icon (use tk.PhotoImage, not just PhotoImage)
image_icon = tk.PhotoImage(file="Images/logo.png")
root.iconphoto(False, image_icon)

# Add Rounded Rectangle Background (use tk.PhotoImage)
round_box = tk.PhotoImage(file="Images/Rounded Rectangle 1.png")
tk.Label(root, image=round_box, bg="#202731").place(x=30, y=60)

# Temperature Label
label_1 = tk.Label(root,text="Temperature",font=("Helvetica", 11),fg="#323661",bg="#aad1c8")
label_1.place(x=50, y=120)

label_2 = tk.Label(root,text="Humidity",font=("Helvetica", 11),fg="#323661",bg="#aad1c8")
label_2.place(x=50, y=140)

label_3 = tk.Label(root,text="Pressure",font=("Helvetica", 11),fg="#323661",bg="#aad1c8")
label_3.place(x=50, y=160)

label_4 = tk.Label(root,text="Wind Speed",font=("Helvetica", 11),fg="#323661",bg="#aad1c8")
label_4.place(x=50, y=180)

label_5 = tk.Label(root,text="Description",font=("Helvetica", 11),fg="#323661",bg="#aad1c8")
label_5.place(x=50, y=200)


# Search Box
# Search box background image
search_image = tk.PhotoImage(file="Images/Rounded Rectangle 3.png")
search_bg = tk.Label(root, image=search_image, bg="#202731")
search_bg.place(x=270, y=122)

# Weather icon inside search box
weather_icon_img = tk.PhotoImage(file="Images/Layer 7.png")
weather_icon = tk.Label(root, image=weather_icon_img, bg="#333c4c")
weather_icon.place(x=290, y=127)

# Search text field
textfield = tk.Entry(root,justify="center",width=15,font=("poppins", 25, "bold"),bg="#333c4c",border=0,fg="white")
textfield.place(x=370, y=130)

# Search button icon
search_icon_img = tk.PhotoImage(file="Images/Layer 6.png")
search_button = tk.Button(root,image=search_icon_img,borderwidth=0,cursor="hand2",bg="#333c4c",command=getWeather)
search_button.place(x=640, y=135)


# Bottom Frame Box
bottom_frame = tk.Frame(root, width=1000, height=180, bg="#7094d4")
bottom_frame.pack(side=tk.BOTTOM)

# Info Boxes in Bottom Frame
# Load box images
first_box_img = tk.PhotoImage(file="Images/Rounded Rectangle 2.png")  
second_box_img = tk.PhotoImage(file="Images/Rounded Rectangle 2 copy.png") 

# Place box images inside frame
box1 = tk.Label(bottom_frame, image=first_box_img, bg="#7094d4")
box1.place(x=30, y=20)

box2 = tk.Label(bottom_frame, image=second_box_img, bg="#7094d4")
box2.place(x=300, y=30)

box3 = tk.Label(bottom_frame, image=second_box_img, bg="#7094d4")
box3.place(x=400, y=30)

box4 = tk.Label(bottom_frame, image=second_box_img, bg="#7094d4")
box4.place(x=500, y=30)

box5 = tk.Label(bottom_frame, image=second_box_img, bg="#7094d4")
box5.place(x=600, y=30)


# Clock Display
clock_label = tk.Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
clock_label.place(x=30, y=20)

# Timezone Display
timezone_label = tk.Label(root, font=("Helvetica", 20), bg="#202731", fg="white")
timezone_label.place(x=500, y=20)

long_lat_label = tk.Label(root, font=("Helvetica", 10), bg="#202731", fg="white")
long_lat_label.place(x=500, y=50)

# Temperature, Humidity, Pressure (THPWD Section)
temperature_label = tk.Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
temperature_label.place(x=150, y=120)

humidity_label = tk.Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
humidity_label.place(x=150, y=140)

pressure_label = tk.Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
pressure_label.place(x=150, y=160)

wind_speed_label = tk.Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
wind_speed_label.place(x=150, y=180)

description_label = tk.Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white")
description_label.place(x=150, y=200)


# First Cell (Forecast Box)
first_frame = tk.Frame(root, width=230, height=132, bg="#323661")
first_frame.place(x=35, y=315)

# Weather icon/image inside first cell
first_image = tk.Label(first_frame, bg="#323661")
first_image.place(x=1, y=15)

# Day label (e.g., "Monday")
day1_label = tk.Label(first_frame,font=("Arial", 17,"bold"),bg="#323661",fg="white")
day1_label.place(x=100, y=5)

# Day temperature label
day1_temp_label = tk.Label(first_frame,font=("Arial", 13, "bold"),bg="#323661",fg="white")
day1_temp_label.place(x=100, y=50)



# Second Cell (Forecast Box)
second_frame = tk.Frame(root, width=90, height=135, bg="#eeefea")
second_frame.place(x=295, y=315)


# Weather icon/image inside second cell
second_image = tk.Label(second_frame, bg="#eeefea")
second_image.place(x=20, y=35, width=50, height=30)


# Day label (e.g., "Tuesday")
day2_label = tk.Label(second_frame, bg="#eeefea", fg="#000", font=("Arial", 11, "bold"), anchor="center", justify="center")
day2_label.place(x=0, y=5, width=90, height=22)


# Day temperature label
day2_temp_label = tk.Label(second_frame, bg="#eeefea", fg="#000", font=("Arial", 9), anchor="center", justify="center", wraplength=80)
day2_temp_label.place(x=2, y=80, width=88, height=55)



# Third Cell (Forecast Box)
third_frame = tk.Frame(root, width=90, height=135, bg="#eeefea")
third_frame.place(x=395, y=315)


# Weather icon/image inside third cell
third_image = tk.Label(third_frame, bg="#eeefea")
third_image.place(x=20, y=35, width=50, height=30)


# Day label (e.g., "Wednesday")
day3_label = tk.Label(third_frame, bg="#eeefea", fg="#000", font=("Arial", 11, "bold"), anchor="center", justify="center")
day3_label.place(x=0, y=5, width=90, height=22)


# Day temperature label
day3_temp_label = tk.Label(third_frame, bg="#eeefea", fg="#000", font=("Arial", 9), anchor="center", justify="center", wraplength=80)
day3_temp_label.place(x=2, y=80, width=88, height=55)



# Fourth Cell (Forecast Box)
fourth_frame = tk.Frame(root, width=90, height=135, bg="#eeefea")
fourth_frame.place(x=495, y=315)


# Weather icon/image inside fourth cell
fourth_image = tk.Label(fourth_frame, bg="#eeefea")
fourth_image.place(x=20, y=35, width=50, height=30)


# Day label (e.g., "Thursday")
day4_label = tk.Label(fourth_frame, bg="#eeefea", fg="#000", font=("Arial", 11, "bold"), anchor="center", justify="center")
day4_label.place(x=0, y=5, width=90, height=22)


# Day temperature label
day4_temp_label = tk.Label(fourth_frame, bg="#eeefea", fg="#000", font=("Arial", 9), anchor="center", justify="center", wraplength=80)
day4_temp_label.place(x=2, y=80, width=88, height=55)



# Fifth Cell (Forecast Box)
fifth_frame = tk.Frame(root, width=90, height=135, bg="#eeefea")
fifth_frame.place(x=595, y=315)


# Weather icon/image inside fifth cell
fifth_image = tk.Label(fifth_frame, bg="#eeefea")
fifth_image.place(x=20, y=35, width=50, height=30)


# Day label (e.g., "Friday")
day5_label = tk.Label(fifth_frame, bg="#eeefea", fg="#000", font=("Arial", 11, "bold"), anchor="center", justify="center")
day5_label.place(x=0, y=5, width=90, height=22)


# Day temperature label
day5_temp_label = tk.Label(fifth_frame, bg="#eeefea", fg="#000", font=("Arial", 9), anchor="center", justify="center", wraplength=80)
day5_temp_label.place(x=2, y=80, width=88, height=55)

# Main loop (you will need this at the end of your app)
root.mainloop()