import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Math Wizards",
    page_icon="🧙‍♂️",
    layout="centered"
)

# Custom CSS for better design with improved color contrast
st.markdown("""
<style>
    .main-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #4c56af;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #5c6bc0;
    }
    .question-text {
        font-size: 28px;
        font-weight: bold;
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: #000000;  /* Black text on light background */
    }
    .correct-answer {
        color: #4caf50;
        font-weight: bold;
    }
    .wrong-answer {
        color: #f44336;
        font-weight: bold;
    }
    .score-display {
        font-size: 24px;
        font-weight: bold;
        margin: 1rem 0;
    }
    .difficulty-btn {
        background-color: #e6e6e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
    }
    .difficulty-btn:hover {
        background-color: #d1d1d1;
    }
    .active-btn {
        background-color: #bbdefb;
        border: 2px solid #2196f3;
    }
    .progress-container {
        margin: 1rem 0;
    }
    /* Dark mode adjustments */
    @media (prefers-color-scheme: dark) {
        .question-text {
            color: #ffffff;  /* White text for dark mode */
            background-color: #1e3a8a;
        }
    }
    /* Ensure all regular text has good contrast */
    p, h1, h2, h3, div {
        color: var(--text-color, inherit);
    }
</style>
""", unsafe_allow_html=True)

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
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "high_score" not in st.session_state:
    st.session_state.high_score = 0
if "timer_start" not in st.session_state:
    st.session_state.timer_start = 0
if "total_time" not in st.session_state:
    st.session_state.total_time = 0
if "answer_times" not in st.session_state:
    st.session_state.answer_times = []
if "operation_type" not in st.session_state:
    st.session_state.operation_type = "Mixed"
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "num_questions" not in st.session_state:
    st.session_state.num_questions = 10

# Function to generate math problems
def generate_question(difficulty, operation_type):
    if difficulty == "Easy":
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
    elif difficulty == "Medium":
        num1, num2 = random.randint(10, 50), random.randint(10, 50)
    else:  # Hard
        num1, num2 = random.randint(50, 100), random.randint(50, 100)
    
    if operation_type == "Mixed":
        operation = random.choice(["+", "-", "*"])
    else:
        operation = operation_type
    
    # Ensure subtraction doesn't result in negative numbers
    if operation == "-" and num1 < num2:
        num1, num2 = num2, num1
    
    # For multiplication, make numbers smaller for medium/hard to avoid excessively large answers
    if operation == "*":
        if difficulty == "Medium":
            num1, num2 = random.randint(2, 15), random.randint(2, 10)
        elif difficulty == "Hard":
            num1, num2 = random.randint(5, 20), random.randint(5, 15)
    
    # Create displayed question with proper operation symbol
    if operation == "+":
        question_text = f"{num1} + {num2}"
        answer = num1 + num2
    elif operation == "-":
        question_text = f"{num1} - {num2}"
        answer = num1 - num2
    else:  # Multiplication
        question_text = f"{num1} × {num2}"
        answer = num1 * num2
    
    return question_text, answer

# Home Screen
if not st.session_state.quiz_started:
    st.markdown("<h1 class='main-header'>🧙‍♂️ Math Wizards 🧙‍♀️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Test your math skills and become a Math Wizard!</p>", unsafe_allow_html=True)
    
    # High score display
    if st.session_state.high_score > 0:
        st.markdown(f"<p style='text-align: center;'>Your Best Score: <span style='color: #ff9800; font-weight: bold;'>{st.session_state.high_score}</span></p>", unsafe_allow_html=True)
    
    # Settings in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='font-weight: bold;'>Select Difficulty:</p>", unsafe_allow_html=True)
        difficulty_options = ["Easy", "Medium", "Hard"]
        st.session_state.difficulty = st.radio("", difficulty_options, horizontal=True, label_visibility="collapsed")
        
        st.markdown("<p style='font-weight: bold; margin-top: 20px;'>Number of Questions:</p>", unsafe_allow_html=True)
        st.session_state.num_questions = st.select_slider("", options=[5, 10, 15, 20], value=10, label_visibility="collapsed")
    
    with col2:
        st.markdown("<p style='font-weight: bold;'>Operation Type:</p>", unsafe_allow_html=True)
        operation_options = ["Mixed", "+", "-", "*"]
        operation_labels = ["Mixed", "Addition", "Subtraction", "Multiplication"]
        index = operation_options.index(st.session_state.operation_type)
        selected_index = st.radio("", operation_labels, index=index, horizontal=True, label_visibility="collapsed")
        st.session_state.operation_type = operation_options[operation_labels.index(selected_index)]
    
    # Start button with animation
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Start Math Adventure", use_container_width=True):
        st.session_state.quiz_started = True
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.streak = 0
        st.session_state.answer_times = []
        st.session_state.current_question, st.session_state.correct_answer = generate_question(
            st.session_state.difficulty, 
            st.session_state.operation_type
        )
        st.session_state.answered = False
        st.session_state.user_answer = None
        st.session_state.timer_start = time.time()
        st.session_state.feedback = ""
        # Replace experimental_rerun with rerun
        st.rerun()

