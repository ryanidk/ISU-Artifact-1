from flask import Flask, request, render_template, redirect, url_for, session
import math
from groq import Groq
import os
import json
import random

# Flask app setup
app = Flask(__name__)
groq_api_key = os.getenv('GROQ_API_KEY')
app.secret_key = os.getenv('SECRET_KEY')
groq_client = Groq(api_key=groq_api_key)


def round_4(value):
    if value.is_integer():
        return f"{int(value)}"
    elif len(f"{value}".split('.')[1]) <= 4:
        return f"{value}"
    else:
        return f"~{value:.4f}"

def generate_options(correct_answer):
    options = [correct_answer]
    while len(options) < 4:
        deviation = random.uniform(-0.5, 0.5) * correct_answer if correct_answer != 0 else random.uniform(1, 5)
        wrong_answer = round(correct_answer + deviation, 2)
        if wrong_answer != correct_answer and wrong_answer not in options and wrong_answer > 0:
            options.append(wrong_answer)
    random.shuffle(options)
    return options

def generate_quiz(num_questions, difficulty):
    questions = []

    shapes_by_difficulty = {
        'easy': ['circle', 'square', 'rectangle', 'cube', 'rectanglePrism', 'triangle', 'cylinder', 'cone', 'squarePyramid', 'trianglePrism'],
        'medium': ['trapezium', 'parallelogram', 'pentagon', 'hexagon', 'pentagonPrism', 'hexagonPrism', 'trianglePyramid', 'parallelogramPrism', 'trapeziumPrism', 'rhombus', 'kite'],
        'hard': ['heptagon', 'octagon', 'nonagon', 'decagon', 'heptagonPrism', 'octagonPrism', 'nonagonPrism', 'decagonPrism', 'pentagonPyramid', 'hexagonPyramid']
    }

    all_shapes = shapes_by_difficulty[difficulty]

    num_shapes = int(num_questions * 0.85)
    num_pythagorean = num_questions - num_shapes

    for _ in range(num_shapes):
        shape = random.choice(all_shapes)
        question = generate_question(shape)
        questions.append(question)

    for _ in range(num_pythagorean):
        question = generate_pythagorean()
        questions.append(question)

    random.shuffle(questions)
    return questions

