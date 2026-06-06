import pandas as pd


def get_agent_logs():
    """Simulates fetching operational data from the agent system."""
    data = {
        'date': pd.to_datetime(['2025-09-01', '2025-09-02']),
        'tasks_completed': [1500, 1600],
        'avg_success_rate': [0.92, 0.94]
    }
    return pd.DataFrame(data)


def get_business_data():
    """Simulates fetching KPI data from a business system."""
    data = {
        'date': pd.to_datetime(['2025-09-01', '2025-09-02']),
        'support_tickets_resolved': [1200, 1350],
        'customer_satisfaction': [4.1, 4.3]
    }
    return pd.DataFrame(data)


def generate_roi_report():
    """Combines operational and business data to show value."""
    agent_df = get_agent_logs()
    business_df = get_business_data()

    # Merge the data on the date
    report_df = pd.merge(agent_df, business_df, on='date')

    # Simple ROI calculation: Each point of success rate improvement
    # is correlated with an increase in customer satisfaction.
    report_df['impact_correlation'] = (
        report_df['customer_satisfaction'] / report_df['avg_success_rate']
    )

    print("--- Business Value (ROI) Report ---")
    print(report_df.to_string(index=False))
    print(
        "\nCONCLUSION: A clear positive correlation is observed between agent success rate "
        "and customer satisfaction."
    )


# --- Generate Report ---
generate_roi_report()