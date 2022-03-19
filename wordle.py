import random
import re
from words import get_all_words, get_common_words


MAX_NUM_OF_GUSSES = 6
WORD_LIST, SOLUTION_LIST = get_all_words(), get_common_words()
WORD_LEN = 5


def get_evaluation(answer, word):
    """
    :return: string in the len of the word with 0, 1, and 2 as item when 
    0 - letter is grey
    1 - letter is yellow
    2 - letter is green
    """
    output = ["0"] * len(answer)
    
    # check for correct letter and placement
    for i in range(len(answer)):
        if word[i] == answer[i]:
            output[i] = "2"
            answer = answer[:i] + ' ' + answer[i + 1:]
           
    # check for correct letter
    for i in range(len(answer)):
        char = word[i]
        if char in answer and output[i] == "0":
            output[i] = "1"
            first_occurence = answer.find(char)
            answer = answer[:first_occurence] + ' ' + answer[first_occurence + 1:]
    return "".join(output)


def get_evaluation2words_map(word, possible_solutions):
    """
    :type1: Str
    :type2: List
    :return: a dictionary where each key is list representing a possible evaluation
             and the values are a list of all the solutions that will return that evaluation 
    """
    eval2words = dict()
    for possible_solution in possible_solutions:
        evaluation = get_evaluation(possible_solution, word)
        if evaluation not in eval2words:
            eval2words[evaluation] = []
        eval2words[evaluation].append(possible_solution)
    return eval2words


def find_worst_evaluation_number(eval2words):
    """
    :param: dictionary of a given word where the key is possible evalution
             and the values are a list of the remaining possible solutions given that evaluation.
    :param type: Dict[Str:List[Str]]
    :retrun: the number of the evaluation that left the most possible solutions remaining
    """
    worst_evaluation_number = None
    for evaluation, remaining_solution in eval2words.items():
        # initiat the worst solution
        if not worst_evaluation_number:
            worst_evaluation_number = len(remaining_solution)
        worst_evaluation = max(worst_evaluation_number, len(remaining_solution))
    return worst_evaluation


def sort_possible_solutions(possible_solutions, word_list, n=10):
    """
    sort the guesses from the guess that in worse case scenario will remove the most options (lowest number)
    to the guess that will remove the least (biggest number)
    """
    return sorted(word_list, key=lambda word: find_worst_evaluation_number(get_evaluation2words_map(word, possible_solutions)))[:n]


def is_valid_guess(word, word_list=WORD_LIST, word_len=WORD_LEN):
    pattern = f"[a-zA-Z]{{{5}}}"
    return bool(re.search(pattern, word)) and (len(word) == word_len) and (word.lower() in word_list)


def advice(word_list=WORD_LIST, solution_list=SOLUTION_LIST, max_num_of_guesses=MAX_NUM_OF_GUSSES, number_of_advices=10):
    remaining_solutions = solution_list
    for _ in range(max_num_of_guesses - 1):
        advices = sort_possible_solutions(remaining_solutions, word_list, n=number_of_advices)
        print(f"algorithem recommand to choose from this words: {','.join(advices)}")
        guess = input("enter your chosen guess: ")
        while not is_valid_guess(guess, word_list):
            print("guess is invalid")
            guess = input("enter your chosen guess: ")
        evaluation = input("enter the given evaluation: ")
        remaining_solutions = get_evaluation2words_map(guess, remaining_solutions).get(evaluation)
        while not remaining_solutions:
            import ipdb
            ipdb.set_trace()
            print("no remaining solutions left... try again:")
            evaluation = input("enter the given evaluation: ")
            remaining_solutions = get_evaluation2words_map(guess, remaining_solutions).get(evaluation)
        print(f"there are {len(remaining_solutions)}")
        if len(remaining_solutions) == 1:
            solution = remaining_solutions[0]
            print(f"the answer is {solution}")
            return

if __name__ == '__main__':
    advice()