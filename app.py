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
                        elif calculation_type == 'perimeter':
                            result = f"Circumference: {round_4(2 * math.pi * radius)}"
                    case "triangle":
                        if calculation_type == 'area':
                            base = float(request.form['base'])
                            height = float(request.form['height'])
                            result = f"Area: {round_4(0.5 * base * height)}"
                        elif calculation_type == 'perimeter':
                            side1 = float(request.form['side1'])
                            side2 = float(request.form['side2'])
                            side3 = float(request.form['side3'])
                            result = f"Perimeter: {round_4(side1 + side2 + side3)}"
                    case "rectangle":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(length * width)}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(2 * (length + width))}"
                    case "square":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(side ** 2)}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(4 * side)}"
                    case "trapezium":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * (a + b) * height)}"
                        elif calculation_type == 'perimeter':
                            c = float(request.form['c'])
                            d = float(request.form['d'])
                            result = f"Perimeter: {round_4(a + b + c + d)}"
                    case "parallelogram":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(base * height)}"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {round_4(2 * (base + side))}"
                    case "rhombus":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * p * q)}"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {round_4(4 * side)}"
                    case "kite":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * p * q)}"
                        elif calculation_type == 'perimeter':
                            a = float(request.form['a'])
                            b = float(request.form['b'])
                            result = f"Perimeter: {round_4(2 * (a + b))}"
                    case "pentagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.25 * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2)}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(5 * side)}"
                    case "hexagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(1.5 * math.sqrt(3) * side ** 2)}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(6 * side)}"
                    case "heptagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * 7 * side * math.sqrt(3 + 2 * math.sqrt(5)))}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(7 * side)}"
                    case "octagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(2 * (1 + math.sqrt(2)) * side ** 2)}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(8 * side)}"
                    case "nonagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(0.5 * 9 * side * math.sqrt(4 - 2 * math.sqrt(3)))}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(9 * side)}"
                    case "decagon":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {round_4(2.5 * side ** 2 * math.sqrt(5 + 2 * math.sqrt(5)))}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {round_4(10 * side)}"

            # 3D shapes
            elif request.form.get('category') == '3d':
                match shape:
                    case "cube":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(6 * side ** 2)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(side ** 3)}"
                    case "cylinder":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * math.pi * radius * (radius + height))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(math.pi * radius ** 2 * height)}"
                    case "cone":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(math.pi * radius * (radius + math.sqrt(radius ** 2 + height ** 2)))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(math.pi * radius ** 2 * height / 3)}"
                    case "trianglePrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(base * height + 3 * base * length)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(base * height * length)}"
                    case "trapeziumPrism":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (0.5 * (a + b) * height + a * length + b * length))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(0.5 * (a + b) * height * length)}"
                    case "parallelogramPrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (base * height + base * length))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(base * height * length)}"
                    case "rectanglePrism":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (length * width + length * height + width * height))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(length * width * height)}"
                    case "rhombusPrism":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        h = float(request.form['h'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(2 * (p * q + p * length + q * length))}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(p * q * h)}"
                    case "pentagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(5 * side ** 2 + 5 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(2.5 * side ** 2 * height * math.sqrt(5 + 2 * math.sqrt(5)))}"
                    case "hexagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(6 * side ** 2 + 6 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(3 * side ** 2 * height * math.sqrt(3))}"
                    case "heptagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(7 * side ** 2 + 7 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(3.5 * side ** 2 * height * math.sqrt(3 + 2 * math.sqrt(5)))}"
                    case "octagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(8 * side ** 2 + 8 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(4 * side ** 2 * height * math.sqrt(2 + math.sqrt(2)))}"
                    case "nonagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(9 * side ** 2 + 9 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(4.5 * side ** 2 * height * math.sqrt(4 - 2 * math.sqrt(3)))}"
                    case "decagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(10 * side ** 2 + 10 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(5 * side ** 2 * height * math.sqrt(5 + 2 * math.sqrt(5)))}"

                    # pyramids
                    case "trianglePyramid":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(base * height + 3 * 0.5 * base * length)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(0.5 * base * height * length / 3)}"
                    case "rectanglePyramid":
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(width * height + 2 * 0.5 * width * length)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(width * height * length / 3)}"
                    case "squarePyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(side ** 2 + 2 * 0.5 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(side ** 2 * height / 3)}"
                    case "pentagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(5 * side ** 2 + 5 * 0.5 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(5 * side ** 2 * height / 3)}"
                    case "hexagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {round_4(6 * side ** 2 + 6 * 0.5 * side * height)}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {round_4(6 * side ** 2 * height / 3)}"

            # Pythagorean theorem calculator
            elif request.form.get('category') == 'pythagorean':
                calculation_type = request.form.get('calculation_type')
                if calculation_type == 'hypotenuse':
                    a = float(request.form['a'])
                    b = float(request.form['b'])
                    c = math.sqrt(a ** 2 + b ** 2)
                    result = f"Hypotenuse: {round_4(c)}"
                elif calculation_type == 'side':
                    hypotenuse = float(request.form['hypotenuse'])
                    side = float(request.form['side'])
                    other_side = math.sqrt(hypotenuse ** 2 - side ** 2)
                    result = f"Other Side: {round_4(other_side)}"

            # ai explanation
            if request.form.get('category') == 'pythagorean':
                completion = groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": f"You are a helpful assistant aimed to help a user calculate the {calculation_type} of a right triangle using the Pythagorean theorem. You shall not output markdown, like **, __, ||, etc. NEVER OUTPUT ANYTHING IN **BOLD**. Never ask the user for any additional input to make your explanation complete."
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
                            "content": f"You are a helpful assistant aimed to help a user calculate the {calculation_type} of a {shape}. You shall not output markdown, like **, __, ||, etc. NEVER OUTPUT ANYTHING IN **BOLD**. Never ask the user for any additional input to make your explanation complete."
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
