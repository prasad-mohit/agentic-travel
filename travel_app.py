# filename: travel_app.py
import streamlit as st
import os
import google.generativeai as genai

# Replace with your actual Gemini API key (store securely, e.g., Streamlit Secrets)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set the GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def search_flights(preferences):
    """Simulates searching for flights based on preferences."""
    prompt = f"""Search for flights to {preferences['destination']} departing on {preferences['departure_date']} and returning on {preferences['return_date']} for {preferences['num_adults']} adults and {preferences['num_children']} children, within a budget of {preferences['budget']}. Consider any preferences: {preferences['preferences']}. Provide a few options including airline, price, and duration."""
    response = model.generate_content(prompt)
    return response.text

def search_hotels(preferences):
    """Simulates searching for hotels based on preferences."""
    prompt = f"""Search for hotels in {preferences['destination']} for the dates {preferences['departure_date']} to {preferences['return_date']} accommodating {preferences['num_adults']} adults and {preferences['num_children']} children, within a budget of {preferences['budget']}. Consider any preferences: {preferences['preferences']}. Provide a few options including hotel name, price per night, and star rating."""
    response = model.generate_content(prompt)
    return response.text

def book_travel(selected_flight, selected_hotel, preferences):
    """Simulates booking the selected travel options."""
    booking_confirmation = f"""**Booking Confirmed:**
    - **Destination:** {preferences['destination']}
    - **Dates:** {preferences['departure_date']} to {preferences['return_date']}
    - **Passengers:** {preferences['num_adults']} adults, {preferences['num_children']} children
    """
    if selected_flight:
        booking_confirmation += f"\n    - **Flight:** {selected_flight}"
    if selected_hotel:
        booking_confirmation += f"\n    - **Hotel:** {selected_hotel}"
    return booking_confirmation

def main():
    st.title("✈️ Your Personal Travel Agent")
    st.subheader("Let's plan your next adventure!")

    with st.form("travel_preferences"):
        destination = st.text_input("Where would you like to travel?")
        departure_date = st.date_input("Departure Date")
        return_date = st.date_input("Return Date")
        num_adults = st.number_input("Number of Adults", min_value=1, value=1)
        num_children = st.number_input("Number of Children", min_value=0, value=0)
        budget = st.text_input("Approximate Budget")
        preferences = st.text_area("Any specific preferences (e.g., direct flights, specific hotels, activities)?")
        submitted = st.form_submit_button("Find Options")

        if submitted and destination and departure_date and return_date:
            travel_preferences = {
                "destination": destination,
                "departure_date": departure_date.strftime("%Y-%m-%d"),
                "return_date": return_date.strftime("%Y-%m-%d"),
                "num_adults": num_adults,
                "num_children": num_children,
                "budget": budget,
                "preferences": preferences
            }

            with st.spinner("Searching for flights..."):
                flight_options = search_flights(travel_preferences)
                st.subheader("Flight Options:")
                st.write(flight_options)

            with st.spinner("Searching for hotels..."):
                hotel_options = search_hotels(travel_preferences)
                st.subheader("Hotel Options:")
                st.write(hotel_options)

            st.subheader("Make Your Selections:")
            selected_flight = st.text_input("Enter the flight you'd like to book (or leave blank):")
            selected_hotel = st.text_input("Enter the hotel you'd like to book (or leave blank):")

            if st.button("Book Now"):
                if selected_flight or selected_hotel:
                    with st.spinner("Processing your booking..."):
                        booking_confirmation = book_travel(selected_flight, selected_hotel, travel_preferences)
                        st.success(booking_confirmation)
                        st.balloons()
                else:
                    st.warning("Please select at least a flight or a hotel to book.")
        elif submitted:
            st.warning("Please fill in all the required travel details.")

if __name__ == "__main__":
    main()
