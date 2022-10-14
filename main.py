import streamlit as st
import streamlit_ext as ste
import openai
from streamlit_tags import st_tags

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY


def write_cover_letter(full_name, job_title, adv_tech_skills, int_tech_skills, personal_skills, job_description, contact_number, email):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=f"write a cover letter as {full_name}, contact details {email} and {contact_number}, "
               f"applying for the following job vacancy to make him "
               f"an ideal candidate based on the selection criteria and his skills. Yonatan is a {job_title}, "
               f"with advanced {adv_tech_skills} skills, intermediate {int_tech_skills} skills, and personal "
               f"skills including {personal_skills}:"
               f"\n\n{job_description}",
        temperature=0.7,
        max_tokens=278,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text']


st.header("COVER LETTER GENERATOR:")
st.write("Complete the form below and we'll do our best to bang together a bitchin cover letter for your dream job:")

with st.form("Cover Letter Generator", clear_on_submit=False):
    applicant_name = st.text_input("Full Name: ")
    contact_number = st.text_input("Contact number: ")
    email = st.text_input("Email: ")
    job_title = st.text_input("Enter your job title:")
    advanced_technical_skills = st_tags(
        label="Enter your advanced technical skills:",
        text="Press enter or tap to add more skills",
        value=[],
        suggestions=["Python", "Javascript", "Java", "C#", "C++", "Golang", "HTML", "CSS", "Microsoft Office Suite",
                     "Adobe Suite", "XPLAN", "MYOB"],
        maxtags=8,
        key="1"
    )
    intermediate_technical_skills = st_tags(
        label="Enter your intermediate technical skills:",
        text="Press enter or tap to add more skills",
        value=[],
        suggestions=["Python", "Javascript", "Java", "C#", "C++", "Golang", "HTML", "CSS", "Microsoft Office Suite",
                     "Adobe Suite", "XPLAN", "MYOB"],
        maxtags=8,
        key="2"
    )
    personal_skills = st_tags(
        label="Enter your personal skills:",
        text="Press enter or tap to add more skills",
        value=[],
        suggestions=["Able to work under pressure", "Great communication skills", "Team leader", "Team player",
                     "Fast learner", "Goal driven", "Great attention to detail", "Career driven"],
        maxtags=8,
        key="3"
    )
    job_description = st.text_area("Paste a few relevant paragraphs from the job you wish to apply for:")

    submitted = st.form_submit_button("Write my damn cover letter!")
    if submitted:
        with st.spinner("Writing cover letter..."):
            cover_letter_text = write_cover_letter(full_name=applicant_name, job_title=job_title,
                                                   adv_tech_skills=advanced_technical_skills,
                                                   int_tech_skills=intermediate_technical_skills,
                                                   personal_skills=personal_skills, job_description=job_description,
                                                   contact_number=contact_number, email=email)
            st.subheader("Your cover letter:")
            st.write(cover_letter_text)
            ste.download_button("Download", cover_letter_text,
                                f"{applicant_name} - Cover letter.txt")
