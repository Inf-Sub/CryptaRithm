import concurrent.futures
from itertools import permutations
import time


def solve_cryptarithmetic(puzzle_str):
    # Разделяем выражение на левую и правую части
    left_side, right_side = puzzle_str.split('=')
    right_side = right_side.strip()
    
    # Определяем операторы и разделяем выражение на части
    terms = []
    operators = []
    current_term = []
    for char in left_side:
        if char in '+-':
            terms.append(''.join(current_term).strip())
            operators.append(char)
            current_term = []
        else:
            current_term.append(char)
    terms.append(''.join(current_term).strip())
    
    # Извлекаем все уникальные буквы из выражения
    unique_letters = set(''.join(terms) + right_side)
    
    # Убедимся, что количество уникальных букв не превышает 10
    if len(unique_letters) > 10:
        return None
    
    # Преобразуем множество в список для упрощения индексации
    unique_letters = list(unique_letters)
    
    # Перебираем все возможные цифровые подстановки
    for perm in permutations(range(10), len(unique_letters)):
        # Создаем словарь подстановок
        letter_to_digit = dict(zip(unique_letters, perm))
        
        # Проверяем, что первая буква каждого слова не заменяется на ноль
        if any(letter_to_digit[word[0]] == 0 for word in terms + [right_side]):
            continue
        
        # Заменяем буквы на цифры и вычисляем числовые значения
        left_value = int(''.join(str(letter_to_digit[char]) for char in terms[0]))
        for i, operator in enumerate(operators):
            term_value = int(''.join(str(letter_to_digit[char]) for char in terms[i + 1]))
            if operator == '+':
                left_value += term_value
            elif operator == '-':
                left_value -= term_value
        
        right_value = int(''.join(str(letter_to_digit[char]) for char in right_side))
        
        # Проверяем, удовлетворяет ли подстановка уравнению
        if left_value == right_value:
            return {char: digit for char, digit in letter_to_digit.items()}
    
    return None


def solve_and_time(puzzle):
    start_time = time.time()
    solution = solve_cryptarithmetic(puzzle)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return puzzle, solution, elapsed_time


def main(list_puzzles):
    start_time_full = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Запускаем решение всех головоломок в параллельном режиме
        future_to_puzzle = {executor.submit(solve_and_time, puzzle): puzzle for puzzle in list_puzzles}
        
        for future in concurrent.futures.as_completed(future_to_puzzle):
            puzzle, solution, elapsed_time = future.result()
            
            if solution:
                # Разделяем левую часть на слова
                puzzle_left_side, puzzle_right_side = puzzle.split('=')
                puzzle_left_side = puzzle_left_side.strip()
                puzzle_right_side = puzzle_right_side.strip()
                
                # Определяем знак и разделяем левую часть на переменные
                if '+' in puzzle_left_side:
                    variable_left, variable_right = puzzle_left_side.split('+')
                    sign = '+'
                else:
                    variable_left, variable_right = puzzle_left_side.split('-')
                    sign = '-'
                
                # Получаем числовые значения для переменных
                variable_left_value = ''.join(str(solution[char]) for char in variable_left.strip())
                variable_right_value = ''.join(str(solution[char]) for char in variable_right.strip())
                result_value = ''.join(str(solution[char]) for char in puzzle_right_side.strip())
                
                # Выводим результат
                if sign == '+':
                    print(f'{puzzle}: {variable_left_value} + {variable_right_value} = {result_value}')
                else:
                    print(f'{puzzle}: {variable_left_value} - {variable_right_value} = {result_value}')
            else:
                print(f'{puzzle}: No solution found')
            
            print(f'Time taken to solve: {elapsed_time:.2f} seconds\n')
    
    end_time_full = time.time()
    elapsed_time_full = end_time_full - start_time_full
    print(f'Time required to solve all tasks: {elapsed_time_full:.2f} seconds\n')


if __name__ == '__main__':
    puzzles = [
        'НИТКА+НИТКА=ТКАНЬ',
        'ДЕТАЛЬ+ДЕТАЛЬ=ИЗДЕЛИЕ',
        'ИЗДЕЛИЕ-ДЕТАЛЬ=ДЕТАЛЬ',
        'ВАГОН+ВАГОН=СОСТАВ',
        'ЛЮБА+ЛЮБИТ=АРБУЗЫ',
        'АРБУЗЫ-ЛЮБИТ=ЛЮБА',
        'АРБУЗЫ-ЛЮБА=ЛЮБИТ',
        'ОДИН+ОДИН=МНОГО',
        'МНОГО-ОДИН=ОДИН',
        'СИНИЦА+СИНИЦА=ПТИЧКИ'
    ]
    
    main(puzzles)

