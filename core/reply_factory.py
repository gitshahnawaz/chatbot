
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    if current_question_id is None or current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return False, "Invalid question ID"
    current_question = PYTHON_QUESTION_LIST[current_question_id]
    if correct_answer not in current_question['options']:
        return False, "Invalid correct answer"
    session_key = f"question_{current_question_id}_correct_answer"
    session[session_key] = correct_answer
    session.save()
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None or current_question_id < 0 or current_question_id >= len(PYTHON_QUESTION_LIST):
        return None, -1

    next_question_id = current_question_id + 1

    if next_question_id < len(PYTHON_QUESTION_LIST):
        next_question = PYTHON_QUESTION_LIST[next_question_id]['question']
        return next_question, next_question_id
    else:
        return None, -1

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    correct_answers = 0

    for question_id, question_data in enumerate(PYTHON_QUESTION_LIST):
        session_key = f"question_{question_id}_correct_answer"
        user_answer = session.get(session_key)

        if user_answer is not None and user_answer == question_data['correct_answer']:
            correct_answers += 1
    score = (correct_answers / total_questions) * 100

    result_message = f"Congratulations! You answered {correct_answers} out of {total_questions} questions correctly. Your score is {score:.2f}%."


    return result_message
