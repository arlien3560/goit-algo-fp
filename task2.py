import turtle

def pifagor_tree(level, size, tree):
    if level == 0:
        return

    tree.forward(size)

    tree.left(45)
    pifagor_tree(level - 1, size / 1.414, tree)

    tree.right(90)
    pifagor_tree(level - 1, size / 1.414, tree)

    tree.left(45)
    tree.backward(size)

def main():
    input_level = int(input("Введіть рівень рекурсії (наприклад, 5): "))
    input_size = 100

    tirtle_item = turtle.Turtle()
    tirtle_item.left(90)
    tirtle_item.penup()
    tirtle_item.goto(0, -200)
    tirtle_item.pendown()
    
    pifagor_tree(input_level, input_size, tirtle_item)
    
    turtle.done()

if __name__ == "__main__":
    raise SystemExit(main())