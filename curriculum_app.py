import streamlit as st
import pandas as pd
import numpy as np

def create_fake_data(num_rows=2000):
    """
    Generates a DataFrame of fake curriculum data spanning from 2000 to 2025.
    """
    
    # --- Define data for randomization ---
    
    # 1. Create Academic Years from 2000-2001 to 2024-2025
    start_year = 2000
    end_year = 2024
    academic_years = [f"{y}-{y+1}" for y in range(start_year, end_year + 1)]
    
    # 2. Fake Event Names (Expanded to match your master_keyword_list)
    event_names = [
        'Anatomy Lab', 'Physiology Lecture', 'Clinical Skills Workshop', 
        'Ethics Seminar', 'Pathology Review', 'Pharmacology I', 'Cardiology Block', 
        'Pulmonology Case Study', 'Surgery Rotation', 'Pediatrics Grand Rounds',
        'Immunology Basics', 'Microbiology Lab', 'Neuroanatomy Lab', 'Renal System',
        'GI Tract Review', 'Genetics Workshop'
    ]
    
    # 3. Fake Objectives (including "Health Equity")
    objectives = [
        'Describe the cardiovascular system', 'Understand cell biology', 
        'Apply principles of health equity', 'Discuss patient-centered care', 
        'Identify major organ structures', 'Analyze determinants of health', 
        'Practice clinical examination', 'Review microbiology basics',
        'Learn surgical knot tying', 'Debate ethical dilemmas in medicine',
        'Discuss telemedicine advancements'
    ]
    
    # 4. Fake MEPO Outcomes
    mepos = [
        'MEPO 1: Medical Knowledge', 'MEPO 2: Patient Care', 
        'MEPO 3: Communication', 'MEPO 4: Professionalism', 
        'MEPO 5: Systems-Based Practice', 'MEPO 6: Lifelong Learning'
    ]

    # 5. Fake data for the *NEW* required columns
    academic_levels = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
    courses = ['Anatomy', 'Ethics', 'Cardiology', 'Pulmonary', 'Renal', 'Genetics']
    items = ['Instructional Method', 'Assessment']
    course_outcomes = ['C-O 1: Foundational Knowledge', 'C-O 2: Clinical Skills', 'C-O 3: Professional Identity']
    
    
    # --- Generate the DataFrame ---
    data = {
        'Academic Year': np.random.choice(academic_years, num_rows),
        'Academic Level': np.random.choice(academic_levels, num_rows),
        'Course': np.random.choice(courses, num_rows),
        'Event Name': np.random.choice(event_names, num_rows),
        'Associated Objectives': np.random.choice(objectives, num_rows),
        'Hours': np.round(np.random.uniform(0.5, 4.0, num_rows), 1),
        'Item': np.random.choice(items, num_rows),
        'Mapped Program Outcome': np.random.choice(mepos, num_rows),
        'Mapped Course Outcome': np.random.choice(course_outcomes, num_rows)
    }
    
    # ***** FIX 1 WAS HERE *****
    # Create the DataFrame from the 'data' dictionary, NOT by calling the function again.
    df = pd.DataFrame(data)
    
    # --- Ensure at least some data for your default search ---
    health_equity_rows = 100
    he_data = {
        'Academic Year': np.random.choice(academic_years, health_equity_rows),
        'Academic Level': 'Phase 1',
        'Course': 'Ethics',
        'Event Name': 'Health Disparities Seminar',
        'Associated Objectives': 'Apply principles of health equity',
        'Hours': np.round(np.random.uniform(1.0, 3.0, health_equity_rows), 1),
        'Item': 'Instructional Method',
        'Mapped Program Outcome': 'MEPO 5: Systems-Based Practice',
        'Mapped Course Outcome': 'C-O 3: Professional Identity'
    }
    he_df = pd.DataFrame(he_data)
    
    # Combine the random data with the specific health equity data
    final_df = pd.concat([df, he_df]).reset_index(drop=True)
    
    return final_df

df = create_fake_data(num_rows=2000)

# --- APP LAYOUT & UI ---
st.set_page_config(layout="wide")
st.title("Comprehensive Curriculum Mapping Tool 🗺️")
st.markdown("This prototype demonstrates advanced reporting, including drill-down and longitudinal analysis for CQI.")

