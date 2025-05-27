
import streamlit as st
import json

@st.cache_data
def load_questions():
    with open("quiz_with_answers.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

if "current" not in st.session_state:
    st.session_state.current = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "wrong" not in st.session_state:
    st.session_state.wrong = 0
if "mode" not in st.session_state:
    st.session_state.mode = "全部题目"
if "wrong_questions" not in st.session_state:
    st.session_state.wrong_questions = []
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

current_set = questions if st.session_state.mode == "全部题目" else st.session_state.wrong_questions
if not current_set:
    st.warning("没有题目可显示")
    st.stop()

q_index = st.session_state.current
q = current_set[q_index]
q_key = f"{q['section']}_{q['section_index']}"

st.title("马原刷题系统（跳转+强锁题号）")
st.subheader(f"{q['section']} 第{q['section_index']}题（总第{q['number']}题）")
st.markdown(q["question"])

option_items = [(k, v) for k, v in q["options"].items()]
default_letter = st.session_state.selected_answers.get(q_key, "A")
default_index = next((i for i, (k, _) in enumerate(option_items) if k == default_letter), 0)

selected = st.radio(
    "请选择一个选项：",
    options=option_items,
    format_func=lambda x: f"{x[0]}. {x[1]}",
    index=default_index,
    key=f"radio_{q_key}"
)
st.session_state.selected_answers[q_key] = selected[0]

if st.button("提交"):
    if not st.session_state.submitted.get(q_key, False):
        st.session_state.submitted[q_key] = True
        correct = q["answer"]
        if selected[0] == correct:
            st.success("回答正确")
            st.session_state.correct += 1
        else:
            st.error("回答错误")
            st.session_state.wrong += 1
            if q not in st.session_state.wrong_questions:
                st.session_state.wrong_questions.append(q)

if st.session_state.submitted.get(q_key, False):
    correct = q["answer"]
    st.info(f"✅ 正确答案：{correct}")
    if selected[0] == correct:
        st.success("回答正确")
    else:
        st.error("回答错误")

col1, col2 = st.columns(2)
with col1:
    if st.button("上一题") and q_index > 0:
        st.session_state.current -= 1
        safe_rerun()
with col2:
    if st.button("下一题") and q_index < len(current_set) - 1:
        st.session_state.current += 1
        safe_rerun()

jump_to = st.number_input("🔎 跳转到题号（总编号）", min_value=1, max_value=len(questions), step=1)
if st.button("跳转"):
    st.session_state.current = jump_to - 1
    safe_rerun()

st.markdown("---")
mode = st.radio("选择模式：", ["全部题目", "错题回顾"], horizontal=True)
if mode != st.session_state.mode:
    st.session_state.mode = mode
    st.session_state.current = 0
    safe_rerun()


st.markdown("---")
st.write(f"📊 当前进度：{st.session_state.current + 1} / {len(current_set)}")
st.write(f"✅ 正确：{st.session_state.correct}  ❌ 错误：{st.session_state.wrong}")
