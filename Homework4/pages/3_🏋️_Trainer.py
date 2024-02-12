from utils.utils import *
import pandas as pd

# each tab has a separate function

def create_search_instructor (search_instructor):
    with search_instructor[0].expander("Search Instructor", True):
        text_input = st.text_input(
            "Search the surname of the instructor",
            placeholder="Surname"
        )
        if text_input:
            st.write("You entered: ", text_input)
        query_birthdate = "SELECT MIN(DateOfBirth), MAX(DateOfBirth) FROM Trainer"
        date = execute_query(st.session_state["connection"], query_birthdate)
        min_max = [dict(zip(date.keys(), result)) for result in date]
        # we know that only one tuple is returned to us
        min_value = min_max[0]['MIN(DateOfBirth)']
        max_value = min_max[0]['MAX(DateOfBirth)']
        # specify min_value and max_value to set the widget with the date range
        date_range = st.date_input("Select the date range:", value=(min_value, max_value), min_value=min_value, max_value=max_value)
        queryTotal = f"SELECT SSN, Name, Surname, DateOfBirth, Email, PhoneNo FROM Trainer WHERE Surname LIKE '%{text_input}%' AND DateOfBirth >'{date_range[0]}' AND DateOfBirth <'{date_range[1]}'"
        trainers = execute_query(st.session_state["connection"], queryTotal)
        df_trainers = pd.DataFrame(trainers)
        # check that there is data in the selected period
        if df_trainers.empty:
            st.warning("No data found.", icon='⚠️')
        else:
            # transform to float and date type
            for row in df_trainers.iterrows():
                st.markdown(f" :blue[Trainer:]  {row[1]['SSN']} {row[1]['Name']} {row[1]['Surname']} {row[1]['DateOfBirth']} {row[1]['Email']} {row[1]['PhoneNo']}")
                df_trainers['DateOfBirth'] = pd.to_datetime(df_trainers['DateOfBirth'])
            st.write("Period", date_range[0], '-', date_range[1])

if __name__ == "__main__":
    st.title("🏋️ Trainer")
    # creation of one single tab
    search_instructor = st.tabs(["Search Trainer"])
    if check_connection():
        create_search_instructor(search_instructor=search_instructor)