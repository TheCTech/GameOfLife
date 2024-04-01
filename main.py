# Importing required libraries
import time, pygame, random

# SETTINGS, you can modify them before starting the program
X, Y = 100, 100 # Width and height, don't set it to 0 or negative
tick_time = 0.25 # Game tick time for automatic simulation, don't set it to 0 or negative, will round to 2 decimals
SCALE = 10 # Scale of every tile in pixels
mode = "editor" # Default mode
automatic_simulation = False # Should the simulation automatically tick from start?
paused = False # Run the game paused?
grid_background = True # Self explanatory

# You can modify it, but why???
LIFE = "L" # U won't even see it
map = [] # It will be cleared before start anyway
go_to_loop_start = False # Just press "M", will do the same and won't conflict with default mode

# Do not touch
running = True # Disable the program, yey
tick = 0 # Someone is cooking a false report?
m_click = False # If it will run with mouse outside the game screen, code will crash
last_tick = -1 # It's needed for getting start time for automatic simulation, don't break it pls

# Set up display
screen = pygame.display.set_mode((X*SCALE, Y*SCALE)) # Every one tile in game is SCALExSCALE pixels

# Round the tick_time
tick_time = round(tick_time, 2)

# Functions
def generate_map(x_len: int,y_len: int, randomize_map = False, random_chance = 5):
    generated_map = []
    for y in range(y_len):
        generated_map.append([])
        for x in range(x_len):
            if random.randint(0,random_chance) == 0 and randomize_map:
                generated_map[y].append(LIFE)
            else:
                generated_map[y].append(" ")
    return(generated_map)

# Draw from map to screen
def draw():
    # If gamemode = editor than change bc to dark green
    # If paused, change to redish
    if paused:
        bc_color = (32,0,0)
        bc_second_color = (38,12,12)
    elif mode == "editor":
        bc_color = (0,32,0)
        bc_second_color = (8,40,8)
    else:
        bc_color = (0,0,0)
        bc_second_color = (24,24,24)

    screen.fill(bc_color)

    for y in range(Y):
        for x in range(X):
            if map[y][x] == LIFE:
                pygame.draw.rect(screen, (255,255,255), (x*SCALE,y*SCALE,SCALE,SCALE)) # Every one tile in game is SCALExSCALE pixels
            else:
                # Create a grid in background
                if (x+y)%2 == 0 and grid_background:
                    pygame.draw.rect(screen, bc_second_color, (x*SCALE,y*SCALE,SCALE,SCALE))

def get_neighbors(origin_x,origin_y):
    neighbors = 0
    positions = [[origin_x-1,origin_y-1], [origin_x,origin_y-1], [origin_x+1,origin_y-1],
                 [origin_x-1,origin_y],                          [origin_x+1,origin_y],
                 [origin_x-1,origin_y+1], [origin_x,origin_y+1], [origin_x+1,origin_y+1]]
    for x, y in positions:
            if x >= 0 and x <= X-1 and y >= 0 and y <= Y-1:
                if map[y][x] == LIFE:
                    neighbors += 1
    
    return(neighbors)

def copy_list(parent_list):
    child_list = []
    for row in parent_list:
        child_list.append(row.copy())

    return(child_list)

# LAWS: 
#     1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
#     2. Any live cell with two or three live neighbors lives on to the next generation.
#     3. Any live cell with more than three live neighbors dies, as if by overpopulation.
#     4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
#
#     (https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
                
def game_tick():
    global map
    new_map = copy_list(map)
    for y in range(Y):
        for x in range(X):
            neighbors = get_neighbors(x, y)
            
            if map[y][x] == LIFE:

                # LAW 1
                if neighbors < 2: # Underpopulation ==> DIES
                    new_map[y][x] = " "

                # LAW 3
                elif neighbors > 3: # Overpopulation ==> DIES
                    new_map[y][x] = " "
                
                # If if's for LAW 1 and LAW 3 return false than it means it LIVES (LAW 2)
                    
            else: # Tile is DEAD

                # LAW 4
                if neighbors == 3: # Reproduction
                    new_map[y][x] = LIFE



    map = new_map

# Generate map
map = generate_map(X, Y)

# First draw on screen
pygame.display.flip()
draw()

# Main loop
while running:

    if last_tick < tick:
        start_time = time.time()
        last_tick = tick

    # Change window title
        
    # Change True to ON and False to OFF for automatic simulation label
    automatic_simulation_label = "ON" if automatic_simulation else "OFF"

    # Add space before paused for easier inserting into strings
    paused_label = " paused" if paused else ""

    if mode == "editor":
        # If tick = 0, than it means that there where changes
        if tick == 0:
            pygame.display.set_caption(f"Game Of Life |editor{paused_label}|")
        else:
            pygame.display.set_caption(f"Game Of Life |editor{paused_label} TICK:{tick}|")

    elif mode == "simulation":
        pygame.display.set_caption(f"Game Of Life |simulation{paused_label} TICK:{tick} auto:{automatic_simulation_label}|")



    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Quit
        
        # Run this only when not paused
        elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                # Get click position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                m_click = True
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False # Quit

            # Change gamemode
            elif event.key == pygame.K_m:
                if mode == "simulation":
                    mode = "editor"

                else:
                    mode = "simulation"

                print(f"Gamemode {mode}")
                go_to_loop_start = True
            
            # Change automatic simulation mode
            elif event.key == pygame.K_a:
                automatic_simulation = not automatic_simulation

                print(f"Automatic simulation: {automatic_simulation}")
                go_to_loop_start = True
            
            # Pause or unpause
            elif event.key == pygame.K_p:
                paused = not paused

                print(f"paused or unpaused (paused:{paused})")
                go_to_loop_start = True
            
            # Randomize map (in editor)
            elif event.key == pygame.K_r:
                if mode == "editor":
                    map = generate_map(X, Y, True)
                    tick = -1
            
            # Clear map (in editor)
            elif event.key == pygame.K_c:
                if mode == "editor":
                    map = generate_map(X, Y)
                    tick = -1
            
            # Disable and enable grid in the background
            elif event.key == pygame.K_b:
                    grid_background = not grid_background
            
            # Change the speed of automatic simulation
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                change_value = 0.1 if event.key == pygame.K_UP else -0.1
                last_tick_time = tick_time
                tick_time = round(tick_time + change_value, 2)
                if tick_time <= 0:
                    print("nuh uh")
                    tick_time = last_tick_time
                print(tick_time)
                go_to_loop_start = True

      
    if go_to_loop_start:
        go_to_loop_start = False
        start_time = time.time()
        continue # If changed mode, go to start of this loop


    if not paused:
        # Simulation game tick
        if mode == "simulation":
            now = time.time()
            if m_click or (automatic_simulation and (start_time + tick_time) < now):
                m_click = False
                game_tick()   
                tick += 1
        
        elif mode == "editor":
            # Editor event handling is done with every other event
            if m_click:
                tick = -1
                # Change the tile (divide the positions by SCALE because the tile is SCALExSCALE pixels)
                mouse_x, mouse_y = int(mouse_x/SCALE), int(mouse_y/SCALE)

                if map[mouse_y][mouse_x] == LIFE:
                    map[mouse_y][mouse_x] = " "
                else:
                    map[mouse_y][mouse_x] = LIFE

                m_click = False


    # Draw on screen
    pygame.display.flip()
    draw()

    # On screen edit, clear or randomization
    if tick == -1:
        last_tick = -1
        tick = 0
        continue

# If loop quits (QUIT event from pygame) quit pygame engine
pygame.quit()