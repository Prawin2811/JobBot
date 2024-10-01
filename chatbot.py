import http.client
import json

def get_weather(city):
    conn = http.client.HTTPSConnection("open-weather13.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "815fa5cbf3msh442f13c5587be06p1da458jsn31e3ce8650e7",
        'x-rapidapi-host': "open-weather13.p.rapidapi.com"
    }

    conn.request("GET", f"/city/{city}/EN", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # Decode and parse the JSON data
    weather_data = json.loads(data.decode("utf-8"))

    # Extract and print useful information
    try:
        print(f"Weather in {weather_data['name']}, {weather_data['sys']['country']}:")
        print(f"Temperature: {weather_data['main']['temp']}°F")
        print(f"Feels Like: {weather_data['main']['feels_like']}°F")
        print(f"Weather: {weather_data['weather'][0]['description'].capitalize()}")
        print(f"Wind Speed: {weather_data['wind']['speed']} mph")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Visibility: {weather_data['visibility'] / 1000} km")
    except KeyError as e:
        print(f"KeyError: {e}. Check the API response structure.")

if __name__ == '__main__':
    city = "Chengalpattu"  # Ensure this is the correct city name
    get_weather(city)
