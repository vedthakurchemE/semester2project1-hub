import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def run(uploaded_data=None):

    st.title("🏭 Industrial SCADA Monitoring Dashboard")

    # ==========================================
    # Data Generation or Upload
    # ==========================================
    st.sidebar.header("Data Source")

    if uploaded_data is not None:
        df = pd.read_csv(uploaded_data)
    else:
        st.sidebar.info("Using simulated live plant data")

        time = np.arange(0, 200)

        temperature = 150 + 5*np.sin(0.05*time) + np.random.normal(0,1,len(time))
        pressure = 8 + 0.5*np.sin(0.08*time) + np.random.normal(0,0.2,len(time))
        flow = 50 + 3*np.sin(0.03*time) + np.random.normal(0,1,len(time))
        level = 60 + 10*np.sin(0.02*time) + np.random.normal(0,2,len(time))

        # Inject anomaly
        pressure[150:] += 2

        df = pd.DataFrame({
            "Time": time,
            "Temperature": temperature,
            "Pressure": pressure,
            "Flow": flow,
            "Level": level
        })

    # ==========================================
    # KPI PANEL
    # ==========================================
    st.subheader("📊 Live KPIs")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Temperature (°C)", round(df["Temperature"].iloc[-1],2))
    col2.metric("Pressure (bar)", round(df["Pressure"].iloc[-1],2))
    col3.metric("Flow (m3/h)", round(df["Flow"].iloc[-1],2))
    col4.metric("Level (%)", round(df["Level"].iloc[-1],2))

    # ==========================================
    # Alarm System
    # ==========================================
    st.subheader("🚨 Alarm Panel")

    alarms = []

    if df["Pressure"].iloc[-1] > 9:
        alarms.append("Pressure HIGH")
    if df["Temperature"].iloc[-1] > 160:
        alarms.append("Temperature HIGH")
    if df["Level"].iloc[-1] < 40:
        alarms.append("Level LOW")

    if alarms:
        for alarm in alarms:
            st.error(alarm)
    else:
        st.success("System Operating Normally")

    # ==========================================
    # Trend Visualization
    # ==========================================
    st.subheader("📈 Process Trends")

    selected_tag = st.selectbox(
        "Select Tag",
        ["Temperature", "Pressure", "Flow", "Level"]
    )

    fig, ax = plt.subplots()
    ax.plot(df["Time"], df[selected_tag])
    ax.set_xlabel("Time")
    ax.set_ylabel(selected_tag)
    ax.set_title(f"{selected_tag} Trend")
    st.pyplot(fig)

    # ==========================================
    # Statistical Analysis
    # ==========================================
    st.subheader("📉 Statistical Summary")

    st.write(df.describe())

    # ==========================================
    # Anomaly Detection (Simple Z-Score)
    # ==========================================
    st.subheader("🔍 Anomaly Detection")

    tag = st.selectbox("Select Tag for Anomaly Detection",
                       ["Temperature", "Pressure", "Flow", "Level"],
                       key="anomaly")

    mean = df[tag].mean()
    std = df[tag].std()

    threshold = 3
    anomalies = df[np.abs((df[tag]-mean)/std) > threshold]

    if not anomalies.empty:
        st.warning(f"Anomalies detected in {tag}")
        st.write(anomalies.tail())
    else:
        st.success("No statistical anomalies detected")

if __name__ == "__main__":
    run()
