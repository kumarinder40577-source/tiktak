import streamlit as st

# Initialize the game state
if 'board' not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.winner = None
    st.session_state.current_player = "X"

def check_winner():
    b = st.session_state.board
    # Winning combinations
    win_indices = [
        (0,1,2), (3,4,5), (6,7,8), # Rows
        (0,3,6), (1,4,7), (2,5,8), # Cols
        (0,4,8), (2,4,6)           # Diagonals
    ]
    for i, j, k in win_indices:
        if b[i] == b[j] == b[k] != "":
            return b[i]
    if "" not in b:
        return "Tie"
    return None

def handle_click(i):
    if st.session_state.board[i] == "" and not st.session_state.winner:
        st.session_state.board[i] = st.session_state.current_player
        st.session_state.winner = check_winner()
        # Switch player
        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.winner = None
    st.session_state.current_player = "X"

# UI Layout
st.title("Tic-Tac-Toe for Streamlit")

if st.session_state.winner:
    if st.session_state.winner == "Tie":
        st.success("It's a Tie!")
    else:
        st.success(f"Player {st.session_state.winner} Wins!")
else:
    st.write(f"Current Turn: **{st.session_state.current_player}**")

# Create a 3x3 grid using Streamlit columns
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        index = row * 3 + col
        button_label = st.session_state.board[index] if st.session_state.board[index] != "" else " "
        cols[col].button(
            button_label, 
            key=f"btn_{index}", 
            on_click=handle_click, 
            args=(index,),
            use_container_width=True
        )

st.divider()
if st.button("Reset Game"):
    reset_game()
    st.rerun()
