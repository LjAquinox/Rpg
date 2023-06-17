import pygame
import sys
import random

class Resource:
    def __init__(self, name, drop_probability, quantity_range):
        self.name = name
        self.drop_probability = drop_probability
        self.quantity_range = quantity_range

class Tile:
    def __init__(self, tile_type, resources=None):
        self.tile_type = tile_type
        self.color = self.get_color()
        self.resources = resources if resources else []

    def get_color(self):
        if self.tile_type == 1:  # grass
            return (0, 255, 0)
        elif self.tile_type in resources :
            return (resources[self.tile_type]['color'])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = {}
        self.color=(255,0,0)

    def display_inventory(self):
        for item, quantity in self.inventory.items():
            print(f"{item}: {quantity}")

    def add_to_inventory(self, item, quantity):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def harvest(self, game):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            tile_type = game.map[(x, y)].tile_type
            if tile_type in resources:
                # Harvest resources from the tile
                for ressource_name , properties in resources[tile_type]['properties'].items():
                    if random.random() < properties['drop_probability']:
                        quantity = random.randint(properties['drop_quantity_range'][0],properties['drop_quantity_range'][1])
                        print(f"obtained {ressource_name} x {quantity}")
                        self.add_to_inventory(ressource_name, quantity)
                # Check if the tile should disappear
                if random.random() < resources[tile_type]['disappearance_probability']:
                    game.map[(x, y)] = Tile(1)  # Replace the tile with grass



resources = {
    2: {  # tree
        'properties' : {
                        'wood': {'drop_probability': 1, 'drop_quantity_range': (2, 3)},
                        'apple': {'drop_probability': 0.05, 'drop_quantity_range': (1, 2)},
                        'wodd fairy': {'drop_probability': 0.001, 'drop_quantity_range': (1, 1)},
                        },
        'disappearance_probability': 0.2,  # 20% chance for the tree to disappear after harvesting
        'spawnRate':50,
        'color':(0,100,0)
    },
    3: {  # rock
        'properties': {
            'stone': {'drop_probability': 1, 'drop_quantity_range': (1, 3)},
            'flint': {'drop_probability': 0.05, 'drop_quantity_range': (1, 2)},
            'stone fairy': {'drop_probability': 0.001, 'drop_quantity_range': (1, 1)},
        },
        'disappearance_probability': 0.35,  # 20% chance for the stone to disappear after harvesting
        'spawnRate' : 100,
        'color':(0,0,0)
    }
}


class Game() :
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.FOV = 10
        self.Nb_Tile_x = self.WINDOW_WIDTH // self.FOV
        self.Nb_Tile_y = self.WINDOW_HEIGHT // self.FOV
        self.TILE_SIZE_x = self.WINDOW_WIDTH // self.Nb_Tile_x
        self.TILE_SIZE_y = self.WINDOW_HEIGHT // self.Nb_Tile_y

        self.player = Player(0, 0)
        self.map = {}
        self.map[(0,0)] = Tile(1)
        self.probaRessources = self.GetProbas()
        print(self.probaRessources)
        self.displayable_range_x = range(self.player.x - self.Nb_Tile_x//2,self.player.x + self.Nb_Tile_x//2 + 1)
        self.displayable_range_y = range(self.player.y - self.Nb_Tile_y // 2, self.player.y + self.Nb_Tile_y // 2 + 1)
        self.explored = {}

        # Create the window and set its caption
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('2D Game')

    def GetProbas(selfself):
        return([(elem,resources[elem]['spawnRate']) for elem in resources])

    def Recalc_FOV(self):
        self.Nb_Tile_x = self.WINDOW_WIDTH // self.FOV
        self.Nb_Tile_y = self.WINDOW_HEIGHT // self.FOV
        self.TILE_SIZE_x = self.WINDOW_WIDTH // self.Nb_Tile_x
        self.TILE_SIZE_y = self.WINDOW_HEIGHT // self.Nb_Tile_y
        self.explored = {}
        self.generate_map()

    def Get_display_Range(self):
        self.displayable_range_x = range(self.player.x - self.Nb_Tile_x // 2, self.player.x + self.Nb_Tile_x // 2 + 1)
        self.displayable_range_y = range(self.player.y - self.Nb_Tile_y // 2, self.player.y + self.Nb_Tile_y // 2 + 1)


    def generate_map(self):
        self.Get_display_Range()
        if self.explored.get((self.player.x,self.player.y)) == None :
            for x in self.displayable_range_x:
                for y in self.displayable_range_y:
                    if self.map.get((x,y)) == None :
                        self.map[(x, y)] = Tile(1)  # grass
                        for RessourceTypes in self.probaRessources :
                            if random.randint(0, RessourceTypes[1]) == 0:
                                self.map[(x, y)] = Tile(RessourceTypes[0], resources[RessourceTypes[0]])
        self.explored[(self.player.x,self.player.y)] = True

    def drawPlayer(self,surface):
        pygame.draw.rect(surface, self.player.color,
                         ((self.Nb_Tile_x // 2) * self.TILE_SIZE_x,
                          (self.Nb_Tile_y // 2) * self.TILE_SIZE_y,
                          self.TILE_SIZE_x,
                          self.TILE_SIZE_y))

    def main(self):
        # Main game loop
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_z]:  # up
                self.player.y -= 1
            if keys[pygame.K_s]:  # down
                self.player.y += 1
            if keys[pygame.K_q]:  # left
                self.player.x -= 1
            if keys[pygame.K_d]:  # right
                self.player.x += 1
            if keys[pygame.K_KP_PLUS]:
                self.FOV += 2
                self.Recalc_FOV()
                print(self.FOV)
            if keys[pygame.K_KP_MINUS]:
                self.FOV = max(2,self.FOV-2)
                self.Recalc_FOV()
                print(self.FOV)
            if keys[pygame.K_SPACE]:
                self.player.harvest(self)
            if keys[pygame.K_TAB]:
                print("ok")
                self.player.display_inventory()

            self.generate_map()

            for x in range(0,self.Nb_Tile_x) :
                for y in range(0,self.Nb_Tile_y) :
                    tile_color = self.map[(self.displayable_range_x[x], self.displayable_range_y[y])].color
                    pygame.draw.rect(self.screen, tile_color, (x * self.TILE_SIZE_x, y * self.TILE_SIZE_y,self.TILE_SIZE_x, self.TILE_SIZE_y))

            # Draw the player
            self.drawPlayer(self.screen)


            # Update the display
            pygame.display.flip()
            pygame.time.delay(50)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game_elem = Game()
    Game_elem.main()