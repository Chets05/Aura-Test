import streamlit as st
import subprocess
import os
import time

st.set_page_config(page_title="AuraTest Execution Engine", page_icon="🛡️", layout="wide")

st.title("🛡️ AuraTest: Autonomous Execution & Healing")
st.write("Click below to launch the live Selenium test suite.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🚀 Test Control")
    if st.button("RUN LIVE SELENIUM TEST"):
        # Clear old reports
        if os.path.exists("healing_report.txt"):
            os.remove("healing_report.txt")
            
        with st.status("Running Selenium Test Suite...", expanded=True) as status:
            st.write("Initializing Chrome Driver...")
            # This runs your actual test script in the background
            process = subprocess.Popen(["python", "test_demo.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Live Terminal Output in the UI
            stdout, stderr = process.communicate()
            st.code(stdout)
            
            status.update(label="Test Run Complete!", state="complete", expanded=False)

with col2:
    st.subheader("📝 Healing Report for QA")
    if os.path.exists("healing_report.txt"):
        with open("healing_report.txt", "r") as f:
            report_data = f.read()
        
        st.success("### ✅ AI HEALING SUCCESSFUL")
        st.text_area("Final Technical Report:", value=report_data, height=200)
        
        # Download button for the QA Team
        st.download_button("Download Report for QA Team", report_data, file_name="aura_healing_report.txt")
    else:
        st.info("No healing events recorded yet. Run a test to generate a report.")