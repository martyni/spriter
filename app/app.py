import pygame
import os
from string import ascii_letters
from copy import deepcopy, copy
from pygame.locals import *
from random import randint, choice
import math
LIGHT_GREY = (240,240,245)

class Canvas(pygame.sprite.Sprite):
    def __init__(self, size, window, grid=(32, 32), image=None, preview=None, colour=None, file_=None):
       pygame.sprite.Sprite.__init__(self)
       self.x, self.y = size
       self.grid = grid
       self.file_=file_
       self.window = window
       self.grid_array = [[tuple((0,0,0,0)) for i in range(grid[0])] for j in range(grid[1])]
       self.image = pygame.Surface([self.x + 5, self.y + 5], pygame.SRCALPHA, 32) if image is None else image
       self.preview = pygame.Surface(self.grid, pygame.SRCALPHA, 32) if preview is None else preview
       self.x_gap = int(self.x / grid[0])
       self.y_gap = int(self.y / grid[1])
       self.colour = (0, 0, 0, 100) if not colour else colour
       self.rubber = (0, 0, 0, 0)
       self.draw()

    def draw(self,color=(0,0,0)):   
       for j in range( self.grid[0] +1):
           pygame.draw.line(
                   self.image,
                   color,
                   [j * self.x_gap, self.y],
                   [j * self.x_gap, 0],
                   )
            
       for i in range( self.grid[1] +1):
           pygame.draw.line(
                   self.image,
                   color,
                   [self.x, i * self.y_gap],
                   [0, i * self.y_gap],
                   )
       self.rect = self.image.get_rect()
    
    def brush(self, draw, rubber, position):
        x,y = position
        grid_position = [ x/self.x_gap , y/self.y_gap]
        if grid_position[0] <  self.grid[0] and grid_position[1] < self.grid[1]:
           rec = Rect(
                   grid_position[0] * self.x_gap, 
                   grid_position[1] * self.y_gap,
                   self.x_gap,
                   self.y_gap)
           if draw:
              pygame.draw.line(
                      self.preview,
                      self.colour,
                      grid_position,
                      grid_position
                      )

              pygame.draw.rect(
                      self.image,
                      self.colour,
                      rec,
                      )
           elif rubber:   
              pygame.draw.rect(
                      self.image,
                      self.rubber,
                      rec,
                      )
              pygame.draw.line(
                      self.preview,
                      self.rubber,
                      grid_position,
                      grid_position
                      )
           self.draw()   
              

    def update(self):
        pass
        #self.draw((randint(0,255), randint(0,255), randint(0,255)))

class Default(pygame.sprite.Group):
    pass

class Wheel(pygame.sprite.Sprite):
    def __init__(self, size):
        self.size = size
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.size, self.size], pygame.SRCALPHA, 32)
        self.quarter_size = int(size /4 )
        for i in range(self.quarter_size):
            for j in range(self.quarter_size):
                normalized_i = int(float(i)/self.quarter_size * 255)
                normalized_j = int(float(j)/self.quarter_size * 255)
                color = (255 - normalized_i ,255 - normalized_j, 0)
                pygame.draw.line(
                        self.image,
                        color,
                        (i, j),
                        (i, j)
                )
        for i in range(self.quarter_size):
            for j in range(self.quarter_size):
                normalized_i = int(float(i)/self.quarter_size * 255)
                normalized_j = int(float(j)/self.quarter_size * 255)
                color = ( 255 - normalized_i ,0 , normalized_j)
                pygame.draw.line(
                        self.image,
                        color,
                        (i, j + self.quarter_size),
                        (i, j + self.quarter_size)
                )
        for i in range(self.quarter_size):
            for j in range(self.quarter_size):
                normalized_i = int(float(i)/self.quarter_size * 255)
                normalized_j = int(float(j)/self.quarter_size * 255)
                color = ( 0 ,normalized_i , normalized_j)
                pygame.draw.line(
                        self.image,
                        color,
                        (i + self.quarter_size, j + self.quarter_size),
                        (i + self.quarter_size, j + self.quarter_size)
                )
        self.rect =  self.image.get_rect()
        self.rect.x = self.size 
        self.colour = (0,0,0,255)
        self.colours = [(0,0,0,0)]
    def draw_colours(self):
        i = 0
        j = 0
        self.limit = 6
        outer = pygame.Rect(
                300,
                0,
                self.rect.bottomright[0] -1,
                self.rect.bottomright[1] -1
                )
        pygame.draw.rect(
                self.image,
                self.colour,
                outer
                )
        for col in self.colours:
           rect = pygame.Rect(
                   self.quarter_size + self.quarter_size * i/6,
                   self.quarter_size * j/6,
                   self.quarter_size/6,
                   self.quarter_size/6  
                   )

           pygame.draw.rect(
                   self.image,
                   col,
                   rect
                   )
           if not i % 6:
               j += 1
               i = 0
           if not j % 6:
               j = 0
           i += 1

    def brush(self, draw, rubber, position):
        if draw:
           rel_position = [position[0] - self.rect.x, position[1] - self.rect.y ]
           if position[0] > self.rect.topleft[0] and position[0] < self.rect.bottomright[0]  and position[1] > self.rect.topleft[1] and position[1] < self.rect.bottomright[1]:
              self.colours.append(self.image.get_at(rel_position))
              self.colour = self.image.get_at(rel_position)
              self.draw_colours()
              return self.image.get_at(rel_position)
        else:
           return None 

