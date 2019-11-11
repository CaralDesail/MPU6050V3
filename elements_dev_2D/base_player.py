import pygame


class Player(pygame.sprite.Sprite):
    # This class represents the player. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height, list_of_limits):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])

        # import list of limits
        self.list_of_limits = list_of_limits
        # resquale the limits
        self.newXmax = int(list_of_limits[3]) - int(list_of_limits[2])
        self.newYmax = int(list_of_limits[5]) - int(list_of_limits[4])

        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Instead we could load a proper pciture of a car...
        # self.image = pygame.image.load("image.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self, x_m, y_m):
        self.newX = x_m - int(self.list_of_limits[2])  # rescale the x value from 0 to 36000
        self.rapnewX = self.newX / self.newXmax  # scale in relation with max value -> the fraction'll been between 0
        # and 1
        print("Rapport X: ", self.rapnewX)
        self.newY = y_m - int(self.list_of_limits[4])  # rescale the y value from 0 to 36000
        self.rapnewY = self.newY / self.newYmax  # scale in relation with max value -> the fraction'll been between 0
        # and 1
        print("Rapport Y: ", self.rapnewY)

        if self.rapnewX > 0.7: self.rect.x += 3  # use of xmin
        if self.rapnewX < 0.3: self.rect.x -= 3  # use of xmax
        if self.rapnewY > 0.7: self.rect.y += 3  # use of ymin
        if self.rapnewY < 0.3: self.rect.y -= 3  # use of ymax
