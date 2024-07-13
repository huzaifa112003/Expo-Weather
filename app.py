import tkinter as tk
from tkinter import ttk, messagebox, font as tkFont, PhotoImage
from weather_api import get_current_weather, get_weather_forecast
from expotree import ExTree
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import datetime
from PIL import Image, ImageTk
import requests
import io

# Global variables for the labels
w, h, d, p = None, None, None, None
temperature_label = None

# Styling function to apply custom styles to widgets
def stylize_widgets(root):
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TLabel', background='#f0f0f0', foreground='#333', font=("poppins", 12))
    style.configure('TButton', font=("poppins", 12, 'bold'), background='#333', foreground='white')
    style.configure('TEntry', font=("poppins", 12), foreground='#555')
    style.configure('TFrame', background='#f0f0f0')

# Function to fetch weather icon images
def fetch_icon(icon_code):
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(icon_url)
    if response.status_code == 200:
        image_bytes = io.BytesIO(response.content)
        img = Image.open(image_bytes)
        return ImageTk.PhotoImage(img)
    else:
        return None

# Function to update the display with current weather and forecast
def update_weather_display(city_name, current_weather_area, forecast_info_area, tree):
    current_weather = get_current_weather(city_name)
    if current_weather:
        display_current_weather(current_weather, current_weather_area)
        # Prepare current weather data for labels
        current_weather_data = {
            'wind_speed': current_weather['wind']['speed'],
            'humidity': current_weather['main']['humidity'],
            'pressure': current_weather['main']['pressure'],
            'precipitation': current_weather.get('rain', {}).get('1h', 0) + current_weather.get('snow', {}).get('1h', 0),
        }
        update_labels_with_weather_data(current_weather_data)  # Update the labels with current weather data
    else:
        messagebox.showerror("Weather Fetch Error", "Could not fetch the current weather data.")

    forecast_data = get_weather_forecast(city_name)
    if forecast_data:
        processed_data = process_weather_data(forecast_data)
        for data in processed_data:
            tree.insert(data['date'], data['weather_info'])
        display_forecast(tree, forecast_info_area)  # Display the forecast data
    else:
        messagebox.showerror("Forecast Fetch Error", "Could not fetch the forecast data.")

def update_labels_with_weather_data(current_weather):
    # Assuming 'current_weather' contains the current data for wind, humidity, etc.
    if current_weather:
        w.config(text=f"{current_weather['wind_speed']:.2f} m/s")
        h.config(text=f"{current_weather['humidity']:.2f}%")
        d.config(text=f"{current_weather['precipitation']:.2f} mm")
        p.config(text=f"{current_weather['pressure']:.2f} hPa")
    else:
        # Update the labels to show 'No data' if there is no weather data
        w.config(text="No data")
        h.config(text="No data")
        d.config(text="No data")
        p.config(text="No data")

def display_current_weather(data, display_area):
    try:
        # Extract the temperature from the data
        temperature = data['main']['temp']
        # Format the string to display the temperature
        weather_str = f"{temperature:.1f}°"
        # Update the label's text to show the formatted string
        display_area.config(text=weather_str)
    except KeyError:
        # If there is a KeyError, update the label to show an error message
        display_area.config(text="Error displaying weather data.")


def process_weather_data(forecast_data):
    """Process raw forecast data to prepare for insertion into the exponential tree."""
    processed_data = []
    for item in forecast_data['list']:
        date = datetime.datetime.fromtimestamp(item['dt']).strftime('%Y%m%d')
        weather_info = {
            'temp': item['main']['temp'],
            'humidity': item['main']['humidity'],
            'precipitation': item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0),
            'pressure': item['main']['pressure'],
            'wind_speed': item['wind']['speed']
        }
        processed_data.append({'date': int(date), 'weather_info': weather_info})
    return processed_data

