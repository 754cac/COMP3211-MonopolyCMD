from game import Game
import vars

game = Game()
load_game = vars.handle_question_with_options('New Game [0] or Load Save File [1] ? ',  ['0', '1'])
if load_game == '0':
    game_initialized = game.new_game()
else:
    save_file_name = vars.handle_question_with_function('Enter save file name: ', vars.is_valid_save_file_name)
    game_initialized = game.load_game_state(save_file_name)

if game_initialized:
    game.play()

