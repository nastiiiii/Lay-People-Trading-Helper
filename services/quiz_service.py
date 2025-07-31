import json

with open("utils/quiz_questions.json", "r") as f:
    quiz_data = json.load(f)

def get_categories():
    return list(quiz_data.keys())

def get_questions_by_category(category: str):
    return quiz_data.get(category, [])

def evaluate_answers(category: str, answers: dict):
    questions = quiz_data.get(category, [])
    total = len(questions)
    correct = 0
    feedback = []

    for idx, question in enumerate(questions):
        user_answer = answers.get(str(idx))
        correct_answer = question.get("answer") or question.get("correct_answer")
        is_correct = user_answer == correct_answer
        if is_correct:
            correct += 1
        feedback.append({
            "question": question["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "explanation": question["explanation"]
        })

    return {"total": total, "correct": correct, "feedback": feedback}

def evaluate_answers_from_submission(submission):
    questions = quiz_data.get(submission.category, [])
    total = len(questions)
    correct = 0

    for answer in submission.answers:
        matching_question = next((q for q in questions if q["question"] == answer.question), None)
        if not matching_question:
            continue

        options = matching_question.get("options") or matching_question.get("choices")
        correct_answer = matching_question.get("answer") or matching_question.get("correct_answer")

        options = [opt.strip().lower() for opt in options]
        correct_answer = correct_answer.strip().lower()

        try:
            correct_index = options.index(correct_answer)
        except ValueError:
            continue  # correct answer not found in options list

        if answer.selected_index == correct_index:
            correct += 1

    return {
        "total_questions": total,
        "correct_answers": correct,
        "category": submission.category
    }
