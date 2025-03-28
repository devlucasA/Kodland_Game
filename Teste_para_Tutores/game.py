import random
import pgzrun
from pygame import Rect
import math

"""
    ATAQUE ou ESQUIVA:
    DASH + Tecla de movimento

"""

MAP_WIDTH = 43
MAP_HEIGHT = 30
ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 8
MAX_ROOMS = 25
TILE_SIZE = 20  
GRAVITY = 0.5

WIDTH = MAP_WIDTH * TILE_SIZE
HEIGHT = MAP_HEIGHT * TILE_SIZE
music_on = True  
sound_fx_on = True  

def toggle_menu_music():
    global music_on  
    if music_on:
        sounds.menu_music.stop()  
        sounds.menu_music.play(loops=-1)  
    else:
        sounds.menu_music.stop()

def toggle_game_music():
    global music_on
    if music_on:
        sounds.game_music.stop()
        sounds.game_music.play(loops=-1)
    else:
        sounds.game_music.stop()

def play_shoot_sound():
    global sound_fx_on 
    if sound_fx_on:
        sounds.shoot.play()

def play_victory():
    global sound_fx_on 
    if sound_fx_on:
        sounds.victory.play()

def play_explosion():
    global sound_fx_on 
    if sound_fx_on:
        sounds.explosion.play()

def play_dash():
    global sound_fx_on 
    if sound_fx_on:
        sounds.dash.play()


def toggle_sound_fx():
    global sound_fx_on  
    sound_fx_on = not sound_fx_on  
    pass

toggle_menu_music()
game_state = "menu" 

start_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 60))
music_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 60))
sound_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 90), (200, 60))
exit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 160), (200, 60))