# --- SIDEBAR FOR CONTROLS ---
st.sidebar.header("Reporting Controls")
# Add a filter for Academic Year
all_years = ['All Years'] + sorted(df['Academic Year'].unique().tolist(), reverse=True)
selected_year = st.sidebar.selectbox("Filter by Academic Year", all_years)

if selected_year != 'All Years':
    df_filtered_by_year = df[df['Academic Year'] == selected_year].copy()
else:
    df_filtered_by_year = df.copy()

report_type = st.sidebar.radio(
    "Select a Report Type",
    ["Keyword/Content Area", "Program Outcome (MEPO) Analysis", "Course Outcome Analysis", "Trends Over Time (CQI)"]
)
st.sidebar.markdown("---")

# --- REPORT GENERATION LOGIC ---
if report_type == "Keyword/Content Area":
    st.header("Keyword/Content Area Report")
    st.info("🎯 **Purpose:** For **accreditation** and **curriculum committees** to identify and quantify content coverage, locate gaps, and identify redundancies.")

    # --- Dynamic Keyword Generation ---
    # 1. Define a master list of potential keywords to look for.
    master_keyword_list = ['Ethics', 'Cardiac', 'Pharmacology', 'Renal', 'Pulmonary', 'Genetics', 'Health Equity', 'Telemedicine', 'Anatomy', 'Histology', 'GI']

    # 2. Create a combined text column for efficient searching.
    df_filtered_by_year['CombinedText'] = df_filtered_by_year['Event Name'] + " " + df_filtered_by_year['Associated Objectives']

    # 3. Find which keywords from the master list actually exist in the data.
    available_keywords = [
        keyword for keyword in master_keyword_list 
        if df_filtered_by_year['CombinedText'].str.contains(keyword, case=False).any()
    ]
    
    with st.sidebar.expander("Keyword Report Filters", expanded=True):
        # 4. Replace the text_input with a selectbox (dropdown).
        keyword = st.selectbox("Select a Keyword", options=available_keywords, index=0) # 'index=0' sets 'Ethics' as default

    if keyword:
        # Search for keyword in the pre-combined text field.
        search_mask = df_filtered_by_year['CombinedText'].str.contains(keyword, case=False)
        report_df = df_filtered_by_year[search_mask]

        if report_df.empty:
            st.warning(f"No content found for the keyword: '{keyword}'")
        else:
            # --- TOP-LEVEL SUMMARY BY PHASE ---
            st.subheader(f"Total Hours for '{keyword}' by Phase ({selected_year})")
            phase_summary = report_df.groupby('Academic Level')['Hours'].sum().reset_index()
            st.dataframe(phase_summary, use_container_width=True, hide_index=True)
            st.bar_chart(phase_summary.set_index('Academic Level')['Hours'])

            # --- COMPREHENSIVE COURSE-LEVEL BREAKDOWN ---
            st.subheader("Course-Level Breakdown")
            st.markdown("This table shows every course where the keyword is mentioned, grouped by phase.")
            
            # Group by both Phase and Course to show all results at once
            course_summary = report_df.groupby(['Academic Level', 'Course'])['Hours'].sum().reset_index()
            st.dataframe(course_summary, use_container_width=True, hide_index=True)

elif report_type == "Program Outcome (MEPO) Analysis":
    st.header("Medical Education Program Outcome (MEPO) Report")
    st.info("🎯 **Purpose:** For **faculty** and **course directors** to see where program-level competencies are taught and assessed within their courses and phases.")
    
    with st.sidebar.expander("MEPO Report Filters", expanded=True):
        activity_type = st.selectbox("Display where outcomes are:", ["Taught", "Assessed"])
        program_outcomes = ['All'] + sorted(df['Mapped Program Outcome'].unique().tolist())
        selected_outcome = st.selectbox("Select Program Outcome (MEPO):", program_outcomes)

    item_filter = "Instructional Method" if activity_type == "Taught" else "Assessment"
    report_df = df_filtered_by_year[df_filtered_by_year['Item'] == item_filter]

    if selected_outcome != 'All':
        report_df = report_df[report_df['Mapped Program Outcome'] == selected_outcome]

    st.subheader(f"Frequency Where MEPOs are {activity_type} ({selected_year})")
    if report_df.empty:
        st.warning("No data found for the selected criteria.")
    else:
        result = report_df.groupby(['Academic Level', 'Course']).size().reset_index(name='Frequency')
        st.dataframe(result, use_container_width=True, hide_index=True)

