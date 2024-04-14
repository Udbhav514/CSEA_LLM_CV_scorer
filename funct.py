import fitz
import google.generativeai as genai
import json
import re
import streamlit as st

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



def create_scores_dict(json_str, template):
    def normalize_entry(entry, max_values, min_values, template):
        normalized_entry = {}
        for key in template.keys():
            value = entry.get(key)
            if value is not None:
                if template[key]['prefers_higher']:
                    if max_values[key] == min_values[key]:
                        normalized_entry[key] = 1
                    else:
                        normalized_entry[key] = (value - min_values[key]) / (max_values[key] - min_values[key])
                else:
                    if max_values[key] == min_values[key]:
                        normalized_entry[key] = 1
                    else:
                        normalized_entry[key] = 1 - (value - min_values[key]) / (max_values[key] - min_values[key])
            else:
                normalized_entry[key] = template[key]['default']
        return normalized_entry

    def calculate_total_score(normalized_entry, template):
        total_score = 0
        for key, value in normalized_entry.items():
            total_score += value * template[key]['weight']
        return total_score

    def format(input_string):
      # Define a regular expression pattern to match non-keyboard characters
      pattern = r'[^\x20-\x7E]'
      # Use the re.sub() function to replace all non-keyboard characters with an empty string
      cleaned_string = re.sub(pattern, '', input_string)
      return cleaned_string
      # Initialize scores dictionary

    scores_dict = {}
    json_str = json_str[json_str.find("["):json_str.find("]") + 1].strip()
    json_str = format(json_str)
    # json_str = json_str.replace("\'", "")

    data = json.loads(json_str)

    # Find the maximum and minimum values for each attribute across all entries
    max_values = {key: float('-inf') for key in template}
    min_values = {key: float('inf') for key in template}
    for entry in data:
        for key, value in entry.items():
            if key in template and value is not None:
                max_values[key] = max(float(max_values[key]), float(value))
                min_values[key] = min(float(min_values[key]), float(value))

    # Normalize each entry using the maximum values and calculate total scores
    for idx, entry in enumerate(data, start=1):
        normalized_entry = normalize_entry(entry, max_values, min_values, template)
        total_score = calculate_total_score(normalized_entry, template)
        scores_dict[idx] = total_score

    def ordinal(n):
      if 10 <= n % 100 <= 20:
          suffix = 'th'
      else:
          suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
      return str(n) + suffix

    return scores_dict


# create_scores_dict(der, template)

#create_scores_dict(response.text, template)






def giveFinalScore(extracted_text,jobProfile,companyCriteria):
    
