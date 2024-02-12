from utils.utils import *
import datetime

def create_form_course():
    with st.form("New Course", clear_on_submit=True):
        st.header(":blue[Add Course:]")
        # parameters
        type = get_info("Type", "Course")
        code = st.text_input("Course code", placeholder="CT000")
        name = st.text_input("Course name", placeholder="Enter the name of the course")
        category = st.selectbox("Type", type)
        level = st.slider("Level", 1, 4)
        # final dictionary with all parameters
        insert_dict = {"CId": code, "name": name, "Type": category, "Level": level}
        # submit button fundamental for the form
        submitted = st.form_submit_button("Submit", type='primary')
    if submitted:
        # check that the insertion was successful or not
        if insert(insert_dict, "Course"):
            st.success("You have added this course!", icon='✅')

def create_form_lesson():
    with st.form("New Lesson", clear_on_submit=False):
        st.header(":blue[Add Lesson:]")
        # parameters
        ssn_info = get_info("SSN", "Trainer")
        ssn = st.selectbox("SSN", ssn_info)
        code_info = get_info("CId", "Course")
        code = st.selectbox("CId", code_info)
        slide = st.slider( "Schedule the lesson:", value=(datetime.time(10, 00)))
        startTime = slide.strftime("%H:%M:00")
        duration = st.slider("Duration", 15, 60)
        gymroom =st.text_input("Gym Room", placeholder="S0")
        day = st.selectbox('Which day of the week?', ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'))
        # final dictionary with all parameters
        insert_dict = {"SSN": ssn, "Day": day, "startTime": startTime, "Duration": duration, "GymRoom": gymroom,  "CId": code}
        # submit button fundamental for the form
        submitted = st.form_submit_button("Submit", type='primary')
        courses_same_day= get_list_where(day, "Schedule")
    if submitted:
        if gymroom == "":
            st.error("Pick a gym room", icon='⚠️')
        elif code not in courses_same_day:
            if insert(insert_dict, "Schedule"):
                st.success("You have added this lesson!", icon='✅')
        else:
            st.error("A lesson of the same course is already present on that day", icon='⚠️')

if __name__ == "__main__":
    st.title("➕ Add")
    # creation of two tabs
    course_form, lesson_form = st.tabs(["Insert Course", "Insert Lesson"])
    if check_connection():
        with course_form:
            create_form_course()
        with lesson_form:
            create_form_lesson()