elif report_type == "Course Outcome Analysis":
    st.header("Course-Level Outcome Report")
    st.info("🎯 **Purpose:** For **course directors** to ensure their specific course outcomes are adequately taught and appropriately assessed within their own course.")
    
    with st.sidebar.expander("Course Outcome Filters", expanded=True):
        courses = sorted(df_filtered_by_year['Course'].unique().tolist())
        selected_course = st.selectbox("Select a Course to Analyze:", courses)

    st.subheader(f"Taught vs. Assessed Analysis for: {selected_course} ({selected_year})")
    course_df = df_filtered_by_year[df_filtered_by_year['Course'] == selected_course].copy()
    
    # Calculate taught frequency/hours
    taught_df = course_df[course_df['Item'] == 'Instructional Method']
    taught_summary = taught_df.groupby('Mapped Course Outcome').agg(
        Frequency_Taught=('Item', 'count'),
        Hours_Taught=('Hours', 'sum')
    ).reset_index()

    # Calculate assessed frequency
    assessed_df = course_df[course_df['Item'] == 'Assessment']
    assessed_summary = assessed_df.groupby('Mapped Course Outcome').agg(
        Frequency_Assessed=('Item', 'count')
    ).reset_index()
    
    if taught_summary.empty and assessed_summary.empty:
        st.warning("No mapped outcomes found for this course.")
    else:
        # Merge the two summaries
        summary_df = pd.merge(taught_summary, assessed_summary, on='Mapped Course Outcome', how='outer').fillna(0)
        # Ensure integer columns for frequencies
        summary_df['Frequency_Taught'] = summary_df['Frequency_Taught'].astype(int)
        summary_df['Frequency_Assessed'] = summary_df['Frequency_Assessed'].astype(int)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

elif report_type == "Trends Over Time (CQI)":
    st.header("Trends Over Time (Longitudinal CQI Report)")
    st.info("🎯 **Purpose:** For **CQI (Continuous Quality Improvement) processes** and **curriculum revitalization** planning to track how changes impact content hours or MEPO coverage year-over-year.")

 # --- Part 1: Sidebar for Filters ---
# This block defines all the user inputs and stores their values in variables.
with st.sidebar.expander("Trend Report Filters", expanded=True):
    trend_type = st.radio("What do you want to track?", ["Keyword Hours", "MEPO Frequency"])
    
    # Initialize variables to None
    keyword = None
    selected_outcome = None

    if trend_type == "Keyword Hours":
        keyword = st.text_input("Enter Keyword to Track", "Health Equity")
        
    elif trend_type == "MEPO Frequency":
        program_outcomes = sorted(df['Mapped Program Outcome'].unique().tolist())
        selected_outcome = st.selectbox("Select Program Outcome (MEPO) to Track:", program_outcomes)

# --- Part 2: Main Page for Results ---
# This code is OUTSIDE the sidebar block, so it renders on the main page.
# It uses the variables captured from the sidebar to run the analysis.

if trend_type == "Keyword Hours":
    if keyword:  # Only run if a keyword has been entered
        search_mask = df['Event Name'].str.contains(keyword, case=False) | df['Associated Objectives'].str.contains(keyword, case=False)
        trend_df = df[search_mask]
        result = trend_df.groupby('Academic Year')['Hours'].sum()
        
        # These display elements are now on the main page
        st.subheader(f"Trend of Instructional Hours for '{keyword}'")
        st.line_chart(result)
        st.dataframe(result)
        
elif trend_type == "MEPO Frequency":
    if selected_outcome:  # Only run if an outcome has been selected
        trend_df = df[df['Mapped Program Outcome'] == selected_outcome]
        result = trend_df.groupby('Academic Year').size()
        result.name = "Frequency"
        
        # These display elements are now on the main page
        st.subheader(f"Trend of Frequency for MEPO '{selected_outcome}'")
        st.line_chart(result)
        st.dataframe(result)