def generate_question(shape):
    working_backward = random.random() < 0.3
    question = {}
    correct_answer = None
    formula = ''

    if shape == 'cube':
        side = random.randint(1, 10)
        formula = 'V = s³'
        if working_backward:
            volume = side ** 3
            question_text = f"A cube has a volume of {volume}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"A cube has sides of length {side}. What is its volume?"
            correct_answer = side ** 3

    elif shape == 'cylinder':
        radius = random.randint(1, 10)
        height = random.randint(1, 10)
        formula = 'V = π r² h'
        if working_backward:
            volume = round(math.pi * radius ** 2 * height, 2)
            question_text = f"A cylinder has a volume of {volume}. Its radius is {radius}. What is its height? (Use π ≈ 3.14)"
            correct_answer = height
        else:
            question_text = f"A cylinder has a radius of {radius} and a height of {height}. What is its volume? (Use π ≈ 3.14)"
            correct_answer = round(math.pi * radius ** 2 * height, 2)

    elif shape == 'cone':
        radius = random.randint(1, 10)
        height = random.randint(1, 10)
        formula = 'V = (1/3) π r² h'
        if working_backward:
            volume = round((math.pi * radius ** 2 * height) / 3, 2)
            question_text = f"A cone has a volume of {volume} and a radius of {radius}. What is its height? (Use π ≈ 3.14)"
            correct_answer = height
        else:
            question_text = f"A cone has a radius of {radius} and a height of {height}. What is its volume? (Use π ≈ 3.14)"
            correct_answer = round((math.pi * radius ** 2 * height) / 3, 2)

    elif shape == 'trianglePrism':
        base = random.randint(1, 10)
        height_base = random.randint(1, 10)
        length = random.randint(1, 10)
        formula = 'V = (1/2) × base × height × length'
        if working_backward:
            volume = 0.5 * base * height_base * length
            question_text = f"A triangular prism has a volume of {volume}. The base of the triangle is {base}, and the height of the triangle is {height_base}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A triangular prism has a triangle base with base {base} and height {height_base}, and a length of {length}. What is its volume?"
            correct_answer = 0.5 * base * height_base * length

    elif shape == 'rectanglePrism':
        length_val = random.randint(1, 10)
        width = random.randint(1, 10)
        height = random.randint(1, 10)
        formula = 'V = length × width × height'
        if working_backward:
            volume = length_val * width * height
            question_text = f"A rectangular prism has a volume of {volume}. The width is {width} and the height is {height}. What is its length?"
            correct_answer = length_val
        else:
            question_text = f"A rectangular prism has dimensions length {length_val}, width {width}, and height {height}. What is its volume?"
            correct_answer = length_val * width * height

    elif shape == 'rhombusPrism':
        p = random.randint(1, 10)
        q = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (p * q) / 2
        formula = 'V = (p × q) / 2 × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A rhombus prism has a volume of {volume}, with diagonals {p} and {q} in the base rhombus. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A rhombus prism has diagonals {p} and {q} in the base rhombus, and a length of {length}. What is its volume?"
            correct_answer = area_base * length

    elif shape == 'trapeziumPrism':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        height_base = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = 0.5 * (a + b) * height_base
        formula = 'V = (1/2)(a + b) × height × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A trapezium prism has a volume of {volume}, bases of lengths {a} and {b}, and a height of {height_base} in the base trapezium. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A trapezium prism has bases {a} and {b}, height {height_base} in the base trapezium, and length {length}. What is its volume?"
            correct_answer = area_base * length

    elif shape == 'parallelogramPrism':
        base = random.randint(1, 10)
        height_base = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = base * height_base
        formula = 'V = base × height × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A parallelogram prism has a volume of {volume}, base {base}, and height {height_base} in the base parallelogram. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A parallelogram prism has base {base}, height {height_base} in the base parallelogram, and length {length}. What is its volume?"
            correct_answer = area_base * length

    elif shape == 'pentagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (5 / 4) * side ** 2 * (1 / math.tan(math.pi / 5))
        formula = 'V = [(5 × side²) / (4 × tan(π/5))] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A pentagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A pentagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'hexagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (3 * math.sqrt(3) * side ** 2) / 2
        formula = 'V = [(3√3 × side²) / 2] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A hexagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A hexagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'heptagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (7 / 4) * side ** 2 * (1 / math.tan(math.pi / 7))
        formula = 'V = [(7 × side²) / (4 × tan(π/7))] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A heptagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A heptagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'octagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = 2 * (1 + math.sqrt(2)) * side ** 2
        formula = 'V = [2(1 + √2) × side²] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"An octagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"An octagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'nonagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (9 / 4) * side ** 2 * (1 / math.tan(math.pi / 9))
        formula = 'V = [(9 × side²) / (4 × tan(π/9))] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A nonagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A nonagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'decagonPrism':
        side = random.randint(1, 10)
        length = random.randint(1, 10)
        area_base = (5 * side ** 2) * (1 / math.tan(math.pi / 10))
        formula = 'V = [(5 × side²) / tan(π/10)] × length'
        if working_backward:
            volume = area_base * length
            question_text = f"A decagonal prism has a volume of {round(volume, 2)} and base side length {side}. What is the length of the prism?"
            correct_answer = length
        else:
            question_text = f"A decagonal prism has base side length {side} and length {length}. What is its volume?"
            correct_answer = round(area_base * length, 2)

    elif shape == 'trianglePyramid':
        side = random.randint(1, 10)
        height = random.randint(1, 10)
        area_base = (math.sqrt(3) / 4) * side ** 2
        formula = 'V = [(√3 / 4) × side² × height] / 3'
        if working_backward:
            volume = (area_base * height) / 3
            question_text = f"A triangular pyramid has a volume of {round(volume, 2)} and base side length {side}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A triangular pyramid has base side length {side} and height {height}. What is its volume?"
            correct_answer = round((area_base * height) / 3, 2)

    elif shape == 'squarePyramid':
        side = random.randint(1, 10)
        height = random.randint(1, 10)
        area_base = side ** 2
        formula = 'V = (side² × height) / 3'
        if working_backward:
            volume = (area_base * height) / 3
            question_text = f"A square pyramid has a volume of {volume} and base side length {side}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A square pyramid has base side length {side} and height {height}. What is its volume?"
            correct_answer = (area_base * height) / 3

    elif shape == 'pentagonPyramid':
        side = random.randint(1, 10)
        height = random.randint(1, 10)
        area_base = (5 / 4) * side ** 2 * (1 / math.tan(math.pi / 5))
        formula = 'V = [(5 × side²) / (4 × tan(π/5)) × height] / 3'
        if working_backward:
            volume = (area_base * height) / 3
            question_text = f"A pentagonal pyramid has a volume of {round(volume, 2)} and base side length {side}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A pentagonal pyramid has base side length {side} and height {height}. What is its volume?"
            correct_answer = round((area_base * height) / 3, 2)

    elif shape == 'hexagonPyramid':
        side = random.randint(1, 10)
        height = random.randint(1, 10)
        area_base = (3 * math.sqrt(3) * side ** 2) / 2
        formula = 'V = [(3√3 × side²) / 2 × height] / 3'
        if working_backward:
            volume = (area_base * height) / 3
            question_text = f"A hexagonal pyramid has a volume of {round(volume, 2)} and base side length {side}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A hexagonal pyramid has base side length {side} and height {height}. What is its volume?"
            correct_answer = round((area_base * height) / 3, 2)

    elif shape == 'rectanglePyramid':
        length_val = random.randint(1, 10)
        width = random.randint(1, 10)
        height = random.randint(1, 10)
        area_base = length_val * width
        formula = 'V = (length × width × height) / 3'
        if working_backward:
            volume = (area_base * height) / 3
            question_text = f"A rectangular pyramid has a volume of {volume}, base length {length_val}, and base width {width}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A rectangular pyramid has base length {length_val}, base width {width}, and height {height}. What is its volume?"
            correct_answer = (area_base * height) / 3

    elif shape == 'circle':
        radius = random.randint(1, 10)
        formula = 'A = π r²'
        if working_backward:
            area = round(math.pi * radius ** 2, 2)
            question_text = f"A circle has an area of {area}. What is its radius? (Use π ≈ 3.14)"
            correct_answer = radius
        else:
            question_text = f"A circle has a radius of {radius}. What is its area? (Use π ≈ 3.14)"
            correct_answer = round(math.pi * radius ** 2, 2)

    elif shape == 'triangle':
        base = random.randint(1, 15)
        height = random.randint(1, 15)
        formula = 'A = (1/2) × base × height'
        if working_backward:
            area = 0.5 * base * height
            question_text = f"A triangle has an area of {area} and a base of {base}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A triangle has a base of {base} and a height of {height}. What is its area?"
            correct_answer = 0.5 * base * height

    elif shape == 'rectangle':
        length_val = random.randint(1, 15)
        width = random.randint(1, 15)
        formula = 'A = length × width'
        if working_backward:
            area = length_val * width
            question_text = f"A rectangle has an area of {area} and a width of {width}. What is its length?"
            correct_answer = length_val
        else:
            question_text = f"A rectangle has a length of {length_val} and a width of {width}. What is its area?"
            correct_answer = length_val * width

    elif shape == 'square':
        side = random.randint(1, 15)
        formula = 'A = side²'
        if working_backward:
            area = side ** 2
            question_text = f"A square has an area of {area}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"A square has a side length of {side}. What is its area?"
            correct_answer = side ** 2

    elif shape == 'trapezium':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        height = random.randint(1, 10)
        formula = 'A = (1/2)(a + b) × height'
        if working_backward:
            area = 0.5 * (a + b) * height
            question_text = f"A trapezium has an area of {area}, bases of lengths {a} and {b}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A trapezium has bases of lengths {a} and {b}, and a height of {height}. What is its area?"
            correct_answer = 0.5 * (a + b) * height

    elif shape == 'parallelogram':
        base = random.randint(1, 15)
        height = random.randint(1, 15)
        formula = 'A = base × height'
        if working_backward:
            area = base * height
            question_text = f"A parallelogram has an area of {area} and a base of {base}. What is its height?"
            correct_answer = height
        else:
            question_text = f"A parallelogram has a base of {base} and a height of {height}. What is its area?"
            correct_answer = base * height

    elif shape == 'rhombus':
        p = random.randint(1, 15)
        q = random.randint(1, 15)
        formula = 'A = (p × q) / 2'
        if working_backward:
            area = (p * q) / 2
            question_text = f"A rhombus has an area of {area} and one diagonal length of {p}. What is the length of the other diagonal?"
            correct_answer = q
        else:
            question_text = f"A rhombus has diagonals of lengths {p} and {q}. What is its area?"
            correct_answer = (p * q) / 2

    elif shape == 'kite':
        p = random.randint(1, 15)
        q = random.randint(1, 15)
        formula = 'A = (p × q) / 2'
        if working_backward:
            area = (p * q) / 2
            question_text = f"A kite has an area of {area} and one diagonal length of {p}. What is the length of the other diagonal?"
            correct_answer = q
        else:
            question_text = f"A kite has diagonals of lengths {p} and {q}. What is its area?"
            correct_answer = (p * q) / 2

    elif shape == 'pentagon':
        side = random.randint(1, 15)
        formula = 'A = (5 × side²) / [4 × tan(π/5)]'
        if working_backward:
            area = (1/4) * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2
            question_text = f"A regular pentagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular pentagon with a side length of {side}?"
            correct_answer = round((1/4) * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2, 2)

    elif shape == 'hexagon':
        side = random.randint(1, 15)
        formula = 'A = (3√3 × side²) / 2'
        if working_backward:
            area = (3 * math.sqrt(3) * side ** 2) / 2
            question_text = f"A regular hexagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular hexagon with a side length of {side}?"
            correct_answer = round((3 * math.sqrt(3) * side ** 2) / 2, 2)

    elif shape == 'heptagon':
        side = random.randint(1, 15)
        formula = 'A = (7 × side²) / [4 × tan(π/7)]'
        if working_backward:
            area = (7 / 4) * side ** 2 * (1 / math.tan(math.pi / 7))
            question_text = f"A regular heptagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular heptagon with a side length of {side}?"
            correct_answer = round((7 / 4) * side ** 2 * (1 / math.tan(math.pi / 7)), 2)

    elif shape == 'octagon':
        side = random.randint(1, 15)
        formula = 'A = [2(1 + √2) × side²]'
        if working_backward:
            area = 2 * (1 + math.sqrt(2)) * side ** 2
            question_text = f"A regular octagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular octagon with a side length of {side}?"
            correct_answer = round(2 * (1 + math.sqrt(2)) * side ** 2, 2)

    elif shape == 'nonagon':
        side = random.randint(1, 15)
        formula = 'A = (9 × side²) / [4 × tan(π/9)]'
        if working_backward:
            area = (9 / 4) * side ** 2 * (1 / math.tan(math.pi / 9))
            question_text = f"A regular nonagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular nonagon with a side length of {side}?"
            correct_answer = round((9 / 4) * side ** 2 * (1 / math.tan(math.pi / 9)), 2)

    elif shape == 'decagon':
        side = random.randint(1, 15)
        formula = 'A = (5 × side²) / tan(π/10)'
        if working_backward:
            area = (5 * side ** 2) * (1 / math.tan(math.pi / 10))
            question_text = f"A regular decagon has an area of {round(area,2)}. What is the length of one side?"
            correct_answer = side
        else:
            question_text = f"What is the area of a regular decagon with a side length of {side}?"
            correct_answer = round((5 * side ** 2) * (1 / math.tan(math.pi / 10)), 2)

    if isinstance(correct_answer, float):
        correct_answer = round(correct_answer, 2)

    options = generate_options(correct_answer)
    question = {
        'question': question_text,
        'options': options,
        'correct_answer': str(correct_answer),
        'formula': formula
    }
    return question