# Used to securely store your API key
# from google.colab import userdata

    GOOGLE_API_KEY= 'AIzaSyAjEGxP6kezlPGu4NTFTId3KsYLldzCMro'
    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')




    
    instruction1 = ''' You are a brilliant resume summarizer .Using the following example , summarize resumes in the exact format as given below.
    For example resume :-
    Udbhav Gupta +91-8107223633
    Roll No.:220101106 udbhavgupta0305@gmail.com
    B.Tech - Computer and Science Engineering udbhav@iitg.ac.in
    Indian Institute Of Technology, Guwahati linkedin.com/in/Udbhav Gupta
    Education
    Degree/Certificate Institute/Board CGPA/Percentage Year
    B.Tech. Major Indian Institute of Technology, Guwahati 8.86 (Current) 2022-Present
    Senior Secondary CBSE Board 92.2% 2022
    Secondary CBSE Board 94.8% 2020
    Projects
    • DocChain , A Complete Solution to Digital Identity Jan 2024 - Feb 2024
    First Prize Winner in Inter Hostel Technical Competition Github
    – Orchestrated backend architecture for blockchain-powered digital identity platform.
    – Implemented blockchain solutions for claims, voting, and property access management.
    – Leveraged Solidity, Third-Web SDK, and MetaMask Wallet API for seamless integration.
    • Live Points Leaderboard May 2023 - June 2023
    Coding Club , IIT Guwahati Github
    – Designed interactive leaderboard using JavaScript, HTML, and CSS for user-friendly contributor ranking.
    – Integrated live API data for real-time display of top contributors by points.
    • Diabetic Macular Edema Segmentation in OCT Images Oct. 2023 - Nov. 2023
    Coding Club , IIT Guwahati Github
    – Utilized UNet for diabetic macular edema in OCT images, enabling detailed analysis beyond classification.
    – Trained segmentation on 10 MATLAB files housing 61 retina images, advancing medical imaging insights.
    Skills
    • Programming: Python*, C/C++, Solidity*
    • Web Technologies: HTML ,CSS ,JavaScript*
    • Tools/Frameworks: Keras*, Tensorflow*, Pytorch*
    • Operating Systems:Windows, Linux* * Elementary proficiency
    Achievements
    • JEE Mains 2022, Secured an All India Rank of 371 among 1.2 million candidates appearing for the test 2022
    • JEE Advanced 2022, Secured an All India Rank of 514 out of 250,000 candidates appearing for the test 2022
    • KVPY SA 2020, Obtained the National research fellowship scholarship by securing an AIR of 871 2020
    • KVPY SX 2021, Secured a CRL Rank of 993 among 100,000 candidates appearing for the test 2021
    • Codeforces, Secured World Rank of 430 in Round 918 - Highest Rating 1501 (Specialist) 2023
    • Reliance Foundation Undergraduate Scholarship, Awardee for Academic Excellence 2023
    • ICPC-de-Tryst , IIT Delhi, Attained 68th rank in a competitive programming competition. 2024
    • STSE 2020, Attained 11th rank in the State examination administered by the Rajasthan Board. 2020
    • ML Hackathon , IITG.Ai, Secured third position among 155 candidates in the ML focused Hackathon. 2023
    • Kriti CP Competition, Awarded Gold Medal for achieving 1st place in the competitive programming event 2023
    • Kriti CTF Competition, Secured 1st rank in the Cybersecurity event 2023
    Key courses taken
    –Mathematics: Linear Algebra, Basic Calculus, Probability & Random Processes
    –Computer Science: Data Structures and Algorithms, Introduction to Computing
    –MOOC’s: Neural Networks and Deep Learning , Convolutional Neural Networks by Deep Learning.AI
    Positions of Responsibility
    – Coordinator, Coding Club, IIT Guwahati July. 2023 - July. 2024
    ∗ Conducted various workshops and took part in projects related to ML and Web Development
    – Associate, Consulting and Analytics Club, IIT Guwahati May. 2023 - May. 2024
    ∗ Contributed in organizing workshops and discussions centered around Consulting and Analytics within the club

    Summary :-

    Name :- Udbhav Gupta
    Degree:- B.Tech - Computer and Science Engineering
    College:- Indian Institute Of Technology, Guwahati
    *Education:*
    CGPA :- 8.86 (Current)
    Senior Secondary CBSE Board 92.2% 2022
    Secondary CBSE Board 94.8% 2020
    *Projects:* Blockchain digital identity platform, Interactive leaderboard, Diabetic macular edema segmentation
    *Skills:* Python, C/C++, Solidity, HTML, CSS, JavaScript, Keras, Tensorflow, Pytorch
    *Achievements:*
    - JEE Mains :- AIR 371/1.2M
    - JEE Advanced :- AIR 514/250K
    - KVPY SA :- AIR 871
    - KVPY SX :- CRL 993
    - Codeforces :- World Rank 430, Rating 1501
    - Scholarship :- Reliance Foundation
    - ICPC-de-Tryst :- Rank 68
    - Hackathon :- ML Hackathon 3rd Place

    *Positions of Responsibility: *
    - Coordinator, Coding Club, IIT Guwahati ,
    - Associate, Consulting and Analytics Club

    Resume :-
    '''


    resumeSummary = model.generate_content(instruction1 + extracted_text)

    if (jobProfile == "Technical"):

        analyzePrompt = """
    Input has summarisations of resume of a single candidate for a job. 
    2)RETURN IN JSON FORMAT ONE AND ONLY ONE MAP
    3))Your motive is the list all the quantifiable skills in a MAP format
    4) assign each of the skillset the explicit value as mentioned in the resume for example- jee mains rank:123
    4)A MAP should contain jee mains rank ,jee advanced rank, codeforces rating,codeforces contest rank,codechef rating, cpi, 12th board percentage,
    10th board percentage,number of internships,number of research internships,total experience for a technical resume
    The above provided set of attributes should be there in the returned MAP always
    5)If some attribute in the MAP has not been mentioned in the resume,assign to it the value null
    6)ASSIGN ONLY AND ONY MATHEMATICAL VALUES TO ATTRIBUTES. ANY NON NUMERICAL EXPRESSION MUST NOT BE PRESENT IN THE VALUES
    7) assign values only and only to its respective index. for example ranking for one attribute must not be assigned to any other attribute no matter however simiar they may sound
    8) WHILE RETURNING THE OUTPUT JSON, DO NOT MENTION JSON ANYWHERE
    9) These are the basic attributes which each MAP should always contain, further attributes to be added will also be mentioned in the
    next queries, which should be added, accordingly with null values if not present or the provided mathematical value(or count) in the resume
    
    """


    if (jobProfile == "Financial"):
        analyzePrompt = """
    Input contains summaries of a resume for a financial position. 
    2) Return in JSON format a single tuple.
        VALUES AT THE SAME INDEX IN ALL TUPLES MUST POINT AT THE SAME SKILL; these values are numerical.
    3) The tuples returned should have the identification skill and their specific values.
    4) A tuple should contain MBA entrance exam score (if applicable), CFA level passed, GMAT score,
    financial modeling certification score, number of years in financial sector, number of internships, number of finance-specific
    research projects, total experience in finance, 12th board percentage, 10th board percentage, and CPI.
    The above-provided set of attributes should always be present in the returned tuple.
    5) Each index of the tuples should point to the same skill across all resumes.
    7) Return a single tuple
    8) Your motive is to list all the quantifiable skills in a tuple format, assign each of the skill sets the explicit value as mentioned in the resume.
        Assign the value null wherever required (any quantifiable value that is a number).
    9) If some resume hasn't mentioned the GMAT score, you can assign the value null.
        Assign them with null if not present in the given resume, or with the provided value in the resume.
    10) Only assign mathematically comparable values in the tuples; the value of each tuple should be a mathematical value, not a string.
    11) You can't provide the value of some other index to some other index; for example, don’t add the score of two different exams at the same index. Create a new index and provide the value at the new index and assign it null for the resumes which don’t have it.
    13) The same set of attributes for each resume should be returned.
    14) These are the basic attributes which each tuple should always contain; further attributes to be added will also be mentioned in the next queries, which should be added accordingly with null values if not present or the provided mathematical value (or count) in the resume.
    """

    if (jobProfile == "Designer"):
        analyzePrompt = """
    Input contains summaries of resume of a single candidate for a design position. 
    2) Return in JSON format a single tuple where each attribute contains a numerical value.
        VALUES AT a INDEX for all attributes MUST POINT to a  numerical value.
    3) The tuples returned should have the identification skill and their specific values.
    4) A tuple should contain scores or levels for design-related qualifications including Adobe Creative Suite proficiency score, UX/UI certification score, graphic design portfolio rating, number of design projects completed, number of design internships, number of design awards won, total experience in design, 12th board percentage, 10th board percentage, and CPI.
        The above-provided set of attributes should always be present in the returned tuples.
    7) Return only a single tuple 
    8) Your motive is to list all the quantifiable skills in a tuple format, assign each of the skill sets the explicit value as mentioned in the resume.
        Assign the value null wherever required (any quantifiable value that is a number).
    9) If a resume hasn't mentioned the UX/UI certification score, you can assign the value null.
        Assign them with null if not present in the given resume, or with the provided value in the resume.
    10) Only assign mathematically quantifiable values in the tuples; the value of each tuple should be a mathematical value, not a string.
    11) You can't provide the value of some other index to some other index; for example, don’t add the proficiency score of one software as a substitute for another. Create a new index and provide the value at the new index and assign it null for the resumes which don’t have it.
    13) The same set of attributes for each resume should be returned.
    14) These are the basic attributes which each tuple should always contain; further attributes to be added will also be mentioned in the next queries, which should be added accordingly with null values if not present or the provided mathematical value (or count) in the resume.
    """


    response = model.generate_content(
        [resumeSummary.text, analyzePrompt, companyCriteria])
    return response.text

# giveFinalScore(extracted_text,"Technical","")    