def create_empty_map():
    return [['#' for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

def create_room(x, y, w, h, game_map):
    for i in range(y, y + h):
        for j in range(x, x + w):
            game_map[i][j] = '.'

def connect_rooms(x1, y1, x2, y2, game_map):
    def clamp(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    x1, y1 = clamp(x1, 0, MAP_WIDTH - 1), clamp(y1, 0, MAP_HEIGHT - 1)
    x2, y2 = clamp(x2, 0, MAP_WIDTH - 1), clamp(y2, 0, MAP_HEIGHT - 1)
    
    if random.random() < 0.5:
        h_x, h_y = x1, y2
    else:
        h_x, h_y = x2, y1

    h_x, h_y = clamp(h_x, 0, MAP_WIDTH - 1), clamp(h_y, 0, MAP_HEIGHT - 1)
    
    for x in range(min(x1, h_x), max(x1, h_x) + 1):
        game_map[y1][x] = '.'
    for y in range(min(y1, h_y), max(y1, h_y) + 1):
        game_map[y][h_x] = '.'
    for x in range(min(h_x, x2), max(h_x, x2) + 1):
        game_map[y2][x] = '.'


def generate_dungeon():
    game_map = create_empty_map()
    rooms = []
    
    for _ in range(MAX_ROOMS):
        w = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = random.randint(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = random.randint(1, MAP_WIDTH - w - 1)
        y = random.randint(1, MAP_HEIGHT - h - 1)
        
        new_room = (x, y, w, h)
        create_room(x, y, w, h, game_map)
        
        if rooms:
            prev_x, prev_y, _, _ = rooms[-1]
            connect_rooms(prev_x + w // 2, prev_y + h // 2, x + w // 2, y + h // 2, game_map)
        
        rooms.append(new_room)
    
    return game_map, rooms[0], rooms  

dungeon, start_room, all_rooms = generate_dungeon()


player_sprites = ["astro1", "astro2", "astro3"]
player_sprites_right = ["astro1d", "astro2d", "astro3d"]  
player_sprites_diag_up_right = ["astro1ds", "astro2ds", "astro3ds"] 
player_sprites_left = ["astro1e", "astro2e", "astro3e"] 
player_sprites_diag_up_left = ["astro1es", "astro2es", "astro3es"]
player_sprites_diag_down_right = ["astro1db", "astro2db", "astro3db"]  
player_sprites_diag_down_left = ["astro1eb", "astro2eb", "astro3eb"]  
player_sprites_up = ["astro1c", "astro2c", "astro3c"]  
player_sprites_down = ["astro1b", "astro2b", "astro3b"]  
dash_sprites = ["voa1", "voa2", "voa3"]
player_sprite = Actor(player_sprites[0]) 

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.dash_speed = 6
        self.is_dashing = False
        self.dash_timer = 0
        self.invincibility_timer = 180  
        self.sprite_index = 0  
        self.sprite_delay = 10  
        self.sprite_timer = 0 
        self.is_moving = False  
        self.direction = (0, 0)  
        self.dash_cooldown = 3 
        self.dash_cooldown_timer = 0
        self.gravity_timer = 0

    def move(self, dx, dy):
        if self.is_dashing:
            speed = self.dash_speed
        else:
            speed = self.speed
        
        new_x = self.x + dx * speed
        if dungeon[int(self.y // TILE_SIZE)][int(new_x // TILE_SIZE)] != '#':  
            self.x = new_x  

        new_y = self.y + dy * speed

        if self.gravity_timer > 0:
            new_y -= GRAVITY  
            self.gravity_timer -= 1  
        else:
            new_y += GRAVITY  

        if dungeon[int(new_y // TILE_SIZE)][int(self.x // TILE_SIZE)] != '#':
            self.y = new_y
            if new_y < self.y:  
                return  

        below_y = self.y + GRAVITY
        if dungeon[int(below_y // TILE_SIZE)][int(self.x // TILE_SIZE)] == '#':
            self.gravity_timer = 100  # Ati
        self.is_moving = (dx != 0 or dy != 0)
        self.direction = (dx, dy)



    def dash(self): 
        if not self.is_dashing and self.invincibility_timer <= 0:
                if not self.is_dashing and self.dash_cooldown_timer <= 0 and self.is_moving: 
                    self.is_dashing = True
                    self.dash_timer = 3 
                    self.dash_cooldown_timer = self.dash_cooldown

    def update(self):

        if self.is_dashing:
            self.dash_timer -= 0.1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = 50 

        self.check_dash_attack()

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1

        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        self.update_sprite()
        

    def update_sprite(self):
        self.sprite_timer += 1
        if self.sprite_timer >= self.sprite_delay:
            self.sprite_timer = 0
            
            if self.is_dashing:
                play_dash()
                self.sprite_index = (self.sprite_index + 1) % len(dash_sprites)
                player_sprite.image = dash_sprites[self.sprite_index]
            elif self.is_moving:
                if self.direction[0] > 0 and self.direction[1] < 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_diag_up_right)
                    player_sprite.image = player_sprites_diag_up_right[self.sprite_index]
                elif self.direction[0] < 0 and self.direction[1] < 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_diag_up_left)
                    player_sprite.image = player_sprites_diag_up_left[self.sprite_index]
                elif self.direction[0] > 0 and self.direction[1] > 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_diag_down_right)
                    player_sprite.image = player_sprites_diag_down_right[self.sprite_index]
                elif self.direction[0] < 0 and self.direction[1] > 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_diag_down_left)
                    player_sprite.image = player_sprites_diag_down_left[self.sprite_index]
                elif self.direction[0] > 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_right)
                    player_sprite.image = player_sprites_right[self.sprite_index]
                elif self.direction[0] < 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_left)
                    player_sprite.image = player_sprites_left[self.sprite_index]
                elif self.direction[1] < 0:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_up)
                    player_sprite.image = player_sprites_up[self.sprite_index]

                else: 
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites_down)
                    player_sprite.image = player_sprites_down[self.sprite_index]
            else:
                    self.sprite_index = (self.sprite_index + 1) % len(player_sprites)
                    player_sprite.image = player_sprites[self.sprite_index]

    def check_dash_attack(self):
        global enemies

        if not self.is_dashing:
            return
        for enemy in enemies:
            distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
            if distance < TILE_SIZE * 2 and not enemy.is_dead: 
                enemy.kill_enemy()  


    def draw(self):
        player_sprite.pos = (self.x, self.y)
        player_sprite.draw()

enemy_sprites_moving = ["et1", "et2"]  
enemy_sprites_death_animation_frames = ["et1m", "et2m", "et3m"]
enemy_sprite_shooting = "et3"  

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0.4
        self.shoot_timer = random.randint(80, 160)
        self.is_shooting = False  
        self.is_dead = False
        self.death_timer = 0
        self.current_frame = 0
        self.sprite_index = 0
        self.sprite_timer = 0
        self.sprite_delay = 10  
        self.sprite = enemy_sprites_moving[0]  

    def move(self):
        if random.random() < 0.5:
            if self.x < player.x:
                new_x = self.x + self.speed
                if not self.check_collision_with_others(new_x, self.y):
                    self.x = new_x
            elif self.x > player.x:
                new_x = self.x - self.speed
                if not self.check_collision_with_others(new_x, self.y):
                    self.x = new_x
        else:
            if self.y < player.y:
                new_y = self.y + self.speed
                if not self.check_collision_with_others(self.x, new_y):
                    self.y = new_y
            elif self.y > player.y:
                new_y = self.y - self.speed
                if not self.check_collision_with_others(self.x, new_y):
                    self.y = new_y

    def kill_enemy(self):
        play_explosion()
        if not self.is_dead: 
            self.is_dead = True
            self.death_timer = 90
            self.current_frame = 0
 
    def update_enemy_sprite(self):
        
        self.sprite_timer += 1
        
        if self.is_dead:
            play_explosion()
            self.death_timer += 1
            if self.death_timer % self.sprite_delay == 0:
                
                self.current_frame += 1
                if self.current_frame < len(enemy_sprites_death_animation_frames):
                    self.sprite = enemy_sprites_death_animation_frames[self.current_frame]
                else:
                    if self in enemies:
                        enemies.remove(self)
            return  

        if self.sprite_timer >= self.sprite_delay:
            self.sprite_timer = 0
            if self.is_shooting:
                self.sprite = enemy_sprite_shooting
            else:
                self.sprite_index = (self.sprite_index + 1) % len(enemy_sprites_moving)
                self.sprite = enemy_sprites_moving[self.sprite_index]


    def check_collision_with_others(self, new_x, new_y):
        for other in enemies:
            if other != self:  
                dist = math.sqrt((new_x - other.x) ** 4 + (new_y - other.y) ** 4)
                if dist < TILE_SIZE:  
                    return True
        return False

    def shoot(self):
        if self.shoot_timer <= 0:
            bullets.append(Bullet(self.x, self.y, player.x, player.y))
            self.shoot_timer = random.randint(80, 400) 
            self.is_shooting = True  
        else:
            self.shoot_timer -= 1
            if self.shoot_timer < 50: 
                self.is_shooting = False 

    def update(self):

        self.move()
        self.shoot()
        self.update_enemy_sprite()


    if game_state == "victory":
        if keyboard.ESCAPE:
            game_state = "menu"
        
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        play_shoot_sound()
        self.x = x
        self.y = y
        angle = math.atan2(target_y - y, target_x - x)
        self.dx = math.cos(angle) * 5
        self.dy = math.sin(angle) * 5

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.is_outside_map():
            bullets.remove(self)

    def is_outside_map(self):
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        if tile_x < 0 or tile_x >= len(dungeon[0]) or tile_y < 0 or tile_y >= len(dungeon):
            return True  # Fora do mapa
        if dungeon[tile_y][tile_x] == '#':
            return True  
        
        return False

    def draw(self):
        screen.draw.filled_circle((self.x, self.y), 5, "cyan")

sounds.shoot.stop()

player = Player(start_room[0] * TILE_SIZE + TILE_SIZE // 2, start_room[1] * TILE_SIZE + TILE_SIZE // 2)
NUM_ENEMIES = 6
random_rooms = random.sample(all_rooms[1:], NUM_ENEMIES)  
enemies = [Enemy(room[0] * TILE_SIZE + TILE_SIZE // 2, room[1] * TILE_SIZE + TILE_SIZE // 2) for room in random_rooms]
bullets = []
game_over = False

def check_collision_with_enemies():
    if player.is_dashing or player.invincibility_timer > 0:
        return False  

    for enemy in enemies:
        dist = math.sqrt((player.x - enemy.x) ** 2 + (player.y - enemy.y) ** 2)
        if dist < TILE_SIZE:
            return True
    return False

def check_collision_with_bullets():
    if player.invincibility_timer > 0:
        return False  
    for bullet in bullets:
        dist = math.sqrt((player.x - bullet.x) ** 2 + (player.y - bullet.y) ** 2)
        if dist < TILE_SIZE // 2:
            return True
    return False

def reset_game():
    global player, enemies, bullets, dungeon, start_room, all_rooms, game_over
    dungeon, start_room, all_rooms = generate_dungeon()
    player = Player(start_room[0] * TILE_SIZE + TILE_SIZE // 2, start_room[1] * TILE_SIZE + TILE_SIZE // 2)
    random_rooms = random.sample(all_rooms[1:], NUM_ENEMIES)
    enemies = [Enemy(room[0] * TILE_SIZE + TILE_SIZE // 2, room[1] * TILE_SIZE + TILE_SIZE // 2) for room in random_rooms]
    bullets.clear()
    game_over = False

victory_timer = None  

def check_victory():
    global game_state, victory_timer

    if len(enemies) == 0 and game_state == "playing":
        if victory_timer is None:  
            victory_timer = 170  
        elif victory_timer > 0:  
            victory_timer -= 1
        else:  
            game_state = "victory"
            victory_timer = None  
    else:
        victory_timer = None  

def on_mouse_down(pos):
    global game_state, music_on, sound_fx_on

    if game_state == "menu":
        if start_button.collidepoint(pos):
            reset_game()
            sounds.menu_music.stop()
            toggle_game_music()
            game_state = "playing"
        elif music_button.collidepoint(pos):  
            music_on = not music_on
            toggle_menu_music()
        elif sound_button.collidepoint(pos):  
            toggle_sound_fx()
        elif exit_button.collidepoint(pos):
            exit()

player = Player(100, 100)

def update():
    global game_state, game_over, sound_on  

    if game_state == "playing":
        
        for enemy in enemies:
            enemy.move()
            enemy.shoot()
            enemy.update_enemy_sprite()
       
        check_victory()
    
    if game_state == "victory":
        play_victory()
        sounds.game_music.stop()
        if keyboard.ESCAPE:
            sounds.victory.stop()
            sounds.game_music.stop()
            toggle_menu_music()
            game_state = "menu"
            
            
    if game_state == "menu":
        sounds.victory.stop()
        return  

    if game_state == "game_over":
        sounds.game_music.stop()
        if keyboard.RETURN : 
            reset_game()
            toggle_game_music()
            game_state = "playing"  
        elif keyboard.ESCAPE: 
            sounds.game_music.stop()
            toggle_menu_music()
            game_state = "menu" 
             
        return

    dx, dy = 0, 0
    if keyboard.left or keyboard.a:
        dx = -1
    if keyboard.right or keyboard.d:
        dx = 1
    if keyboard.up or keyboard.w:
        dy = -1
    if keyboard.down or keyboard.s:
        dy = 1

    player.move(dx, dy)
    player.update()

    if keyboard.space:
        player.dash()

    for enemy in enemies:
        enemy.update()
    for bullet in bullets:
        bullet.update()

    if check_collision_with_enemies() or check_collision_with_bullets():
        game_state = "game_over"  

def draw():
    screen.clear()
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "game_over":
        draw_game_over()
    elif game_state == "victory":
        draw_victory_screen()


def draw_menu():
    screen.clear()
    screen.draw.text("O ASTRONAUTA", center=(WIDTH // 2, HEIGHT // 4), fontsize=80, color="white")

    screen.draw.filled_rect(start_button, "white")
    screen.draw.text("Começar o Jogo", center=start_button.center, fontsize=30, color="black")

    screen.draw.filled_rect(music_button, "white")
    music_text = "Música: ON" if music_on else "Música: OFF"
    screen.draw.text(music_text, center=music_button.center, fontsize=30, color="black")

    screen.draw.filled_rect(sound_button, "white")
    sound_text = "Som: ON" if sound_fx_on else "Som: OFF"
    screen.draw.text(sound_text, center=sound_button.center, fontsize=30, color="black")

    screen.draw.filled_rect(exit_button, "white")
    screen.draw.text("Sair", center=exit_button.center, fontsize=30, color="black")

def draw_game():
    screen.clear()
    
    

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if dungeon[y][x] == '#':
                screen.draw.filled_rect(Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)), "darkgray")
            else:
                screen.draw.filled_rect(Rect((x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE)), "black")
    

    player.draw()
    

    for enemy in enemies:
        enemy.draw()
    for bullet in bullets:
        bullet.draw()


    if player.invincibility_timer > 0:
        time_left = player.invincibility_timer // 60  
        screen.draw.text(f"Invencibility: {time_left}s", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=30, color="blue")
        
def draw_victory_screen():
    screen.clear()
    screen.draw.text("VICTORY", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="yellow", align="center")
    screen.draw.text("Press ESC to return to the menu", center=(WIDTH // 2, HEIGHT // 2 + 30), fontsize=30, color="white", align="center")

def draw_game_over():
    screen.clear()
    screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 20), fontsize=50, color="red")
    screen.draw.text("Press ENTER to restart", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=30, color="green")
    screen.draw.text("Press ESC to menu", center=(WIDTH // 2, HEIGHT // 2 + 45), fontsize=30, color="white")

pgzrun.go()
