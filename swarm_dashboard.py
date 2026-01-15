import os

import pandas as pd
import streamlit as st


def load_log(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def main() -> None:
    st.set_page_config(page_title="Harmonia Swarm Dashboard", layout="wide")
    st.title("Harmonia Swarm Dashboard")

    default_path = "swarm_log.csv"
    st.sidebar.header("Configuration")
    log_path = st.sidebar.text_input("Swarm log CSV path", value=default_path)

    if not log_path or not os.path.exists(log_path):
        st.warning(f"CSV file not found at: {log_path!r}. Run swarm_sim.py with --csv first.")
        st.stop()

    df = load_log(log_path)

    # Basic info
    st.sidebar.markdown("**Summary**")
    steps = sorted(df["step"].unique())
    agents = sorted(df["agent_index"].unique())
    st.sidebar.write(f"Steps: {len(steps)}")
    st.sidebar.write(f"Agents: {len(agents)}")

    # Agent selection
    selected_agents = st.sidebar.multiselect(
        "Agents to display",
        options=agents,
        default=agents,
    )

    metric = st.sidebar.selectbox(
        "Metric",
        ["R", "psi", "phi", "energy", "epsilon", "maturity"],
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("Select a metric and agents to visualize their trajectories.")

    # Filtered dataframe
    plot_df = df[df["agent_index"].isin(selected_agents)]

    col1, col2 = st.columns(2)

    # Per-agent metric over time
    with col1:
        st.subheader(f"Per-agent {metric} over steps")
        if plot_df.empty:
            st.info("No agents selected.")
        else:
            pivot = plot_df.pivot_table(index="step", columns="agent_index", values=metric)
            st.line_chart(pivot)

    # Swarm-level R statistics
    with col2:
        st.subheader("Swarm-level R (mean and std)")
        stats = df.groupby("step")["R"].agg(["mean", "std"])
        st.line_chart(stats)

    st.subheader("Final state snapshot")
    last_step = df["step"].max()
    last_df = df[df["step"] == last_step].set_index("agent_index")
    st.write(f"Last step: {last_step}")
    st.dataframe(last_df[["R", "psi", "phi", "energy", "epsilon", "maturity"]])


if __name__ == "__main__":  # pragma: no cover
    main()
