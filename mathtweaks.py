import streamlit as st
import random

# Initialize session state variables
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "answered" not in st.session_state:
    st.session_state.answered = False
if "user_answer" not in st.session_state:
    st.session_state.user_answer = None

# Function to generate math problems
def generate_question(difficulty):
    if difficulty == "Easy":
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
    elif difficulty == "Medium":
        num1, num2 = random.randint(10, 50), random.randint(10, 50)
    else:  # Hard
        num1, num2 = random.randint(50, 100), random.randint(50, 100)
    
    operation = random.choice(["+", "-", "*"])
    
    question = f"{num1} {operation} {num2}"
    
    if operation == "+":
        answer = num1 + num2
    elif operation == "-":
        answer = num1 - num2
    else:  # Multiplication
        answer = num1 * num2
    
    return question, answer

# Home Screen
st.title("Math Game!")
st.write("Welcome to the Math Game! Select a difficulty and start the quiz.")

# Difficulty Selection
difficulty = st.selectbox("Select Difficulty:", ["Easy", "Medium", "Hard"])
st.session_state.difficulty = difficulty

# Start Quiz Button
if st.button("Start Quiz", use_container_width=True):
    st.session_state.quiz_started = True
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.current_question, st.session_state.correct_answer = generate_question(st.session_state.difficulty)
    st.session_state.answered = False
    st.session_state.user_answer = None

# Quiz Section
if st.session_state.quiz_started:
    st.header(f"Question {st.session_state.question_count + 1}")
    
    # Display question
    st.write(f"What is {st.session_state.current_question}?")
    
    # Input field for user answer
    user_answer = st.number_input("Enter your answer:", value=None, step=1, key="user_answer", placeholder="Type your answer here")
    
    # Auto-check answer when user presses Enter
    if user_answer is not None and user_answer != st.session_state.user_answer:
        st.session_state.user_answer = user_answer
        if user_answer == st.session_state.correct_answer:
            st.success("Correct! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! The correct answer was {st.session_state.correct_answer}.")
        st.session_state.answered = True
    
    # Show "Next Question" button only after checking the answer
    if st.session_state.answered and st.button("Next Question"):
        st.session_state.question_count += 1
        
        # Generate new question if quiz is not over
        if st.session_state.question_count < 10:
            st.session_state.current_question, st.session_state.correct_answer = generate_question(st.session_state.difficulty)
            st.session_state.answered = False
            st.session_state.user_answer = None
        else:
            st.subheader("Quiz Complete!")

            # Show final score and message
            if st.session_state.score >= 8:
                st.success("You did great! 🎉")
            elif 6 <= st.session_state.score <= 7:
                st.info("You did good!")
            else:
                st.warning("You can do better!")

            st.write(f"Final Score: {st.session_state.score}/10")

            # Play Again Button
            if st.button("Play Again"):
                st.session_state.quiz_started = False
                st.session_state.score = 0
                st.session_state.question_count = 0
                st.session_state.current_question = None
                st.session_state.correct_answer = None
                st.session_state.user_answer = None