# Travel Explorer

Travel Explorer is a web application that allows users to explore destinations around the world, providing information about weather, popular attractions, and destination images.

## Features

- Search for any destination worldwide
- View multiple high-quality images of the destination
- Get current weather information for the destination
- Explore popular attractions in the area
- Interactive map showing the destination and attractions
- Brief description of the destination from Wikipedia
- List of predefined popular destinations for quick exploration

## Technologies Used

- Python 3.8+
- Flask
- HTML/CSS
- JavaScript
- Mapbox GL JS
- External APIs:
  - OpenWeatherMap API
  - Mapbox API
  - OpenTripMap API
  - Unsplash API
  - Wikipedia API

## Installation

1. Clone the repository: https://github.com/naaveen-raj/Travel-Explorer.git

2. Create a virtual environment and activate it:python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


3. Install the required packages:pip install -r requirements.txt

4.
4. Set up API keys:
- Sign up for free accounts and obtain API keys from the following services:
  - [OpenWeatherMap](https://openweathermap.org/api)
  - [Mapbox](https://www.mapbox.com/)
  - [OpenTripMap](https://opentripmap.io/product)
  - [Unsplash](https://unsplash.com/developers)

5. Create a `.env` file in the project root and add your API keys:
OPENWEATHER_API_KEY=your_openweather_api_key
MAPBOX_API_KEY=your_mapbox_api_key
OPENTRIPMAP_API_KEY=your_opentripmap_api_key
UNSPLASH_API_KEY=your_unsplash_api_key


## Usage

1. Ensure your virtual environment is activated:
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`


2. Run the Flask application:
python app.py


3. Open a web browser and navigate to `http://localhost:5000`

4. Explore destinations:
- Enter a destination in the search box on the home page and click "Explore"
- Or click on one of the popular destinations displayed on the home page

5. On the destination details page, you can:
- View multiple high-quality images of the destination
- Check the current weather information
- Read a brief description of the destination
- Explore popular attractions in the area
- Interact with the map to see the location of attractions

6. To explore a new destination, return to the home page by clicking on the "Travel Explorer" title or refreshing the page

7. To stop the application, press CTRL+C in the terminal where the Flask app is running

8. When you're done, deactivate the virtual environment:


## Customization

- To modify the list of popular destinations, edit the `POPULAR_DESTINATIONS` list in `app.py`
- To change the styling, modify the CSS in the `<style>` tags within `templates/index.html` and `templates/details.html`
- To add new features or modify existing ones, edit the `app.py` file and the corresponding HTML templates

## Troubleshooting

- If you encounter any "API key not valid" errors, double-check that you've correctly set up your `.env` file and that your API keys are valid
- If the application fails to start, ensure that all required packages are installed by running `pip install -r requirements.txt` again
- For any other issues, check the console output for error messages and refer to the documentation of the respective APIs
