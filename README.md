# AI-Powered-Travel-Insights-Recommendation-System


## 🚀 Overview
The **AI-Powered Travel Insights & Recommendation System** helps travelers discover must-try foods, top photography spots, and essential travel tips for any destination. By integrating **Yelp API** and **Google Maps API**, this system provides real-time, personalized travel recommendations to enhance user experiences.

## ✨ Features
- 📍 **Restaurant Recommendations** – Fetches the top-rated restaurants in any destination using **Yelp API**.
- 📸 **Photography Hotspots** – Identifies the best photography locations via **Google Maps Places API**.
- 🌍 **Travel Tips & Local Insights** – Provides useful local information, including currency, emergency contacts, and power outlet types.
- 🔄 **Real-time Data Retrieval** – Ensures up-to-date recommendations through API integration.

## 🛠️ Technologies Used
- **Python** 🐍
 **Yelp Fusion API**
- **Google Maps Places API**
- **Requests Library** (for API calls)

## 📦 Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/travel-insights-system.git
   cd travel-insights-system
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Set up API keys:
   - Obtain **Yelp API Key** from [Yelp Developer](https://www.yelp.com/developers/).
   - Obtain **Google Maps API Key** from [Google Cloud Console](https://console.cloud.google.com/).
   - Add your API keys in the script:
   ```python
   YELP_API_KEY = "your_yelp_api_key"
   GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
   ```

## 🚀 Usage
Run the script and enter a destination to get travel insights:
```python
from travel_insights import get_local_insights

insights = get_local_insights("New York")
print(insights)
```

## 📌 Example Output
```json
{
    "must_try_foods": ["Joe's Pizza", "Shake Shack", "Katz's Delicatessen"],
    "photo_spots": ["Brooklyn Bridge", "Times Square", "Central Park"],
    "travel_tips": {
        "currency": "USD",
        "emergency": "911",
        "power_outlets": "Type A & B"
    }
}
```

## 🛠️ Future Enhancements
- 🔍 **Sentiment Analysis** on restaurant reviews for better recommendations.
- 📊 **User Preference Learning** to tailor recommendations over time.
- 🌎 **Multi-language Support** for a global audience.