class Spriter(object):
    def copy_current_canvas(self):
       tmp = Canvas(
          [self.width/2, self.height/2],
          self.screen,
          image=self.canvas.image.copy(),
          preview=self.canvas.preview.copy(),
          colour=self.colour
       )
       self.canvas.kill()
       self.canvas = tmp
       self.default_sprites.add(self.canvas)
       self.frames.append(self.canvas)

    def create_new_canvas(self):
       self.canvas.kill()
       self.canvas = Canvas(
          [self.width/2, self.height/2],
          self.screen,
          colour=self.colour
       )
       self.default_sprites.add(self.canvas)
       self.frames.append(self.canvas)

    def select_frame(self, frame):
       try:
          tmp = self.frames[frame]
       except:
          print "frame out of range" 
          return None 
       self.canvas.kill()
       self.canvas = tmp
       self.canvas.colour = self.colour
       self.default_sprites.add(self.canvas)

    def __init__(self):
       pygame.init()
       self.width = 1024
       self.height = 768
       self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF)
       self.running = True
       self.draw = False
       self.rubber = False
       self.clock = pygame.time.Clock() 
       self.canvas_pointer = 0
       self.canvas = Canvas(
               [self.width/2, self.height/2],
               self.screen
               )
       self.frames = [self.canvas]
       self.wheel = Wheel(self.width/2)
       self.default_sprites = Default()
       self.default_sprites.add(self.canvas, self.wheel)
       self.colour = (0,0,0,100)
       pygame.time.set_timer(31, 100)
       while self.running:
          self.screen.fill(LIGHT_GREY)
          for event in pygame.event.get():
             if event.type==KEYDOWN:
                if event.key==K_n:
                   self.create_new_canvas()
                if event.key==K_c:
                   self.copy_current_canvas()
                if event.key in (K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0):
                    self.number_dict = {
                            K_1: 0,
                            K_2: 1,
                            K_3: 2,
                            K_4: 3,
                            K_5: 4,
                            K_6: 5,
                            K_7: 6,
                            K_8: 7,
                            K_9: 8,
                            K_0: 9,

                            }        
                    self.select_frame(self.number_dict[event.key])
                if event.key==K_s:
                    random_path = ''.join([choice(ascii_letters) for _ in range(3)])
                    os.makedirs(random_path)
                    for im in range(len(self.frames)):
                        pygame.image.save(self.frames[im].preview, "{}/{}.tga".format(random_path, im))
                        pygame.image.save(self.frames[im].image, "{}/{}-canvas.tga".format(random_path, im))
             if event.type==31:
                self.canvas_pointer +=1       
             if event.type==QUIT:
                self.running = False
             elif event.type==MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                   self.draw = True
                if pygame.mouse.get_pressed()[2]:
                   self.rubber = True
             elif event.type==MOUSEBUTTONUP:  
                if not pygame.mouse.get_pressed()[0]:
                   self.draw = False
                if not pygame.mouse.get_pressed()[2]:
                   self.rubber = False
             if event.type==VIDEORESIZE:
                print event
          self.canvas.brush(self.draw, self.rubber, pygame.mouse.get_pos())
          c = self.wheel.brush(self.draw, self.rubber, pygame.mouse.get_pos())
          if c:
             self.canvas.colour = c
             self.colour = c
          self.default_sprites.draw(self.screen)      
          
          if self.canvas_pointer >= len(self.frames):
              self.canvas_pointer = 0
          self.screen.blit(pygame.transform.scale2x(self.frames[self.canvas_pointer].preview), [self.width/2, self.height/2])
          pygame.display.flip()
          self.default_sprites.update()
          self.clock.tick(30)





def main():
   my_game = Spriter()
   
if __name__ == "__main__":
    main()