def display_forecast(tree, display_area):
    """Display the forecast information in the GUI."""
    start_date = int(datetime.datetime.now().strftime('%Y%m%d'))
    end_date = start_date + 4  # Display forecast for the next 5 days
    average_weather = tree.get_average_weather(start_date, end_date)
    display_area.config(state='normal')
    display_area.delete('1.0', tk.END)
    if average_weather:
        forecast_str = f"Avg TEMP: {average_weather['avg_temp']:.2f}°C\n"
        forecast_str += f"Avg HUMIDITY: {average_weather['avg_humidity']:.2f}%\n"
        forecast_str += f"Total PRECIPITATION: {average_weather['total_precipitation']:.2f} mm\n"
        forecast_str += f"Avg PRESSURE: {average_weather['avg_pressure']:.2f} hPa\n"
        forecast_str += f"Avg WIND SPEED: {average_weather['avg_wind_speed']:.2f} m/s\n"
        display_area.insert(tk.END, forecast_str)
    else:
        display_area.insert(tk.END, "No forecast data available.")
    display_area.config(state='disabled')

    return average_weather


# Main function to setup the application window and widgets
def main():

    global w, h, d, p  # Declare as global within the function

    global temperature_label
    
    tree = ExTree()  # Initialize the exponential tree
    root = tk.Tk()
    root.title("Weather App")
    root.geometry('900x500+300+200')  # Set the size of the window
    # root.resizable(False, False) # Disable resizing of the window
    root.configure(background='#f0f0f0')

    stylize_widgets(root)  # Apply custom styles to widgets

    # Main frame to hold content widgets
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(expand=True, fill=tk.BOTH)

    # Input area for city name
    search_image = PhotoImage(file="search.png")
    city_label = tk.Label(image=search_image)
    city_label.place(x=0, y=20)

    city_entry= tk.Entry(root, justify="center", font=("poppins", 25, "bold"), width=17, bg = "#404040", border = 0, fg = "white")
    city_entry.place(x=50, y=40)
    city_entry.focus()

    search_icon = PhotoImage(file="searchicon.png")
    myimage = tk.Button(image=search_icon, borderwidth=0,cursor="hand2",bg = "#404040", command=lambda: update_weather_display(city_entry.get(), current_weather_area, forecast_info_area, tree))
    myimage.place(x=380, y=34)

    logo_image = PhotoImage(file="logo.png")
    logo = tk.Label(image=logo_image)
    logo.place(x=0, y=100)

    main_frame.columnconfigure(1, weight=1)  # Make the entry field expand with the window

    current_weather_area=tk.Label(font=("arial", 70, "bold"), fg="#ee666d") 
    current_weather_area.place(x=250,y=160)
 
    # Load the rounded rectangle image
    rounded_rect_image = tk.PhotoImage(file="boxix.png")  # Replace with the path to your image

    # Create a label with the image
    image_label = tk.Label(main_frame, image=rounded_rect_image)
    image_label.place(x=425, y=60)  # Position where you want the image

    # Create a text widget with a transparent background
    forecast_info_area = tk.Text(main_frame, height=6, font=("Helvetica", 18, "bold"), state='disabled', fg="white", bg="#008080", borderwidth=0, highlightthickness=0)
    forecast_info_area.place(x=488, y=132, width=370, height=185)  # Match the position and size of the image

    #bottombox
    Frame_image = PhotoImage(file="box.png")
    frame = tk.Label(image=Frame_image)
    frame.pack(side="bottom", padx=5,pady=5)

    #label
    label1 = tk.Label(root, text="WIND", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
    label1.place(x=120, y=400)

    label2 = tk.Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
    label2.place(x=250, y=400)

    label3 = tk.Label(root, text="PRECIPITATION", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
    label3.place(x=430, y=400)

    label4 = tk.Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), bg="#1ab5ef", fg="white")
    label4.place(x=650, y=400)

    # Initialize labels
    w = tk.Label(root, text="...", font=("arial", 15, "bold"), bg="#1ab5ef")
    h = tk.Label(root, text="...", font=("arial", 15, "bold"), bg="#1ab5ef")
    d = tk.Label(root, text="...", font=("arial", 15, "bold"), bg="#1ab5ef")
    p = tk.Label(root, text="...", font=("arial", 15, "bold"), bg="#1ab5ef")

    # Now place the labels
    w.place(x=120, y=430)
    h.place(x=270, y=430)
    d.place(x=470, y=430)
    p.place(x=650, y=430)

    root.mainloop()

if __name__ == "__main__":
    main()
