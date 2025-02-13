import streamlit as st
from helpers import (
    get_travel_time,
    get_weather_forecast,
    get_attractions,
    get_hotels,
    generate_packing_list,
)

# Page Config with custom theme
st.set_page_config(
    page_title="Smart Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets\styles.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Header Section with animated gradient
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1 class="hero-title">✈️ Smart Travel Planner</h1>
        <p class="hero-subtitle">Your Personal Guide to Stress-Free Travel Planning</p>
        <div class="scrolling-icons">
            <span>🌍</span><span>🗺️</span><span>🧳</span><span>⛅</span><span>🏨</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input Section with Card Design
with st.form("travel_form"):
    st.markdown("""
    <div class="form-card">
        <div class="form-header">
            <h3 class="form-title">📅 Plan Your Journey</h3>
            <div class="form-decoration"></div>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns((1, 1, 1, 1))
    with cols[0]:
        origin = st.text_input("From", placeholder="City, Country", help="Starting location")
    with cols[1]:
        destination = st.text_input("To", placeholder="City, Country", help="Destination")
    with cols[2]:
        travel_date = st.date_input("Departure Date", help="When are you leaving?")
    with cols[3]:
        return_date = st.date_input("Return Date", help="When are you coming back?")
    
    members = st.number_input("Travelers", min_value=1, value=1, 
                            help="Number of people traveling", key="members")
    
    st.markdown("</div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("✨ Generate Travel Plan", use_container_width=True)

# Results Section
if submitted:
    if origin and destination and travel_date and return_date:
        with st.spinner("🔍 Analyzing routes... ⏳ Checking weather... 🌟 Finding best options..."):
            # Fetch data
            travel_time = get_travel_time(origin, destination)
            weather = get_weather_forecast(destination, travel_date, return_date)
            attractions = get_attractions(destination)
            hotels = get_hotels(destination)
            packing_list = generate_packing_list(weather["start_date"])

        # Display Results
        st.markdown("## 🌍 Your Personalized Travel Plan")
        
        # Main Columns
        main_col1, main_col2 = st.columns([3, 2])
        
        with main_col1:
            # Route Card
            with st.expander("🚗 Travel Details", expanded=True):
                cols = st.columns(2)
                cols[0].metric("Estimated Travel Time", travel_time, 
                             help="Driving time between locations")
                cols[1].metric("Approximate Distance", "1,234 km", 
                             help="Straight line distance between cities")
                
                st.markdown("""
                <div class="map-placeholder">
                    <div class="map-overlay">Interactive Map Preview</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Weather Card
            with st.expander("🌦️ Weather Forecast", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    st.markdown(f"### Departure Day ({travel_date})")
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="weather-icon">⛅</div>
                        <div class="weather-info">
                            <div class="temperature">{weather['start_date']['temperature']:.1f}°C</div>
                            <div class="conditions">{weather['start_date']['description'].title()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with cols[1]:
                    st.markdown(f"### Return Day ({return_date})")
                    st.markdown(f"""
                    <div class="weather-card">
                        <div class="weather-icon">🌤️</div>
                        <div class="weather-info">
                            <div class="temperature">{weather['return_date']['temperature']:.1f}°C</div>
                            <div class="conditions">{weather['return_date']['description'].title()}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
        with main_col2:
            # Packing List Card
            with st.expander("🧳 Smart Packing List", expanded=True):
                st.markdown("""
                <div class="packing-list">
                    <div class="essentials">
                        <h4>Essentials</h4>
                        {}
                    </div>
                    <div class="weather-specific">
                        <h4>Weather-Specific</h4>
                        {}
                    </div>
                </div>
                """.format(
                    "".join([f'<div class="packing-item">✓ {item}</div>' for item in packing_list[:3]]),
                    "".join([f'<div class="packing-item">✓ {item}</div>' for item in packing_list[3:]])
                ), unsafe_allow_html=True)
            
            # Attractions & Hotels
            tabs = st.tabs(["🏞️ Top Attractions", "🏨 Recommended Stays"])
            with tabs[0]:
                st.markdown("""
                <div class="attraction-list">
                    {}
                </div>
                """.format("".join([
                    f'<div class="attraction-item">📍 {attraction}</div>' 
                    for attraction in attractions
                ])), unsafe_allow_html=True)
            with tabs[1]:
                st.markdown("""
                <div class="hotel-list">
                    {}
                </div>
                """.format("".join([
                    f'<div class="hotel-item">🏩 {hotel}</div>' 
                    for hotel in hotels
                ])), unsafe_allow_html=True)
        
        # Recommendations Section
        st.markdown("## 🌟 Local Insights")
        cols = st.columns(3)
        with cols[0]:
            st.markdown("""
            <div class="insight-card food">
                <h3>🍴 Must-Try Foods</h3>
                <div class="insight-content">
                    <div>🥘 Local Specialty 1</div>
                    <div>🍲 Famous Dish 2</div>
                    <div>🍢 Street Food 3</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            st.markdown("""
            <div class="insight-card photo">
                <h3>📸 Photo Spots</h3>
                <div class="insight-content">
                    <div>🌅 Scenic Viewpoint 1</div>
                    <div>🏛️ Historic Landmark 2</div>
                    <div>🌉 Iconic Location 3</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            st.markdown("""
            <div class="insight-card tips">
                <h3>⚠️ Travel Tips</h3>
                <div class="insight-content">
                    <div>💵 Local currency: XYZ</div>
                    <div>🚨 Emergency: 112</div>
                    <div>🔌 Power outlets: Type C</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
    else:
        st.error("Please fill in all required fields!", icon="❌")

# Footer
st.markdown("""
<div class="footer">
    <div class="footer-content">
        <p>Powered by OpenWeather, Google Maps, and Yelp APIs</p>
        <p>Built with ❤️ using Streamlit</p>
    </div>
</div>
""", unsafe_allow_html=True)