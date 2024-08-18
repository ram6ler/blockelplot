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
