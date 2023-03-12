

import random
import typing

import time

def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "t-boner",
        "color": "#4A412A",
        "head": "tiger-king", 
        "tail": "weight",
    }

# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")





# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict, ai_state) -> typing.Dict:

    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }

    
    my_head = game_state["you"]["body"][0]
    my_neck = game_state["you"]["body"][1]

    if my_neck["x"] < my_head["x"]:
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:
        is_move_safe["up"] = False

    
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
      is_move_safe["left"] = False

    if my_head["x"] == board_width-1:
      is_move_safe["right"] = False

    if my_head["y"] == 0:
      is_move_safe["down"] = False

    if my_head["y"] == board_height-1:
      is_move_safe["up"] = False

    
      
    
    my_body = game_state['you']['body']

    for body_pos in my_body:
      if my_head["y"] == body_pos["y"]:
      
        if my_head["x"] == body_pos["x"]+1:
          is_move_safe["left"] = False

        if my_head["x"] == body_pos["x"]-1:
          is_move_safe["right"] = False

      if my_head["x"] == body_pos["x"]:
        if my_head["y"] == body_pos["y"]+1:
          is_move_safe["down"]=False

        if my_head["y"] == body_pos["y"]-1:
          is_move_safe["up"]=False

    
    
    opponents = game_state['board']['snakes']

    headon_tiles = [[0]*(board_width+2) for i in range(board_height+2)]

    for opp in opponents:
      
      for opp_body in opp["body"]:
        if my_head["y"] == opp_body["y"]:
      
          if my_head["x"] == opp_body["x"]+1:
            is_move_safe["left"] = False

          if my_head["x"] == opp_body["x"]-1:
            is_move_safe["right"] = False

        if my_head["x"] == opp_body["x"]:
          if my_head["y"] == opp_body["y"]+1:
            is_move_safe["down"]=False

          if my_head["y"] == opp_body["y"]-1:
            is_move_safe["up"]=False
       
        if len(my_body) > len(opp["body"]):
            break


        # look for head-on collisions, avoid them if we lose them
        opp_head = opp["body"][0]
        if distance(my_head, opp_head) == 2:
            if opp_head["x"] - my_head["x"] == 1:
                is_move_safe["right"] = False

            if opp_head["x"] - my_head["x"] == -1:
                is_move_safe["left"] = False

            if opp_head["y"] - my_head["y"] == 1:
                is_move_safe["up"] = False

            if opp_head["y"] - my_head["y"] == -1:
                is_move_safe["down"] = False

            if (opp_head["x"] == my_head["x"] and abs(opp_head["y"] - my_head["y"]) == 2):
                if (opp_head["y"] > my_head["y"]):
                    is_move_safe["up"] = False
                else:
                    is_move_safe["down"] = False
            if (opp_head["y"] == my_head["y"] and abs(opp_head["x"] - my_head["x"]) == 2):
                if (opp_head["x"] > my_head["x"]):
                    is_move_safe["right"] = False
                else:
                    is_move_safe["left"] = False
       

        
    
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)


    
    food = game_state['board']['food']

    good_food = []

    for f in food:
        safe = True
        my_distance = distance(f, my_head)
        for opp in opponents:
            if distance(opp["body"][0], f) < my_distance:
                safe = False
        if safe:
            good_food.append(f)

    if len(good_food) == 0:
        good_food = food

    sorted_food = sorted(good_food, key=lambda x: (distance(my_head,x)))

    print(sorted_food)

    cf = sorted_food[0]
  
    print("target food is " + str(cf))
  
    next_move = None

    #print(floodfill(get_map(game_state),my_head["x"]+1,my_head["y"], 0, 2, 0))

    scored_moves = {}


    
    for move in safe_moves:
      if move == "left":
        scored_moves[move] = floodfill(get_map(game_state),my_head["x"]-1,my_head["y"], 0, 2, 0)
      elif move == "right":
        scored_moves[move] = floodfill(get_map(game_state),my_head["x"]+1,my_head["y"], 0, 2, 0)
      elif move == "up":
        scored_moves[move] = floodfill(get_map(game_state),my_head["x"],my_head["y"]+1, 0, 2, 0)
      elif move == "down":
        scored_moves[move] = floodfill(get_map(game_state),my_head["x"],my_head["y"]-1, 0, 2, 0)

    

    print(scored_moves)

    print(floodfill(get_map(game_state),my_head["x"]-1,my_head["y"], 0, 2, 0))

    pre_flood = is_move_safe

    all_bad = True

    for move,score in scored_moves.items():
        if score >= 80:
            all_bad = False


    for move,score in scored_moves.items():
        if all_bad:
            break
        if score < 80:
            is_move_safe[move] = False
    
    

    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:

        is_move_safe = pre_flood
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)

    ranked_moves = sorted(scored_moves.items(), key=lambda x: -1*x[1])
    #print(ranked_moves)
    
    #next_move = ranked_moves[0][0]
    
    distance_ranked_moves = []

    for move in safe_moves:
        
        np = my_head

        if move == "left":
            np["x"]-=1
        elif move == "right":
            np["x"]+=1
        elif move == "down":
            np["y"]-=1
        elif move == "up":
            np["y"]+=1

        distance_ranked_moves.append((move, distance(my_head, cf)))
    #print(game_state)
    distance_ranked_moves = sorted(distance_ranked_moves, key=lambda x: x[1])
    
    if len(distance_ranked_moves) == 0:
        next_move = random.choice(safe_moves)
    else:
        next_move = distance_ranked_moves[0][0]

    #if game_state["you"]["health"] >= 80:
    #    next_move = ranked_moves[0][0]

    if next_move == None:
      print("no food path")
      next_move = ranked_moves[0][0]

    print(distance(my_head,cf))

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def get_map(game_state):
  board_width = game_state['board']['width']
  board_height = game_state['board']['height']

  game_map = [ [0]*board_width for i in range(board_height)]

  my_body = game_state["you"]["body"]
  
  for pos in my_body:
    x = pos["x"]
    y = pos["y"]
    game_map[x][y] = 1

  for opp in game_state["board"]["snakes"]:
    for pos in opp["body"]:
      x = pos["x"]
      y = pos["y"]
      game_map[x][y] = 1

  return game_map


def floodfill(game_map, x, y, old, new, size):
    

    if x < 0 or x >= len(game_map):
      return size

    if y < 0 or y >= len(game_map[0]):
      return size

    if game_map[x][y] >= 1:
      return size
  
    if game_map[x][y] == 0:
      game_map[x][y] = 2
      

    size = floodfill(game_map, x+1, y, old, new,size+1)
    size = floodfill(game_map,x-1, y, old, new,size+1)
    size = floodfill(game_map,x, y+1, old, new,size+1)
    size = floodfill(game_map,x, y-1, old, new,size+1)
    return size
  

def distance(pos1, pos2):
  dx = abs(pos1["x"] - pos2["x"])
  dy = abs(pos1["y"] - pos2["y"])

  return (dx + dy)

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })

