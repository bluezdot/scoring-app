import json
import os
import pandas as pd
import streamlit as st

exams = {}
key_file = 'exam.json'
        
if os.path.exists(key_file):
    with open(key_file, 'r') as f:
        exams = json.load(f)

if 'code' not in st.session_state:
    st.session_state['code'] = ''
if 'ans' not in st.session_state:
    st.session_state['ans'] = ''

def add():
    
    if exams != {}:
        st.subheader('Modify exist exam')
        for k, v in exams.items():
            temp_ans = v['ans']
            if k and st.button(f'Exam {k} : {temp_ans}'):
                st.session_state['code'] = k
                st.session_state['ans'] = temp_ans

    st.subheader('Create new exam')
    code = st.text_input('Exam code', value=st.session_state['code'])
    ans = st.text_input('Answer key', value=st.session_state['ans'])
    num_q = st.number_input('Number of questions', step=1, value=len(ans))
    exams[code] = {'numq': num_q, 'ans': ans}
    if st.button('Save'):
        if len(ans) == num_q:
            with open(key_file, 'w') as f:
                json.dump(exams, f)
            st.success(f'Exam {code} saved.')
        else:
            st.error('Error: Answer key length does not match number of questions.')
    
def grade():
    grade_file = 'grade.csv'
    if os.path.exists(grade_file):
        df = pd.read_csv(grade_file)
        df = df[['Name', 'Grade']].sort_values('Grade', ascending=False)
        st.subheader('Grades')
        st.dataframe(df)
        
        bins = [i for i in range(0, 11, 1)]
        labels = ['0 - 1', '1 - 2', '2 - 3', '3 - 4', '4 - 5', '5 - 6', '6 - 7', '7 - 8', '8 - 9', '9 - 10']
        df['bins'] = pd.cut(df['Grade'], bins=bins, labels=labels, include_lowest=True)
        st.bar_chart(df['bins'].value_counts())
        # st.bar_chart(df['Grade'].value_counts(bins=10), x = [f'{i}' for i in range(0, 11, 1)])
    
    st.subheader('Calculate Grade Exam')
    code = st.selectbox('Select exam code', list(exams.keys()))
    if code:
        name = st.text_input('Student name')
        stud = st.text_input(
            f'Student answers as a string, with spaces for unanswered questions'
        )
        if st.button('Save Answer'):
            ans = exams[code]['ans']
            num_q = exams[code]['numq']
            
            if len(name):
                if len(stud) == num_q:
                    num_correct = sum([1 for i in range(num_q) if stud[i] == ans[i]])
                    grade = num_correct / num_q * 10
                    st.success(
                        f'{name} got {num_correct} out of {num_q} correct, grade {grade}'
                    )

                    grade_file = 'grade.csv'
                    data = {
                        'Name': [name],
                        'Exam Code': [code],
                        'Number Correct': [num_correct],
                        'Total Questions': [num_q],
                        'Grade': [grade],
                    }
                    if os.path.exists(grade_file):
                        df = pd.read_csv(grade_file)
                        df = pd.concat([df, pd.DataFrame(data)])
                        df.sort_values('Name', inplace=True)
                        df.to_csv(grade_file, index=False)
                    else:
                        pd.DataFrame(data).to_csv(grade_file, index=False)
                else:
                    st.warning(
                        f'Invalid number of answers: expected {num_q}, got {len(stud)}'
                    )
            else:
                st.warning('Please enter student name')

st.sidebar.title('Multiple Choice Exam Grader')
page = st.sidebar.selectbox('Select an option', ('Add Exam', 'Grade Exam'))

if page == 'Add Exam':
    add()
else:
    grade()