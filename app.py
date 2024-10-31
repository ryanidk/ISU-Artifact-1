from flask import Flask, request, render_template
import math
from groq import Groq
import os
import json

# Flask app setup
app = Flask(__name__)
groq_api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=groq_api_key)


def round_4(value):
    if value.is_integer():
        return f"{int(value)}"
    elif len(f"{value}".split('.')[1]) <= 4:
        return f"{value}"
    else:
        return f"~{value:.4f}"


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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
