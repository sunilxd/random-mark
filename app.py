import streamlit as st
import pandas as pd

from random import random, randint

def weighted_random(min_val, max_val):
    if min_val > max_val:
        raise ValueError("min_val must not be greater than max_val")

    raw_random = random()
    
    # Apply a custom weight function to emphasize the middle values
    # Using a quadratic weight: f(x) = 4x(1 - x), where x ∈ [0, 1]
    weight = 4 * raw_random * (1 - raw_random)
    
    return int(min_val + (max_val - min_val) * weight)

def random_partition(value : int, parts: list[int]):
    # value: 17
    # parts: [2, 2, 2, 2, 2, 10]

    n = len(parts)
    ans = [0]*n
    total = sum(parts)
    index_array = list(range(n))

    index_array.sort(key= lambda x: parts[x])

    for index in index_array:
        total -= parts[index]
        min_val = max(0, value-total)
        max_val = min(parts[index], value)

        
        ans[index] = weighted_random(min_val, max_val)
        # print(total, value, min_val, max_val, ans[index])

        value -= ans[index]

    ans.append(sum(ans))

    return ans

def question(mark, option, header=False):
    if header:
        return [f"{mark}({i+1})" for i in range(option)] if option != 1 else [f"{mark}"]
    else:
        j = randint(0, option-1)
        return [mark if j == i else 0 for i in range(option)]
    
def section(mark, count, option, header=False):
    return [item for _ in range(count) for item in question(mark, option, header)]

def paper(q_values, header=False):

    sol = [item for q in q_values for item in section(q[0], q[1], q[2], header)]

    if header:
        return [f"{item}.{i+1}" for i, item in enumerate(sol)]
    else:
        return sol

st.title("Random Mark Substituter")
st.subheader("Question")

n = st.number_input("Question Type", step=1, min_value=1)
total_mark = 0
question_values = []

for i in range(n):
    value = [0]*3
    left, middle, right = st.columns(3)

    value[0] = left.number_input("Mark", step=1, min_value=1, key=f"left-{i}")
    value[1] = middle.number_input("No. of question", step=1, min_value=1, key=f"middle-{i}")
    value[2] = right.number_input("Choice", step=1, min_value=1, key=f"right-{i}")

    total_mark += value[0]*value[1]
    question_values.append(value)

f"Total Mark: {total_mark}"

st.subheader("Mark")

pasted_text = st.text_area(label='Paste the values here')

if pasted_text or st.button('Generate'):
    marks = [int(line.strip()) for line in pasted_text.splitlines() if line.strip()]
    st.write(f"Count: {len(marks)}")

    master_sheet = [random_partition(mark, paper(question_values)) for mark in marks]
    df = pd.DataFrame(master_sheet, columns=paper(question_values, header=True)+['Sum'])
    df = df.replace(0, '')
    st.dataframe(df)