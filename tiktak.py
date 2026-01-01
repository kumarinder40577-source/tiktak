import streamlit as st

# --- INITIALIZATION ---
# We use session_state to keep the game board in memory across reruns.
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None

# --- GAME LOGIC ---
def check_winner():
    b = st.session_state.board
    # Winning combinations (rows, columns, diagonals)
    wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for x, y, z in wins:
        if b[x] == b[y] == b[z] != "":
            return b[x]
    if "" not in b:
        return "Tie"
    return None

def handle_click(index):
    # Only allow a move if the square is empty and there is no winner yet
    if st.session_state.board[index] == "" and not st.session_state.winner:
        st.session_state.board[index] = st.session_state.current_player
        
        # Check for a win after the move
        winner = check_winner()
        if winner:
            st.session_state.winner = winner
        else:
            # Switch player turn
            st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None

# --- UI LAYOUT ---
st.set_page_config(page_title="Streamlit Tic-Tac-Toe")
st.title("Tic-Tac-Toe")

# Status messaging
if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.warning("The game is a Tie!")
    else:
        st.success(f"Player {st.session_state.winner} Wins!")
else:
    st.info(f"It's Player {st.session_state.current_player}'s turn")

# Create a 3x3 Grid using columns

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        # Create a button for each cell
        button_label = st.session_state.board[index] if st.session_state.board[index] != "" else " "
        cols[col].button(
            button_label, 
            key=f"sq_{index}", 
            on_click=handle_click, 
            args=(index,),
            use_container_width=True
        )

st.write("---")
if st.button("Restart Game"):
    reset_game()
    st.rerun()
