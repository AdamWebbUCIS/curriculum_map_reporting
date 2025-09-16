import streamlit as st
import pandas as pd
import numpy as np

# --- EXPANDED & CORRECTED MOCK DATA SETUP ---
# This data is modeled after the University of Cincinnati's curriculum structure.
# It includes over 100 entries over two academic years to showcase robust reporting.
data = {
    'Academic Year': ['2024-2025']*56 + ['2025-2026']*61,
    'Academic Level': ['Phase 1']*25 + ['Phase 2']*20 + ['Phase 3']*11 + ['Phase 1']*28 + ['Phase 2']*22 + ['Phase 3']*11,
    'Course': [
        # Phase 1 (2024-2025)
        'Foundations of the Human Body', 'Foundations of the Human Body', 'Foundations of the Human Body', 'Host Defense', 'Host Defense',
        'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'GI, Endo, Repro', 'GI, Endo, Repro',
        'Neuroscience', 'Neuroscience', 'Physician & Society', 'Physician & Society', 'Clinical Skills 1', 'Clinical Skills 1', 'Clinical Skills 1',
        'Foundations of the Human Body', 'Host Defense', 'Cardio, Pulm, Renal', 'GI, Endo, Repro', 'Neuroscience', 'Physician & Society', 'Clinical Skills 1',
        # Phase 2 (2024-2025)
        'Internal Medicine', 'Internal Medicine', 'Internal Medicine', 'Surgery', 'Surgery', 'Surgery', 'Pediatrics', 'Pediatrics',
        'OB/GYN', 'OB/GYN', 'Psychiatry', 'Psychiatry', 'Neurology', 'Neurology', 'Family Medicine', 'Family Medicine',
        'Internal Medicine', 'Surgery', 'Pediatrics', 'OB/GYN',
        # Phase 3 (2024-2025)
        'Emergency Medicine', 'Emergency Medicine', 'Sub-Internship (Medicine)', 'Sub-Internship (Medicine)', 'Sub-Internship (Medicine)', 'Radiology Elective',
        'Global Health Elective', 'Bioinformatics', 'Emergency Medicine', 'Sub-Internship (Surgery)', 'Global Health Elective',
        # Phase 1 (2025-2026)
        'Foundations of the Human Body', 'Foundations of the Human Body', 'Foundations of the Human Body', 'Host Defense', 'Host Defense',
        'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'Cardio, Pulm, Renal', 'GI, Endo, Repro', 'GI, Endo, Repro',
        'Neuroscience', 'Neuroscience', 'Physician & Society', 'Physician & Society', 'Physician & Society', 'Clinical Skills 1', 'Clinical Skills 1', 'Clinical Skills 1',
        'Foundations of the Human Body', 'Host Defense', 'Cardio, Pulm, Renal', 'GI, Endo, Repro', 'Neuroscience', 'Physician & Society', 'Clinical Skills 1', 'Cardio, Pulm, Renal', 'Physician & Society',
        # Phase 2 (2025-2026)
        'Internal Medicine', 'Internal Medicine', 'Internal Medicine', 'Surgery', 'Surgery', 'Surgery', 'Pediatrics', 'Pediatrics',
        'OB/GYN', 'OB/GYN', 'Psychiatry', 'Psychiatry', 'Neurology', 'Neurology', 'Family Medicine', 'Family Medicine',
        'Internal Medicine', 'Surgery', 'Pediatrics', 'OB/GYN', 'Family Medicine', 'Internal Medicine',
        # Phase 3 (2025-2026)
        'Emergency Medicine', 'Emergency Medicine', 'Sub-Internship (Medicine)', 'Sub-Internship (Medicine)', 'Sub-Internship (Medicine)', 'Radiology Elective',
        'Global Health Elective', 'Bioinformatics', 'Emergency Medicine', 'Sub-Internship (Surgery)', 'Global Health Elective'
    ],
    'Event Name': [
        # Phase 1 (2024-2025)
        'Anatomy Lab: Thorax', 'Histology Lecture', 'Genetics Small Group', 'Immunology Basics', 'Microbiology Lab',
        'ECG Workshop', 'Renal Physiology I', 'Pulmonary Function Lab', 'Pharmacology: Diuretics', 'GI Anatomy', 'Endocrine Feedback Loops',
        'Neuroanatomy Lab', 'Cranial Nerves Exam', 'Health Equity Seminar', 'Ethics: Informed Consent', 'History Taking I', 'Physical Exam: Cardiac', 'Patient Interview Assessment',
        'Anatomy Final Exam', 'Microbiology Practical', 'Pathophysiology Exam', 'GI OSCE', 'Neuro OSCE', 'Ethics Essay', 'Final OSCE',
        # Phase 2 (2024-2025)
        'Inpatient Rounds', 'Case Presentation', 'Shelf Exam Review', 'OR Observation', 'Suturing Workshop', 'Pre-Op Assessment', 'Well-Child Check', 'Vaccination Schedule',
        'Labor & Delivery', 'Gyn Clinic', 'Inpatient Psychiatry', 'CBT Workshop', 'Stroke Clinic', 'Neurology Shelf Review', 'Outpatient Clinic', 'Community Medicine Project',
        'EBM Presentation', 'Surgical Note Writing', 'Pediatric OSCE', 'OB/GYN Final Exam',
        # Phase 3 (2024-2025)
        'Trauma Bay Simulation', 'Splinting Workshop', 'Patient Admissions', 'Discharge Summaries', 'Ethics Grand Rounds', 'Reading Chest X-Rays',
        'Clinic in Rural Setting', 'Data Analysis Project', 'EM Final Exam', 'Presenting on Rounds', 'Cultural Competency Reflection',
        # Phase 1 (2025-2026)
        'Anatomy Lab: Thorax', 'Histology Lecture', 'Genetics Small Group', 'Immunology Basics', 'Microbiology Lab',
        'ECG Workshop', 'Renal Physiology I', 'Pulmonary Function Lab', 'Pharmacology: Diuretics', 'GI Anatomy', 'Endocrine Feedback Loops',
        'Neuroanatomy Lab', 'Cranial Nerves Exam', 'Health Equity Seminar', 'Ethics: Informed Consent', 'Health Disparities Research', 'History Taking I', 'Physical Exam: Cardiac', 'Patient Interview Assessment',
        'Anatomy Final Exam', 'Microbiology Practical', 'Pathophysiology Exam', 'GI OSCE', 'Neuro OSCE', 'Ethics Essay', 'Final OSCE', 'Pharmacology: Beta Blockers', 'Telemedicine Workshop',
        # Phase 2 (2025-2026)
        'Inpatient Rounds', 'Case Presentation', 'Shelf Exam Review', 'OR Observation', 'Suturing Workshop', 'Pre-Op Assessment', 'Well-Child Check', 'Vaccination Schedule',
        'Labor & Delivery', 'Gyn Clinic', 'Inpatient Psychiatry', 'CBT Workshop', 'Stroke Clinic', 'Neurology Shelf Review', 'Outpatient Clinic', 'Community Medicine Project',
        'EBM Presentation', 'Surgical Note Writing', 'Pediatric OSCE', 'OB/GYN Final Exam', 'Preventive Care OSCE', 'Geriatrics Rotation',
        # Phase 3 (2025-2026)
        'Trauma Bay Simulation', 'Splinting Workshop', 'Patient Admissions', 'Discharge Summaries', 'Ethics Grand Rounds', 'Reading Chest X-Rays',
        'Clinic in Rural Setting', 'Data Analysis Project', 'EM Final Exam', 'Presenting on Rounds', 'Cultural Competency Reflection'
    ],
    'Item': ['Instructional Method']*18 + ['Assessment']*7 + ['Instructional Method']*16 + ['Assessment']*4 + ['Instructional Method']*8 + ['Assessment']*3 + ['Instructional Method']*19 + ['Assessment']*9 + ['Instructional Method']*16 + ['Assessment']*6 + ['Instructional Method']*8 + ['Assessment']*3,
    'Associated Objectives': [
        'Identify major thoracic structures', 'Describe epithelial tissue types', 'Analyze a pedigree for genetic disorders', 'Explain innate vs. adaptive immunity', 'Perform a gram stain',
        'Interpret a basic ECG', 'Describe glomerular filtration', 'Measure lung volumes with spirometry', 'Explain diuretic mechanism of action', 'Trace the path of digestion', 'Diagram the HPA axis',
        'Identify major brain structures', 'Perform a complete cranial nerve exam', 'Define social determinants of health', 'Explain the elements of informed consent', 'Gather a complete patient history', 'Perform a cardiac physical exam', 'Demonstrate patient-centered communication',
        'Test knowledge of anatomy', 'Identify unknown microbes', 'Apply knowledge of cardiac pathophysiology', 'Assess clinical skills in GI', 'Assess clinical skills in neuro', 'Analyze an ethical dilemma', 'Assess overall clinical skills for Phase 1',
        'Formulate a differential diagnosis', 'Present a patient case effectively', 'Prepare for NBME shelf exam', 'Understand the roles in an OR', 'Demonstrate basic surgical skills', 'Evaluate a patient for surgery', 'Perform a developmental screening', 'Recall pediatric vaccine schedule',
        'Manage a patient in labor', 'Perform a speculum exam', 'Conduct a psychiatric interview', 'Apply principles of cognitive behavioral therapy', 'Localize a neurological lesion', 'Prepare for neurology shelf exam', 'Manage common outpatient conditions', 'Address a community health need',
        'Critically appraise a research article', 'Write a SOAP note', 'Assess pediatric history taking', 'Test knowledge of OB/GYN',
        'Manage an unstable patient', 'Apply a splint correctly', 'Admit a new patient to the floor', 'Write a safe discharge summary', 'Discuss complex ethical cases', 'Identify common pathologies on CXR',
        'Experience healthcare in a low-resource setting', 'Use python for data analysis', 'Test knowledge of emergency medicine', 'Function as a PGY-1 intern', 'Reflect on cross-cultural patient encounters',
        'Identify major thoracic structures', 'Describe epithelial tissue types', 'Analyze a pedigree for genetic disorders', 'Explain innate vs. adaptive immunity', 'Perform a gram stain',
        'Interpret a basic ECG', 'Describe glomerular filtration', 'Measure lung volumes with spirometry', 'Explain diuretic mechanism of action', 'Trace the path of digestion', 'Diagram the HPA axis',
        'Identify major brain structures', 'Perform a complete cranial nerve exam', 'Define social determinants of health', 'Explain the elements of informed consent', 'Analyze data on local health disparities', 'Gather a complete patient history', 'Perform a cardiac physical exam', 'Demonstrate patient-centered communication',
        'Test knowledge of anatomy', 'Identify unknown microbes', 'Apply knowledge of cardiac pathophysiology', 'Assess clinical skills in GI', 'Assess clinical skills in neuro', 'Analyze an ethical dilemma', 'Assess overall clinical skills for Phase 1', 'Explain beta blocker pharmacology', 'Demonstrate use of telemedicine platform',
        'Formulate a differential diagnosis', 'Present a patient case effectively', 'Prepare for NBME shelf exam', 'OR Observation', 'Suturing Workshop', 'Pre-Op Assessment', 'Well-Child Check', 'Vaccination Schedule',
        'Manage a patient in labor', 'Perform a speculum exam', 'Conduct a psychiatric interview', 'Apply principles of cognitive behavioral therapy', 'Localize a neurological lesion', 'Prepare for neurology shelf exam', 'Manage common outpatient conditions', 'Address a community health need',
        'Critically appraise a research article', 'Write a SOAP note', 'Assess pediatric history taking', 'Test knowledge of OB/GYN', 'Assess preventive care skills', 'Manage care for older adults',
        'Manage an unstable patient', 'Apply a splint correctly', 'Admit a new patient to the floor', 'Write a safe discharge summary', 'Discuss complex ethical cases', 'Identify common pathologies on CXR',
        'Experience healthcare in a low-resource setting', 'Use python for data analysis', 'Test knowledge of emergency medicine', 'Function as a PGY-1 intern', 'Reflect on cross-cultural patient encounters'
    ],
    'Mapped Program Outcome': [
        'MK-1', 'MK-1', 'MK-2', 'MK-1', 'PC-1', 'PC-2', 'MK-1', 'PC-1', 'MK-4', 'MK-1', 'MK-1', 'MK-1', 'PC-2', 'SBP-1', 'PROF-1', 'ICS-1', 'PC-2', 'ICS-2', 'MK-1', 'PC-1', 'MK-1', 'PC-2', 'PC-2', 'PROF-1', 'PC-2',
        'PC-4', 'ICS-2', 'PBLI-1', 'PROF-2', 'PC-1', 'PC-3', 'PC-3', 'MK-3', 'PC-5', 'PC-5', 'PC-6', 'ICS-1', 'MK-1', 'PBLI-1', 'PC-3', 'SBP-2', 'PBLI-2', 'ICS-2', 'PC-3', 'MK-3',
        'PC-7', 'PC-1', 'PC-8', 'ICS-2', 'PROF-1', 'MK-1', 'SBP-3', 'PBLI-3', 'MK-5', 'PC-8', 'PROF-3',
        'MK-1', 'MK-1', 'MK-2', 'MK-1', 'PC-1', 'PC-2', 'MK-1', 'PC-1', 'MK-4', 'MK-1', 'MK-1', 'MK-1', 'PC-2', 'SBP-1', 'PROF-1', 'SBP-1', 'ICS-1', 'PC-2', 'ICS-2', 'MK-1', 'PC-1', 'MK-1', 'PC-2', 'PC-2', 'PROF-1', 'PC-2', 'MK-4', 'SBP-4',
        'PC-4', 'ICS-2', 'PBLI-1', 'PROF-2', 'PC-1', 'PC-3', 'PC-3', 'MK-3', 'PC-5', 'PC-5', 'PC-6', 'ICS-1', 'MK-1', 'PBLI-1', 'PC-3', 'SBP-2', 'PBLI-2', 'ICS-2', 'PC-3', 'MK-3', 'PC-3', 'PC-4',
        'PC-7', 'PC-1', 'PC-8', 'ICS-2', 'PROF-1', 'MK-1', 'SBP-3', 'PBLI-3', 'MK-5', 'PC-8', 'PROF-3'
    ],
    'Mapped Course Outcome': [
        'FHB-1', 'FHB-1', 'FHB-2', 'HD-1', 'HD-2', 'CPR-1', 'CPR-2', 'CPR-3', 'CPR-4', 'GER-1', 'GER-2', 'NEURO-1', 'NEURO-2', 'PS-1', 'PS-2', 'CS1-1', 'CS1-2', 'CS1-3', 'FHB-1', 'HD-2', 'CPR-1', 'GER-1', 'NEURO-2', 'PS-2', 'CS1-3',
        'IM-1', 'IM-2', 'IM-3', 'SURG-1', 'SURG-2', 'SURG-3', 'PEDS-1', 'PEDS-2', 'OB-1', 'OB-2', 'PSYCH-1', 'PSYCH-2', 'NEURO-C-1', 'NEURO-C-2', 'FM-1', 'FM-2', 'IM-2', 'SURG-3', 'PEDS-1', 'OB-1',
        'EM-1', 'EM-2', 'SUBI-M-1', 'SUBI-M-2', 'SUBI-M-3', 'RAD-1', 'GH-1', 'BIO-1', 'EM-1', 'SUBI-S-1', 'GH-2',
        'FHB-1', 'FHB-1', 'FHB-2', 'HD-1', 'HD-2', 'CPR-1', 'CPR-2', 'CPR-3', 'CPR-4', 'GER-1', 'GER-2', 'NEURO-1', 'NEURO-2', 'PS-1', 'PS-2', 'PS-3', 'CS1-1', 'CS1-2', 'CS1-3', 'FHB-1', 'HD-2', 'CPR-1', 'GER-1', 'NEURO-2', 'PS-2', 'CS1-3', 'CPR-4', 'PS-4',
        'IM-1', 'IM-2', 'IM-3', 'SURG-1', 'SURG-2', 'SURG-3', 'PEDS-1', 'PEDS-2', 'OB-1', 'OB-2', 'PSYCH-1', 'PSYCH-2', 'NEURO-C-1', 'NEURO-C-2', 'FM-1', 'FM-2', 'IM-2', 'SURG-3', 'PEDS-1', 'OB-1', 'FM-3', 'IM-4',
        'EM-1', 'EM-2', 'SUBI-M-1', 'SUBI-M-2', 'SUBI-M-3', 'RAD-1', 'GH-1', 'BIO-1', 'EM-1', 'SUBI-S-1', 'GH-2'
    ],
    'Hours': [
        4, 2, 3, 2, 4, 3, 2, 3, 2, 2, 2, 4, 2, 2, 2, 4, 4, 2, 3, 3, 3, 2, 2, 4, 4,
        160, 4, 8, 40, 4, 8, 80, 4, 120, 40, 80, 8, 40, 8, 80, 8, 4, 4, 2, 2,
        4, 4, 160, 4, 2, 8, 8, 4, 2, 160, 2,
        4, 2, 3, 2, 4, 3, 2, 3, 2, 2, 2, 4, 2, 3, 2, 4, 4, 4, 2, 3, 3, 3, 2, 2, 4, 4, 2, 3,
        160, 4, 8, 40, 4, 8, 80, 4, 120, 40, 80, 8, 40, 8, 80, 8, 4, 4, 2, 2, 2, 40,
        4, 4, 160, 4, 2, 8, 8, 4, 2, 160, 2
    ]
}

df = pd.DataFrame(data)

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

    with st.sidebar.expander("Trend Report Filters", expanded=True):
        trend_type = st.radio("What do you want to track?", ["Keyword Hours", "MEPO Frequency"])
        if trend_type == "Keyword Hours":
            keyword = st.text_input("Enter Keyword to Track", "Health Equity")
            if keyword:
                search_mask = df['Event Name'].str.contains(keyword, case=False) | df['Associated Objectives'].str.contains(keyword, case=False)
                trend_df = df[search_mask]
                result = trend_df.groupby('Academic Year')['Hours'].sum()
                st.subheader(f"Trend of Instructional Hours for '{keyword}'")
                st.line_chart(result)
                st.dataframe(result)

        elif trend_type == "MEPO Frequency":
            program_outcomes = sorted(df['Mapped Program Outcome'].unique().tolist())
            selected_outcome = st.selectbox("Select Program Outcome (MEPO) to Track:", program_outcomes)
            if selected_outcome:
                trend_df = df[df['Mapped Program Outcome'] == selected_outcome]
                result = trend_df.groupby('Academic Year').size()
                result.name = "Frequency"
                st.subheader(f"Trend of Frequency for MEPO '{selected_outcome}'")
                st.line_chart(result)
                st.dataframe(result)