# Quiz Section
if st.session_state.quiz_started:
    # Header with progress
    progress_text = f"Question {st.session_state.question_count + 1} of {st.session_state.num_questions}"
    st.markdown(f"<h2 class='sub-header'>{progress_text}</h2>", unsafe_allow_html=True)
    progress = st.session_state.question_count / st.session_state.num_questions
    st.progress(progress)
    
    # Display score and streak
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p>Score: <b>{st.session_state.score}</b></p>", unsafe_allow_html=True)
    with col2:
        streak_text = f"Streak: 🔥 × {st.session_state.streak}" if st.session_state.streak > 0 else "Streak: 0"
        st.markdown(f"<p>{streak_text}</p>", unsafe_allow_html=True)
    
    # Display question
    st.markdown(f"<div class='question-text'>{st.session_state.current_question} = ?</div>", unsafe_allow_html=True)
    
    # Input field for user answer
    user_answer = st.number_input("Your answer:", value=None, step=1, key=f"answer_{st.session_state.question_count}", placeholder="Type your answer here")
    
    # Submit button
    submit_col1, submit_col2 = st.columns([3, 1])
    with submit_col1:
        submit_button = st.button("Submit Answer", use_container_width=True)
    with submit_col2:
        hint_button = st.button("Hint 💡")
    
    # Display hint if requested
    if hint_button and not st.session_state.answered:
        question_parts = st.session_state.current_question.split()
        if len(question_parts) >= 3:
            num1 = int(question_parts[0])
            operation = question_parts[1]
            num2 = int(question_parts[2])
            
            hint_text = ""
            if operation == "+":
                hint_text = f"Try counting up from {num1}, {num2} times"
            elif operation == "-":
                hint_text = f"Try counting down from {num1}, {num2} times"
            elif operation == "×":
                hint_text = f"Think of adding {num1} to itself, {num2} times"
            
            st.info(f"Hint: {hint_text}")
    
    # Auto-check answer when user presses Enter or clicks submit
    if (user_answer is not None and user_answer != st.session_state.user_answer) or submit_button:
        if user_answer is not None:
            st.session_state.user_answer = user_answer
            answer_time = time.time() - st.session_state.timer_start
            st.session_state.answer_times.append(answer_time)
            
            if user_answer == st.session_state.correct_answer:
                st.session_state.score += 1
                st.session_state.streak += 1
                if st.session_state.streak >= 3:
                    st.session_state.feedback = "🔥 Amazing streak! Keep it up! 🔥"
                else:
                    st.session_state.feedback = "Correct! 🎉"
            else:
                st.session_state.feedback = f"Not quite! The correct answer is {st.session_state.correct_answer}."
                st.session_state.streak = 0
            
            st.session_state.answered = True
    
    # Display feedback
    if st.session_state.answered and st.session_state.feedback:
        if "Correct" in st.session_state.feedback or "Amazing" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
    
    # Show "Next Question" button only after checking the answer
    if st.session_state.answered:
        if st.button("Next Question ➡️", use_container_width=True):
            st.session_state.question_count += 1
            
            # Generate new question if quiz is not over
            if st.session_state.question_count < st.session_state.num_questions:
                st.session_state.current_question, st.session_state.correct_answer = generate_question(
                    st.session_state.difficulty,
                    st.session_state.operation_type
                )
                st.session_state.answered = False
                st.session_state.user_answer = None
                st.session_state.timer_start = time.time()
                st.session_state.feedback = ""
                # Replace experimental_rerun with rerun
                st.rerun()
            else:
                # Update high score
                if st.session_state.score > st.session_state.high_score:
                    st.session_state.high_score = st.session_state.score
                
                # Calculate total time and average time per question
                st.session_state.total_time = sum(st.session_state.answer_times)
                avg_time = st.session_state.total_time / len(st.session_state.answer_times) if st.session_state.answer_times else 0
                
                st.session_state.quiz_started = False
                # Replace experimental_rerun with rerun
                st.rerun()

# Results Screen
if not st.session_state.quiz_started and st.session_state.question_count >= st.session_state.num_questions:
    st.markdown("<h1 class='main-header'>Quiz Complete! 🏆</h1>", unsafe_allow_html=True)
    
    # Calculate percentage score
    percentage = (st.session_state.score / st.session_state.num_questions) * 100
    
    # Display different messages based on score
    if percentage >= 90:
        message = "🌟 Math Wizard Master! 🌟"
        color = "#4caf50"
    elif percentage >= 70:
        message = "⭐ Math Wizard Apprentice! ⭐"
        color = "#ff9800"
    elif percentage >= 50:
        message = "👍 Math Wizard Novice! 👍"
        color = "#2196f3"
    else:
        message = "🔍 Keep Practicing! 🔍"
        color = "#f44336"
    
    st.markdown(f"<h2 style='text-align: center; color: {color};'>{message}</h2>", unsafe_allow_html=True)
    
    # Display score
    st.markdown(f"<div class='score-display' style='text-align: center;'>Your Score: <span style='color: {color};'>{st.session_state.score}/{st.session_state.num_questions} ({percentage:.0f}%)</span></div>", unsafe_allow_html=True)
    
    # Display time statistics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p style='text-align: center;'>Total Time: <b>{st.session_state.total_time:.1f} seconds</b></p>", unsafe_allow_html=True)
    with col2:
        avg_time = st.session_state.total_time / st.session_state.num_questions
        st.markdown(f"<p style='text-align: center;'>Average: <b>{avg_time:.1f} seconds/question</b></p>", unsafe_allow_html=True)
    
    # High score display
    if st.session_state.score == st.session_state.high_score and st.session_state.high_score > 0:
        st.success("🎉 New High Score! 🎉")
    
    # Play Again Button
    if st.button("Play Again 🔄", use_container_width=True):
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.current_question = None
        st.session_state.correct_answer = None
        st.session_state.user_answer = None
        st.session_state.streak = 0
        st.session_state.timer_start = 0
        st.session_state.total_time = 0
        st.session_state.answer_times = []
        st.session_state.feedback = ""
        # Replace experimental_rerun with rerun
        st.rerun()