# Blockelplot

Welcome to *blockelplot*, a Python library for basic graphics in the terminal.


## Install

Install directly from this repository using:

```txt
pip install git+https://github.com/ram6ler/blockelplot
```

## Use

The library exposes a *Screen* class that can be instantiated, drawn to and printed to the terminal. Internally, [unicode block elements](https://en.wikipedia.org/wiki/Block_Elements) are used to draw the "pixels" to the terminal.

```py
Screen(
  height_in_pixels: int,
  width_in_pixels: int,
  adjust_aspect=False
)
```

An instance of *Screen* has the following methods:

### pixel

```py
pixel(
    row: int,
    column: int,
    wrap=False,
    mode=Mode.write
)
```

Draws a pixel at row-column coordinates *(row, column)*.

Example:

```py
from blockelplot import Screen

zig, zag = 8, 8
column, direction = 0, 2

screen = Screen(32, 18)

for row in range(32):
    screen.pixel(row, column)
    column += direction
    zig -= 1
    if zig == 0:
        zag -= 1
        zig = zag
        direction *= -1

print(screen)
```

```txt
▘▖       
  ▘▖     
    ▘▖   
      ▘▖ 
       ▖▘
     ▖▘  
   ▖▘    
 ▖▘      
  ▘▖     
    ▘▖   
      ▘▖ 
     ▖▘  
   ▖▘    
  ▘▖     
    ▘▖   
     ▖▘  
```

### line

```py
line(
    r0: int,
    c0: int,
    r1: int,
    c1: int,
    wrap=False,
    mode=Mode.write
)
```

Draws a line between row-column points *(r0, c0)* and *(r1, c1)*.

Example:

```py
from math import pi, sin, cos
from blockelplot import Screen

rows, columns = 32, 32
radius = 14
screen = Screen(rows, columns, adjust_aspect=True)

vertices = 5
r0, c0 = rows // 2, columns // 2


def theta(i: int) -> float:
    return 2 * pi * (i + 0.75) / vertices


def map_row(i: int) -> int:
    return r0 + int(radius * sin(theta(i)))


def map_column(i: int) -> int:
    return c0 + int(radius * cos(theta(i)))


for i in range(vertices):
    for j in (j for j in range(vertices) if abs(j - i) % (vertices - 1) > 1):
        screen.line(map_row(i), map_column(i), map_row(j), map_column(j))

print(screen)

```
```txt
                                
                █               
               █ █              
              ▄▀ ▀▄             
              █   █             
             █     █            
   ▀██▀▀▀▀▀▀█▀▀▀▀▀▀▀█▀▀▀▀▀▀██▀  
      ▀▄    █       █    ▄▀     
        ▀▀▄▄▀       ▀▄▄▀▀       
           █▀▄     ▄▀█          
          █   ▀▄▄▄▀   █         
         ▄▀  ▄▄▀ ▀▄▄  ▀▄        
         █ ▄▀       ▀▄ █        
        █▀▀           ▀▀█
```

### circle

```py
circle(
    row: int,
    column: int,
    radius: int,
    wrap=False,
    mode=Mode.write,
)
```

Draws a circle with center at row-column coordinates *(row, column)* and radius *radius*.

Example:

```py
from blockelplot import Screen

screen = Screen(32, 48, adjust_aspect=True)

for i in range(5):
    screen.circle(
        row=(i % 2) * 8 + 8,
        column=i * 8 + 8,
        radius=7,
    )

print(screen)
```

```txt
      ▄▄▄▄▄           ▄▄▄▄▄           ▄▄▄▄▄     
   ▄▀▀     ▀▀▄     ▄▀▀     ▀▀▄     ▄▀▀     ▀▀▄  
  █           █   █           █   █           █ 
 █             █ █             █ █             █
 █            ▄█▄█▄           ▄█▄█▄            █
 ▀▄        ▄▀▀▄▀ ▀▄▀▀▄     ▄▀▀▄▀ ▀▄▀▀▄        ▄▀
  ▀▄      █  ▄▀   ▀▄  █   █  ▄▀   ▀▄  █      ▄▀ 
    ▀▀▄▄▄█▄▀▀       ▀▀▄█▄█▄▀▀       ▀▀▄█▄▄▄▀▀   
         █             █ █             █        
         ▀▄           ▄▀ ▀▄           ▄▀        
          ▀▄         ▄▀   ▀▄         ▄▀         
            ▀▀▄▄▄▄▄▀▀       ▀▀▄▄▄▄▄▀▀
```

### rectangle

```py
rectangle(
    top_left_row: int,
    top_left_column: int,
    height: int,
    width: int,
    wrap=False,
    mode=Mode.write
)
```

Draws a rectangle with top-left corner at row-column coordinates *(top_left_row, top_left_column)*, width *width* and height *height*.

Example:

```py
from blockelplot import Screen

width, height = 4, 8
screen = Screen(20, 38, adjust_aspect=True)
column = 0
dw = 1
for i in range(7):
    row = i % 2 * (height + 2)
    screen.rectangle(row, column, height, width)
    column += width
    width += dw
    if width >= 7:
        dw = -1

print(screen)
```

```txt
█▀▀▀█    █▀▀▀▀▀█      █▀▀▀▀▀█    █▀▀▀█
█   █    █     █      █     █    █   █
█   █    █     █      █     █    █   █
█   █    █     █      █     █    █   █
▀▀▀▀▀    ▀▀▀▀▀▀▀      ▀▀▀▀▀▀▀    ▀▀▀▀▀
    █▀▀▀▀█     █▀▀▀▀▀▀█     █▀▀▀▀█    
    █    █     █      █     █    █    
    █    █     █      █     █    █    
    █    █     █      █     █    █    
    ▀▀▀▀▀▀     ▀▀▀▀▀▀▀▀     ▀▀▀▀▀▀ 
```

### polygon

```py
polygon(
    row: int,
    column: int,
    radius: float,
    sides: int, 
    otation=0.0,
    wrap=False,
    mode=Mode.write
)
```

Draws a regular polygon with *sides* sides, center at row-column coordinates *(row, column)* and radius *radius*.

Example:

```py
from blockelplot import Screen

screen = Screen(32, 32, adjust_aspect=True)
radius = 15
for i, sides in enumerate((7, 6, 5, 4, 3)):
    screen.polygon(
        16,
        16,
        radius,
        sides,
    )
    radius = int(0.75 * radius)

print(screen)
```

```txt
             ▄▄                 
          ▄▀▀  ▀▀▀▀▄▄▄▄         
       ▄▄▀             ▀▀▀▄     
     ▄▀   █▀▀▀▀▀▀▀▀▀▀▀▀▄  ▀▄    
  ▄▀▀    █    ▄▄▄▀▀▄   ▀▄  ▀▄   
  █     █ ▄▄▀▀ ▄▀▄  █   ▀▄  ▀▄  
  █    █  █  ▄█   ▀▄ ▀▄  ▀▄  ▀▄ 
  █   █   █▄▀ █▀▀▄▄ ▀▄ █  ▀▄  ▀▄
  █  ▀▄   █▄  █   ▄█▀▄▀▄▀ ▄▀  ▄▀
  █   ▀▄  █ ▀▄█▄▀▀ ▄▀ █  ▄▀  ▄▀ 
  █    ▀▄ █▄  ▀▄ ▄▀ ▄▀  ▄▀  ▄▀  
  █      █  ▀▀▀▄█  █   ▄▀  ▄▀   
   ▀▀▄    █      ▀▀   ▄▀  ▄▀    
      ▀▄▄  ▀▀▀▀▀▀▀▀▀▀▀▀  ▄▀     
         ▀▄         ▄▄▄▄▀▀      
           ▀▀▄▄▄▀▀▀▀               
```

### poke

```py
poke(
    row: int,
    column: int,
    datum: int,
    bits=8,
    wrap=False,
    inverse=False
)
```

Pokes a bitwise pattern defined by *datum* at row-column point *(row, column)*. (Similarly, method *peek* allows us to read data from a point on the screen.)

Example:

```py
from blockelplot import Screen

screen = Screen(16, 4, adjust_aspect=True)

for i in range(16):
    screen.poke(i, 0, i, bits=4)

print(screen)
```
```txt
   ▄
  █▄
 █ ▄
 ██▄
█  ▄
█ █▄
██ ▄
███▄
```

### sprite

```py
sprite(
    row: int,
    column: int,
    sprite_data: list[int],
    bits=8,
    wrap=False,
    inverse=False
)
```

A convenience method for poking a set of bitwise patterns defined by *data* at row-column point *(row, column)*.

Example:

```py
from blockelplot import Screen

wizard_data = [
    # datum      # binary
    0x00000000,  # ................................
    0x00000100,  # .......................1........
    0x00000700,  # .....................111........
    0x00003F00,  # ..................111111........
    0x0001E700,  # ...............1111..111........
    0x0003E700,  # ..............11111..111........
    0x8402FF00,  # 1....1........1.11111111........
    0x84043F00,  # 1....1.......1....111111........
    0x78080E00,  # .1111.......1.......111.........
    0x30100100,  # ..11.......1...........1........
    0x30331980,  # ..11......11..11...11..11.......
    0x30233180,  # ..11......1...11..11...11.......
    0x30118100,  # ..11.......1...11......1........
    0x300D2600,  # ..11........11.1..1..11.........
    0x3013FA00,  # ..11.......1..1111111.1.........
    0x30100200,  # ..11.......1..........1.........
    0x7038C700,  # .111......111...11...111........
    0x7C3C07F0,  # .11111....1111.......1111111....
    0x7EFE0FFE,  # .111111.1111111.....11111111111.
    0x37FF9F9C,  # ..11.111111111111..111111..111..
    0x33FFDF38,  # ..11..111111111111.11111..111...
    0x307FFF70,  # ..11.....111111111111111.111....
    0x303FFFE0,  # ..11......11111111111111111.....
    0x303FFFE0,  # ..11......11111111111111111.....
    0x303FFFC0,  # ..11......1111111111111111......
    0x301FFF80,  # ..11.......11111111111111.......
    0x301FFE00,  # ..11.......111111111111.........
    0x301FFE00,  # ..11.......111111111111.........
    0x301FFE00,  # ..11.......111111111111.........
    0x301FFE00,  # ..11.......111111111111.........
    0x303FFF00,  # ..11......11111111111111........
    0x307FFF80,  # ..11.....1111111111111111.......
]

screen = Screen(32, 32, adjust_aspect=True)
screen.sprite(0, 0, wizard_data, bits=32)
print(screen)
```

```txt
                       ▄        
                  ▄▄▄███        
              ▄████  ███        
█    █       ▄▀ ▀▀██████        
 ▀██▀      ▄▀       ▀▀▀▄        
  ██      █▀  ██  ▄█▀  ██       
  ██       ▀▄▄ █▀ ▄  ▄▄▀        
  ██       █  ▀▀▀▀▀▀▀ █         
 ███▄▄    ███▄  ▀▀   ███▄▄▄▄    
 ▀██▀██▄███████▄▄  ▄█████▀▀███▀ 
  ██  ▀▀▀█████████▄█████ ▄██▀   
  ██      █████████████████     
  ██      ▀██████████████▀      
  ██       ████████████         
  ██       ████████████         
  ██     ▄██████████████▄ 
  ```

  Thanks for your interest! Feel free to [report any issues](https://github.com/ram6ler/blockelplot/issues).