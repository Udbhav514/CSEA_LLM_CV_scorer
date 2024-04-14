import streamlit as st
import pandas as pd
import funct
import fitz
from io import StringIO

template = {
    "jee_mains_rank": {"weight": 0.05, "default": 2000, "prefers_higher": False},
    "jee_advanced_rank": {"weight": 0.05, "default": 2000, "prefers_higher": False},
    "codeforces_rating": {"weight": 0.15, "default": 1200, "prefers_higher": True},
    "codeforces_contest_rank": {"weight": 0.1, "default": 1000, "prefers_higher": False},
    "codechef_rating": {"weight": 0.1, "default": 1600, "prefers_higher": True},
    "cpi": {"weight": 0.2, "default": 8, "prefers_higher": True},
    "board_12th_percentage": {"weight": 0.05, "default": 90, "prefers_higher": True},
    "board_10th_percentage": {"weight": 0.05, "default": 90, "prefers_higher": True},
    "number_of_projects": {"weight": 0.1, "default": 0, "prefers_higher": True},
    "number_of_internships": {"weight": 0.05, "default": 0, "prefers_higher": True},
    "number_of_research_experience": {"weight": 0.1, "default": 0, "prefers_higher": True},
    "total_experience": {"weight": 0.1, "default": 0, "prefers_higher": True}
}



import json
import re




st.title('WELCOME')

col1, col2 = st.columns(2)
uploaded_files = []
num= 0 
text =[]
import pdfplumber
from io import BytesIO



with col1:
    role = st.selectbox('Which role would you like to hire for?',     ('Technical', 'Financial', 'Designer'))
    st.write('You selected:', role)
    criteria = "" 

    criteria = st.text_input(label="Please Mention Any Additional Criteria")
    
    num = st.text_input(label="Number of Candidates")
    # try:
    #     num = int(num)  # Convert num to integer safely
    # except ValueError:
    #     st.error("Please enter a valid number")
    #     # Stop further execution if num is not valid

    if num.isdigit():  
        for i in range(int(num)):
            uploaded_file = st.file_uploader(f"Upload your file #{i+1}", key=f"file_uploader_{i}")
            if uploaded_file is not None:
                uploaded_files.append(uploaded_file)

        # Displaying details of uploaded files
        if uploaded_files:
            st.write("Uploaded Files:")
            for uploaded_file in uploaded_files:
                st.write(uploaded_file.name)
    if st.button('SUBMIT',type="primary"):
        if((int(num)==0)or(len(uploaded_files)!=int(num)) ):            
            st.write("Please enter all details")
            # st.write(num, len(uploaded_files))

        else:
            for i in range(int(num)):
                with pdfplumber.open(BytesIO(uploaded_files[i].getvalue())) as pdf:
                    text1 = ''
                    for page in pdf.pages:
                        text1 += page.extract_text() + '\n'  # Extracting text from each page
                    text.append(text1)
            response =[]        
            for i in range(int(num)):
                responsei = funct.giveFinalScore(text[i],role,criteria)
                response.append(responsei)
            
            temp = "["
            for i in response:
                temp = temp + i + ","
            temp = temp[:-1] + "]"

            answer_list = funct.create_scores_dict(temp, template)

            st.write(answer_list)

# with col2:
 

# Open the PDF filet.text_area("Extracted Text", text, height=300)
    
            

# with col2:
#     name_and_rank = get_name_rank()
#     st.dataframe(pd.DataFrame(name_and_rank, columns = ["Name","Rank"]),use_container_width=True)
#     print(name_and_rank)
