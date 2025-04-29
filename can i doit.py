import streamlit as st
import random
import time

# Set page configuration
st.set_page_config(
    page_title="Math Wizards",
    page_icon="🧙‍♂️",
    layout="centered"
)

# Custom CSS for better design - updated with blue font and gray background
st.markdown("""
<style>
    body {
        color: #1e88e5;
        background-color: #f0f0f0;
    }
    .main-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #1e88e5;
    }
    .question-text {
        font-size: 28px;
        font-weight: bold;
        background-color: #e0e0e0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        color: #1e88e5;
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
        color: #1e88e5;
    }
    .difficulty-btn {
        background-color: #d1d1d1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
    }
    .difficulty-btn:hover {
        background-color: #c1c1c1;
    }
    .active-btn {
        background-color: #90caf9;
        border: 2px solid #1e88e5;
    }
    .progress-container {
        margin: 1rem 0;
    }
    .hearts-container {
        font-size: 24px;
        text-align: center;
        margin: 10px 0;
    }
    .tutorial-container {
        background-color: #e0e0e0;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1e88e5;
        color: #1e88e5;
    }
    /* Override ALL text elements to be blue */
    p, h1, h2, h3, h4, h5, h6, li, span, div, label, .stMarkdown, .stText, .stCode {
        color: #1e88e5 !important;
    }
    /* Override Streamlit's base styles */
    .stApp {
        background-color: #f0f0f0;
    }
    .stButton button {
        color: #1e88e5 !important;
        background-color: #d1d1d1;
    }
    .stButton button:hover {
        color: #1e88e5 !important;
        background-color: #c1c1c1;
    }
    .stNumberInput input {
        color: #1e88e5 !important;
    }
    .stRadio label {
        color: #1e88e5 !important;
    }
    /* Style success/error messages */
    .stSuccess {
        color: #1e88e5 !important;
        background-color: #d1d1d1;
    }
    .stError {
        color: #1e88e5 !important;
        background-color: #d1d1d1;
    }
    .stInfo {
        color: #1e88e5 !important;
        background-color: #d1d1d1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "home"  # home, tutorial, game, gameover
if "score" not in st.session_state:
    st.session_state.score = 0
if "hearts" not in st.session_state:
    st.session_state.hearts = 3
if "difficulty_level" not in st.session_state:
    st.session_state.difficulty_level = 1  # 1: easy, 2: medium, 3: hard
if "max_number" not in st.session_state:
    st.session_state.max_number = 10
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
if "operation_type" not in st.session_state:
    st.session_state.operation_type = "Mixed"
if "feedback" not in st.session_state:
    st.session_state.feedback = ""
if "tutorial_step" not in st.session_state:
    st.session_state.tutorial_step = 1
if "question_range" not in st.session_state:
    st.session_state.question_range = 10  # Default range 1-10
if "input_key" not in st.session_state:
    st.session_state.input_key = 0  # Key for input field to force refresh

# Function to generate math problems
def generate_question(max_number, operation_type):
    num1 = random.randint(1, max_number)
    num2 = random.randint(1, max_number)
    
    if operation_type == "Mixed":
        operation = random.choice(["+", "-", "*", "/"])
    else:
        operation = operation_type
    
    # Ensure subtraction doesn't result in negative numbers
    if operation == "-" and num1 < num2:
        num1, num2 = num2, num1
    
    # For division, ensure clean division (no remainders)
    if operation == "/":
        # Create a divisible problem
        num2 = random.randint(1, min(max_number, 10))  # Smaller divisor to avoid complexity
        answer = random.randint(1, max(1, int(max_number/num2)))
        num1 = num2 * answer
        question_text = f"{num1} ÷ {num2}"
        return question_text, answer
    
    # For multiplication, keep numbers manageable
    if operation == "*":
        if max_number > 10:
            num1 = random.randint(1, min(max_number, 12))
            num2 = random.randint(1, min(max_number, 12))
    
    if operation == "+":
        answer = num1 + num2
        question_text = f"{num1} + {num2}"
    elif operation == "-":
        answer = num1 - num2
        question_text = f"{num1} - {num2}"
    elif operation == "*":
        answer = num1 * num2
        question_text = f"{num1} × {num2}"
    
    return question_text, answer

# Function to adjust difficulty based on streak
def adjust_difficulty():
    # If player gets 5 consecutive correct answers, increase difficulty
    if st.session_state.streak == 5:
        # Increase difficulty level (max 3)
        if st.session_state.difficulty_level < 3:
            st.session_state.difficulty_level += 1
            if st.session_state.difficulty_level == 2:
                st.session_state.max_number = 15
            else:
                st.session_state.max_number = 20
            st.session_state.feedback = "Difficulty increased! 🔼"
        st.session_state.streak = 0  # Reset streak after increasing difficulty

# Tutorial content
def show_tutorial():
    st.markdown("<h1 class='main-header'>🧙‍♂️ Tutorial 📚</h1>", unsafe_allow_html=True)
    
    # Different tutorial steps
    if st.session_state.tutorial_step == 1:
        st.markdown("""
        <div class='tutorial-container'>
            <h3>Welcome to Math Wizards! 👋</h3>
            <p>In this game, you'll solve math problems to become a true Math Wizard.</p>
            <p>You'll start with <strong>3 hearts ❤️❤️❤️</strong>. Each wrong answer costs you one heart.</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.tutorial_step == 2:
        st.markdown("""
        <div class='tutorial-container'>
            <h3>Operations & Settings ⚙️</h3>
            <p>You can choose from:</p>
            <ul>
                <li>Addition (+)</li>
                <li>Subtraction (-)</li>
                <li>Multiplication (×)</li>
                <li>Division (÷)</li>
                <li>Mixed (all operations)</li>
            </ul>
            <p>You can also select the range of numbers (1-10, 1-15, or 1-20).</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.tutorial_step == 3:
        st.markdown("""
        <div class='tutorial-container'>
            <h3>Adaptive Difficulty 📈</h3>
            <p>The game gets harder as you improve!</p>
            <p>After 5 correct answers in a row, the difficulty will increase automatically.</p>
            <p>Keep your streak going to test your skills at higher levels!</p>
        </div>
        """, unsafe_allow_html=True)
    
    elif st.session_state.tutorial_step == 4:
        st.markdown("""
        <div class='tutorial-container'>
            <h3>Ready to Play? 🚀</h3>
            <p>Answer as many questions as you can before losing all your hearts.</p>
            <p>Try to beat your high score each time!</p>
            <p><strong>Good luck, Math Wizard!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.tutorial_step > 1:
            if st.button("⬅️ Previous"):
                st.session_state.tutorial_step -= 1
                st.rerun()
    
    with col3:
        if st.session_state.tutorial_step < 4:
            if st.button("Next ➡️"):
                st.session_state.tutorial_step += 1
                st.rerun()
        else:
            if st.button("Start Game 🎮"):
                st.session_state.page = "home"
                st.rerun()

# Home Screen
def show_home():
    st.markdown("<h1 class='main-header'>🧙‍♂️ Math Wizards 🧙‍♀️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Test your math skills and become a Math Wizard!</p>", unsafe_allow_html=True)
    
    # High score display
    if st.session_state.high_score > 0:
        st.markdown(f"<p style='text-align: center;'>Your Best Score: <span style='font-weight: bold;'>{st.session_state.high_score}</span></p>", unsafe_allow_html=True)
    
    # Settings in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='font-weight: bold;'>Select Number Range:</p>", unsafe_allow_html=True)
        range_options = ["1-10", "1-15", "1-20"]
        selected_range = st.radio("", range_options, horizontal=True, label_visibility="collapsed")
        st.session_state.question_range = int(selected_range.split("-")[1])
        
        st.markdown("<p style='font-weight: bold; margin-top: 20px;'>Hearts:</p>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:24px;'>❤️❤️❤️</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<p style='font-weight: bold;'>Operation Type:</p>", unsafe_allow_html=True)
        operation_options = ["Mixed", "+", "-", "*", "/"]
        operation_labels = ["Mixed", "Addition", "Subtraction", "Multiplication", "Division"]
        
        try:
            index = operation_options.index(st.session_state.operation_type)
        except ValueError:
            index = 0
            
        selected_index = st.radio("", operation_labels, index=index, horizontal=True, label_visibility="collapsed")
        st.session_state.operation_type = operation_options[operation_labels.index(selected_index)]
    
    # Control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Tutorial", use_container_width=True):
            st.session_state.tutorial_step = 1
            st.session_state.page = "tutorial"
            st.rerun()
    
    with col2:
        if st.button("🚀 Start Game", use_container_width=True):
            start_new_game()
            st.rerun()

# Start a new game
def start_new_game():
    st.session_state.page = "game"
    st.session_state.score = 0
    st.session_state.hearts = 3
    st.session_state.difficulty_level = 1
    st.session_state.max_number = st.session_state.question_range
    st.session_state.streak = 0
    st.session_state.current_question, st.session_state.correct_answer = generate_question(
        st.session_state.max_number,
        st.session_state.operation_type
    )
    st.session_state.answered = False
    st.session_state.user_answer = None
    st.session_state.timer_start = time.time()
    st.session_state.feedback = ""
    st.session_state.input_key += 1  # Increment input key to reset the input field

# Game Screen
def show_game():
    # Display hearts
    heart_display = "❤️" * st.session_state.hearts + "🖤" * (3 - st.session_state.hearts)
    st.markdown(f"<div class='hearts-container'>{heart_display}</div>", unsafe_allow_html=True)
    
    # Display difficulty level and score
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<p>Score: <b>{st.session_state.score}</b></p>", unsafe_allow_html=True)
    with col2:
        diff_text = ["Easy", "Medium", "Hard"][st.session_state.difficulty_level - 1]
        st.markdown(f"<p>Difficulty: <b>{diff_text}</b> (1-{st.session_state.max_number})</p>", unsafe_allow_html=True)
    
    # Display streak
    streak_text = f"Streak: 🔥 × {st.session_state.streak}" if st.session_state.streak > 0 else "Streak: 0"
    st.markdown(f"<p>{streak_text}</p>", unsafe_allow_html=True)
    
    # Display question
    st.markdown(f"<div class='question-text'>{st.session_state.current_question} = ?</div>", unsafe_allow_html=True)
    
    # Input field for user answer - use a unique key each time to force reset
    user_answer = st.number_input("Your answer:", key=f"answer_input_{st.session_state.input_key}", 
                                 value=None, step=1, placeholder="Type your answer here")
    
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
            elif operation == "÷":
                hint_text = f"How many times does {num2} go into {num1}?"
            
            st.info(f"Hint: {hint_text}")
    
    # Check answer ONLY when submit button is clicked
    if submit_button and not st.session_state.answered:
        if user_answer is not None:
            st.session_state.user_answer = user_answer
            
            if user_answer == st.session_state.correct_answer:
                # Correct answer
                st.session_state.score += 1
                st.session_state.streak += 1
                
                # Check for streak-based difficulty adjustment
                adjust_difficulty()
                
                if "Difficulty increased" in st.session_state.feedback:
                    pass  # Keep the difficulty increased message
                elif st.session_state.streak >= 3:
                    st.session_state.feedback = "🔥 Amazing streak! Keep it up! 🔥"
                else:
                    st.session_state.feedback = "Correct! 🎉"
            else:
                # Wrong answer
                st.session_state.feedback = f"Not quite! The correct answer is {st.session_state.correct_answer}."
                st.session_state.streak = 0
                st.session_state.hearts -= 1
                
                # Check for game over
                if st.session_state.hearts <= 0:
                    # Update high score if needed
                    if st.session_state.score > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.score
                    
                    st.session_state.page = "gameover"
                    st.rerun()
            
            st.session_state.answered = True
            st.rerun()  # Force refresh to display feedback
    
    # Display feedback
    if st.session_state.answered and st.session_state.feedback:
        if "Correct" in st.session_state.feedback or "Amazing" in st.session_state.feedback or "Difficulty" in st.session_state.feedback:
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
    
    # Show "Next Question" button only after checking the answer
    if st.session_state.answered:
        if st.button("Next Question ➡️", use_container_width=True):
            # Generate new question
            st.session_state.current_question, st.session_state.correct_answer = generate_question(
                st.session_state.max_number,
                st.session_state.operation_type
            )
            st.session_state.answered = False
            st.session_state.user_answer = None
            st.session_state.timer_start = time.time()
            st.session_state.feedback = ""
            st.session_state.input_key += 1  # Increment to reset the input field
            st.rerun()

# Game Over Screen
def show_game_over():
    st.markdown("<h1 class='main-header'>Game Over! 🏆</h1>", unsafe_allow_html=True)
    
    # Display score
    st.markdown(f"<div class='score-display' style='text-align: center;'>Your Score: <span>{st.session_state.score}</span></div>", unsafe_allow_html=True)
    
    # High score display
    if st.session_state.score == st.session_state.high_score and st.session_state.high_score > 0:
        st.success("🎉 New High Score! 🎉")
    
    # Display message based on score
    if st.session_state.score >= 15:
        message = "🌟 Math Wizard Master! 🌟"
    elif st.session_state.score >= 10:
        message = "⭐ Math Wizard Apprentice! ⭐"
    elif st.session_state.score >= 5:
        message = "👍 Math Wizard Novice! 👍"
    else:
        message = "🔍 Keep Practicing! 🔍"
    
    st.markdown(f"<h2 style='text-align: center;'>{message}</h2>", unsafe_allow_html=True)
    
    # Play Again and Main Menu buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again 🔄", use_container_width=True):
            start_new_game()
            st.rerun()
    
    with col2:
        if st.button("Main Menu 🏠", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# Main app logic - display the appropriate screen
if st.session_state.page == "home":
    show_home()
elif st.session_state.page == "tutorial":
    show_tutorial()
elif st.session_state.page == "game":
    show_game()
elif st.session_state.page == "gameover":
    show_game_over()