import random

good_moves = []

for i in range(9):
    suggested_move = random.choice([j for j in range(1, 9)])
    while bool(input(f"Is {suggested_move} a good move (True/False)? ")) is False and suggested_move in good_moves:
        suggested_move = random.choice([j for j in range(1, 9)])
    good_moves.append(suggested_move)
    user_move = int(input("Your move: "))
    while user_move in good_moves:
        user_move = int(input(f"Your move ({user_move} is not available): "))
    good_moves.append(user_move)

print(good_moves)