def generate_pythagorean():
    find_hypotenuse = random.choice([True, False])
    if find_hypotenuse:
        a = random.randint(3, 10)
        b = random.randint(3, 10)
        c = round(math.sqrt(a ** 2 + b ** 2), 2)
        question_text = f"In a right-angled triangle, one side is {a} and the other is {b}. What is the length of the hypotenuse?"
        correct_answer = c
        formula = 'hypotenuse = √(a² + b²)'
    else:
        c = random.randint(5, 15)
        a = random.randint(3, c - 1)
        b = round(math.sqrt(c ** 2 - a ** 2), 2)
        question_text = f"In a right-angled triangle, the hypotenuse is {c} and one side is {a}. What is the length of the other side?"
        correct_answer = b
        formula = 'b = √(hypotenuse² - a²)'

    options = generate_options(correct_answer)
    question = {
        'question': question_text,
        'options': options,
        'correct_answer': str(correct_answer),
        'formula': formula
    }
    return question


@app.route("/", methods=['GET', 'POST'])
def index():
    result = None
    ai_explain = None
    if request.method == 'POST':
        try:
            shape = request.form.get('shape')
            calculation_type = request.form.get('calculation_type')

            # 2D shapes
            if request.form.get('category') == '2d':
                match shape:
                    case "circle":
                        radius = float(request.form['radius'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(math.pi * radius ** 2)}"
                            result += "\nFormula: πr²"
                        elif calculation_type == 'perimeter':
                            result = f"Circumference: {round_4(2 * math.pi * radius)}"
                            result += "\nFormula: 2πr"
                    case "triangle":
                        if calculation_type == 'area':
                            base = float(request.form['base'])
                            height = float(request.form['height'])
                            result = f"Area: {round_4(0.5 * base * height)}"
                            result += "\nFormula: 0.5 * base * height"
                        elif calculation_type == 'perimeter':
                            side1 = float(request.form['side1'])
                            side2 = float(request.form['side2'])
                            side3 = float(request.form['side3'])
                            result = f"Perimeter: {round_4(side1 + side2 + side3)}"
                            result += "\nFormula: side1 + side2 + side3"
                    case "rectangle":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(length * width)}"
                            result += "\nFormula: length * width"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(2 * (length + width))}"
                            result += "\nFormula: 2 * (length + width)"
                    case "square":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(side ** 2)}"
                            result += "\nFormula: side²"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(4 * side)}"
                            result += "\nFormula: 4 * side"
                    case "trapezium":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * (a + b) * height)}"
                            result += "\nFormula: 0.5 * (a + b) * height"
                        elif calculation_type == 'perimeter':
                            c = float(request.form['c'])
                            d = float(request.form['d'])
                            result = f"Perimeter: {round_4(a + b + c + d)}"
                            result += "\nFormula: a + b + c + d"
                    case "parallelogram":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(base * height)}"
                            result += "\nFormula: base * height"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {round_4(2 * (base + side))}"
                            result += "\nFormula: 2 * (base + side)"
                    case "rhombus":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * p * q)}"
                            result += "\nFormula: 0.5 * p * q"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {round_4(4 * side)}"
                            result += "\nFormula: 4 * side"
                    case "kite":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * p * q)}"
                            result += "\nFormula: 0.5 * p * q"
                        elif calculation_type == 'perimeter':
                            a = float(request.form['a'])
                            b = float(request.form['b'])
                            result = f"Perimeter: {round_4(2 * (a + b))}"
                            result += "\nFormula: 2 * (a + b)"
                    case "pentagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.25 * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2)}"
                            result += "\nFormula: 0.25 * √(5 * (5 + 2√5)) * side²"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(5 * side)}"
                            result += "\nFormula: 5 * side"
                    case "hexagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(1.5 * math.sqrt(3) * side ** 2)}"
                            result += "\nFormula: 1.5 * √3 * side²"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(6 * side)}"
                            result += "\nFormula: 6 * side"
                    case "heptagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * 7 * side * math.sqrt(3 + 2 * math.sqrt(5)))}"
                            result += "\nFormula: 0.5 * 7 * side * √(3 + 2√5)"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(7 * side)}"
                            result += "\nFormula: 7 * side"
                    case "octagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(2 * (1 + math.sqrt(2)) * side ** 2)}"
                            result += "\nFormula: 2 * (1 + √2) * side²"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(8 * side)}"
                            result += "\nFormula: 8 * side"
                    case "nonagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * 9 * side * math.sqrt(4 - 2 * math.sqrt(3)))}"
                            result += "\nFormula: 0.5 * 9 * side * √(4 - 2√3)"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(9 * side)}"
                            result += "\nFormula: 9 * side"
                    case "decagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(2.5 * side ** 2 * math.sqrt(5 + 2 * math.sqrt(5)))}"
                            result += "\nFormula: 2.5 * side² * √(5 + 2√5)"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(10 * side)}"
                            result += "\nFormula: 10 * side"

            # 3D shapes
            elif request.form.get('category') == '3d':
                match shape:
                    case "cube":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(6 * side ** 2)}"
                            result += "\nFormula: 6 * side²"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(side ** 3)}"
                            result += "\nFormula: side³"
                    case "cylinder":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * math.pi * radius * (radius + height))}"
                            result += "\nFormula: 2πr(r + h)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(math.pi * radius ** 2 * height)}"
                            result += "\nFormula: πr²h"
                    case "cone":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(math.pi * radius * (radius + math.sqrt(radius ** 2 + height ** 2)))}"
                            result += "\nFormula: πr(r + √(r² + h²))"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(math.pi * radius ** 2 * height / 3)}"
                            result += "\nFormula: (πr²h)/3"
                    case "trianglePrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(base * height + 3 * base * length)}"
                            result += "\nFormula: base * height + 3 * base * length"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(0.5 * base * height * length)}"
                            result += "\nFormula: 0.5 * base * height * length"
                    case "trapeziumPrism":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (0.5 * (a + b) * height + a * length + b * length))}"
                            result += "\nFormula: 2 * (0.5 * (a + b) * height + a * length + b * length)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(0.5 * (a + b) * height * length)}"
                            result += "\nFormula: 0.5 * (a + b) * height * length"
                    case "parallelogramPrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            side = float(request.form['side'])
                            result = f"Surface Area: {round_4(2 * (base * height + base * length + length * side))}"
                            result += "\nFormula: 2 * (base * height + base * length + length * side)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(base * height * length)}"
                            result += "\nFormula: base * height * length"
                    case "rectanglePrism":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (length * width + length * height + width * height))}"
                            result += "\nFormula: 2 * (length * width + length * height + width * height)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(length * width * height)}"
                            result += "\nFormula: length * width * height"
                    case "rhombusPrism":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(p * q + 2 * math.sqrt(p**2 + q**2) * length)}"
                            result += "\nFormula:  p * q + 2 * √(p² + q²) * length"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((p * q * length) / 2)}"
                            result += "\nFormula: (p × q × length) / 2"
                    case "pentagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (5 * side**2 / 4) * math.sqrt(2 * math.sqrt(5) / 5 + 1) + 5 * side * height)}"
                            result += "\nFormula: 2 * (5 * side² / 4) * √(2√5/5 + 1) + 5 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(2.5 * side ** 2 * height * math.sqrt(5 + 2 * math.sqrt(5)))}"
                            result += "\nFormula: 2.5 * side² * height * √(5 + 2√5)"
                    case "hexagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(3 * math.sqrt(3) * side**2 + 6 * side * height)}"
                            result += "\nFormula: 3√3 * side² + 6 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((3 * math.sqrt(3) / 2) * side**2 * height)}"
                            result += "\nFormula: (3√3 / 2) * side² * height"
                    case "heptagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4((7 / 2) * side**2 * math.sqrt((7 + 3 * math.sqrt(7)) / 4) + 7 * side * height)}"
                            result += "\nFormula: (7/2) * side² * √((7 + 3√7)/4) + 7 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((7 / 4) * side**2 * math.sqrt((7 + 3 * math.sqrt(7)) / 4) * height)}"
                            result += "\nFormula: (7/4) * side² * √((7 + 3√7)/4) * height"
                    case "octagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(4 * (1 + math.sqrt(2)) * side**2 + 8 * side * height)}"
                            result += "\nFormula: 4 * (1 + √2) * side² + 8 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(2 * (1 + math.sqrt(2)) * side**2 * height)}"
                            result += "\nFormula: 2 * (1 + √2) * side² * height"
                    case "nonagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4((9 / 2) * side**2 * math.sqrt((9 + 2 * math.sqrt(3) * math.sqrt(27)) / 3) + 9 * side * height)}"
                            result += "\nFormula: (9/2) * side² * √((9 + 2√3 * √27) / 3) + 9 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((9 / 4) * side**2 * math.sqrt((9 + 2 * math.sqrt(3) * math.sqrt(27)) / 3) * height)}"
                            result += "\nFormula: (9/4) * side² * √((9 + 2√3 * √27) / 3) * height"
                    case "decagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(5 * side**2 * math.sqrt(5 + 2 * math.sqrt(5)) + 10 * side * height)}"
                            result += "\nFormula: 5 * side² * √(5 + 2√5) + 10 * side * height"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((5 / 2) * side**2 * math.sqrt(5 + 2 * math.sqrt(5)) * height)}"
                            result += "\nFormula: (5/2) * side² * √(5 + 2√5) * height"

                    # pyramids
                    case "trianglePyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4((math.sqrt(3) / 4) * side**2 + (3 / 2) * side * math.sqrt((math.sqrt(3) / 6 * side)**2 + height**2))}"
                            result += "\nFormula: (√3 / 4) * side² + (3 / 2) * side * √((√3 / 6 * side)² + height²)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((math.sqrt(3) / 4) * side**2 + (3 / 2) * side * math.sqrt((math.sqrt(3) / 6 * side)**2 + height**2))}"
                            result += "\nFormula: (√3 / 12) * side² * height"
                    case "rectanglePyramid":
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(width * length + width * math.sqrt((length / 2)**2 + height**2) + length * math.sqrt((width / 2)**2 + height**2))}"
                            result += "\nFormula: width * length + width * √((length / 2)² + height²) + length * √((width / 2)² + height²)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((width * height * length) / 3)}"
                            result += "\nFormula: (width * height * length) / 3"
                    case "squarePyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(side**2 + 2 * side * math.sqrt((side / 2)**2 + height**2))}"
                            result += "\nFormula: side² + 2 * side * √((side / 2)² + height²)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(side ** 2 * height / 3)}"
                            result += "\nFormula: side² * height / 3"
                    case "pentagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4((5/4) * side**2 * math.sqrt(5 + 2 * math.sqrt(5)) + (5/2) * side * math.sqrt((side / (2 * math.tan(math.pi / 5)))**2 + height**2))}"
                            result += "\nFormula: (5/4) * side² * √(5 + 2√5) + (5/2) * side * √((side / (2 * tan(π / 5)))² + height²)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((5/12) * side**2 * math.sqrt(5 + 2 * math.sqrt(5)) * height)}"
                            result += "\nFormula: (5/12) * side² * √(5 + 2√5) * height"
                    case "hexagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4((3 * math.sqrt(3) / 2) * side**2 + 3 * side * math.sqrt((math.sqrt(3) / 2 * side)**2 + height**2))}"
                            result += "\nFormula: (3√3 / 2) * side² + 3 * side * √((√3 / 2 * side)² + height²)"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4((math.sqrt(3) / 2) * side**2 * height)}"
                            result += "\nFormula: (√3 / 2) * side² * height"

            # Pythagorean theorem calculator
            elif request.form.get('category') == 'pythagorean':
                calculation_type = request.form.get('calculation_type')
                if calculation_type == 'hypotenuse':
                    a = float(request.form['a'])
                    b = float(request.form['b'])
                    c = math.sqrt(a ** 2 + b ** 2)
                    result = f"Hypotenuse: {round_4(c)}"
                    result += "\nFormula: √(a² + b²)"
                elif calculation_type == 'side':
                    hypotenuse = float(request.form['hypotenuse'])
                    side = float(request.form['side'])
                    other_side = math.sqrt(hypotenuse ** 2 - side ** 2)
                    result = f"Other Side: {round_4(other_side)}"
                    result += "\nFormula: √(hypotenuse² - side²)"

            # ai explanation
            if request.form.get('category') == 'pythagorean':
                completion = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a helpful assistant aimed to help a user calculate the {calculation_type} of a right triangle using the Pythagorean theorem. The result is: {result}. You shall not output markdown, like **, __, ||, etc. NEVER OUTPUT ANYTHING IN **BOLD**. Never ask the user for any additional input to make your explanation complete. You shall only use the formula mentioned in the result, no additional formulas, even if you disagree. Only provide examples if they are step by step and directly related to the formula. Avoid using too many decimals."
                        },
                        {
                            "role": "user",
                            "content": f"Explain how to determine the {calculation_type} of a right triangle using the Pythagorean theorem."
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
            else:
                completion = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a helpful assistant aimed to help a user calculate the {calculation_type} of a {shape}. The result is: {result}. You shall not output markdown, like **, __, ||, etc. NEVER OUTPUT ANYTHING IN **BOLD**. Never ask the user for any additional input to make your explanation complete. You shall only use the formula mentioned in the result, no additional formulas, even if you disagree. Only provide examples if they are step by step and directly related to the formula. Avoid using too many decimals."
                        },
                        {
                            "role": "user",
                            "content": f"Explain how to determine the {calculation_type} of a {shape}."
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
            msg = completion.choices[0].message.content
            ai_explain = f"<b>AI Explanation:</b>\n{msg}"

        except Exception as e:
            result = f"Error in calculation: {e}"
            ai_explain = "<b>AI Explanation:</b>\nNot available"
        return json.dumps({'result': result, 'explain': ai_explain})

    return render_template('index.html')


@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        num_questions = int(request.form.get('num_questions'))
        difficulty = request.form.get('difficulty')
        questions = generate_quiz(num_questions, difficulty)
        session['questions'] = questions
        return render_template('quiz.html', questions=enumerate(questions))
    else:
        return render_template('quizsetup.html')

@app.route("/quiz_results", methods=['POST'])
def quiz_results():
    user_answers = request.form.to_dict()
    questions = session.get('questions', [])
    results = []
    score = 0
    for idx, question in enumerate(questions):
        qid = f"q{idx}"
        user_answer = user_answers.get(qid)
        question_text = question['question']
        correct_answer = question['correct_answer']
        formula = question['formula']
        is_correct = user_answer == correct_answer
        explanation = "Correct"
        if is_correct:
            score += 1
        if not is_correct:
            # i love ai explanation
            completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful assistant aimed to help a user solve the following question: {question_text}. The user input {user_answer}, but the correct answer is {correct_answer}. The formula used to calculate the answer is {formula}. You shall not output markdown, like **, __, ||, etc. NEVER OUTPUT ANYTHING IN **BOLD**. Never ask the user for any additional input to make your explanation complete. You shall only use the formula mentioned previously, no additional formulas, even if you disagree. Only provide examples if they are step by step and directly related to the formula. Avoid using too many decimals."
                    },
                    {
                        "role": "user",
                        "content": f"Explain how to solve the following question: {question_text}."
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None,
            )
            msg = completion.choices[0].message.content
            explanation = msg
        results.append({
            'question': question['question'],
            'options': question['options'],
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'explanation': explanation
        })
    percentage = round(score / len(questions) * 100, 1)
    return render_template('quizresults.html', results=results, score=score, total=len(questions), percentage=percentage)



if __name__ == "__main__":
    app.run(host="0.0.0.0")
