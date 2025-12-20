import streamlit as st
import requests

st.title("Docker Networking Demo — Streamlit Frontend")
st.write("This frontend calls the backend service using the Docker service name `backend`.")
text = st.text_area("Text to analyze", "Type something here to analyze...")

if st.button("Analyze"):
   try:
       resp = requests.post("http://backend:5000/analyze", json={"text": text}, timeout=5)
       resp.raise_for_status()
       data = resp.json()
       st.success("Backend returned:")
       st.json(data)
   except Exception as e:
       st.error(f"Call to backend failed: {e}")
       st.write("Tip: make sure backend service is up and both services are on the same Docker network.")

if st.button("Count"):
    resp = requests.get("http://backend:5000/count")
    count = resp.json()["total_words"]
    st.write(f"Total words analysed: {count}")
    # The duplicate line was here, make sure it is removed or moved
    # resp = requests.get("http://backend:5000/count") 
    # count = resp.json()["total_words"]
    # st.write(f"Total words analysed: {count}")

