import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
BOARD_SIZE = 15

st.set_page_config(
    page_title="오목 게임",
    page_icon="⚫",
    layout="centered"
)

# -----------------------------
# 게임 초기화
# -----------------------------
def initialize_game():
    st.session_state.board = [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]
    st.session_state.current_player = 1  # 1: 흑, 2: 백
    st.session_state.winner = 0
    st.session_state.game_over = False


if "board" not in st.session_state:
    initialize_game()


# -----------------------------
# 승리 판정
# -----------------------------
def check_winner(row, col, player):
    board = st.session_state.board

    # 가로, 세로, 대각선 2개
    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for dr, dc in directions:
        count = 1

        # 한 방향 확인
        r = row + dr
        c = col + dc

        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r += dr
            c += dc

        # 반대 방향 확인
        r = row - dr
        c = col - dc

        while (
            0 <= r < BOARD_SIZE
            and 0 <= c < BOARD_SIZE
            and board[r][c] == player
        ):
            count += 1
            r -= dr
            c -= dc

        if count >= 5:
            return True

    return False


# -----------------------------
# 돌 놓기
# -----------------------------
def place_stone(row, col):
    if st.session_state.game_over:
        return

    if st.session_state.board[row][col] != 0:
        return

    player = st.session_state.current_player

    st.session_state.board[row][col] = player

    # 승리 확인
    if check_winner(row, col, player):
        st.session_state.winner = player
        st.session_state.game_over = True
        return

    # 무승부 확인
    if all(
        cell != 0
        for row_data in st.session_state.board
        for cell in row_data
    ):
        st.session_state.game_over = True
        st.session_state.winner = 3
        return

    # 플레이어 변경
    st.session_state.current_player = 2 if player == 1 else 1


# -----------------------------
# 제목
# -----------------------------
st.title("⚫ ⚪ 오목 게임")

st.write("15 × 15 바둑판에서 두 명이 번갈아 오목을 둡니다.")

# -----------------------------
# 현재 상태 표시
# -----------------------------
if st.session_state.game_over:

    if st.session_state.winner == 1:
        st.success("🎉 흑돌 승리!")

    elif st.session_state.winner == 2:
        st.success("🎉 백돌 승리!")

    else:
        st.info("🤝 무승부입니다.")

else:

    if st.session_state.current_player == 1:
        st.info("⚫ 흑돌 차례입니다.")
    else:
        st.info("⚪ 백돌 차례입니다.")


# -----------------------------
# 게임판
# -----------------------------
for row in range(BOARD_SIZE):

    columns = st.columns(BOARD_SIZE)

    for col in range(BOARD_SIZE):

        value = st.session_state.board[row][col]

        if value == 0:
            text = "·"
        elif value == 1:
            text = "⚫"
        else:
            text = "⚪"

        with columns[col]:

            if st.button(
                text,
                key=f"cell_{row}_{col}",
                use_container_width=True
            ):
                place_stone(row, col)
                st.rerun()


# -----------------------------
# 다시 시작
# -----------------------------
st.divider()

if st.button("🔄 새 게임 시작", use_container_width=True):
    initialize_game()
    st.rerun()
