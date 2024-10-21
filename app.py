from flask import Flask, request, render_template
import math

# Flask app setup
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            shape = request.form.get('shape')
            calculation_type = request.form.get('calculation_type')

            # 2d shapes
            if request.form.get('category') == '2d':
                match shape:
                    case "circle":
                        radius = float(request.form['radius'])
                        if calculation_type == 'area':
                            result = f"Area: {math.pi * radius ** 2:.4f}"
                        elif calculation_type == 'perimeter':
                            result = f"Circumference: {2 * math.pi * radius:.4f}"
                    case "triangle":
                        if calculation_type == 'area':
                            base = float(request.form['base'])
                            height = float(request.form['height'])
                            result = f"Area: {0.5 * base * height:.4f}"
                        elif calculation_type == 'perimeter':
                            side1 = float(request.form['side1'])
                            side2 = float(request.form['side2'])
                            side3 = float(request.form['side3'])
                            result = f"Perimeter: {side1 + side2 + side3:.4f}"
                    case "rectangle":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        if calculation_type == 'area':
                            result = f"Area: {length * width:.4f}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {2 * (length + width):.4f}"
                    case "square":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Area: {side ** 2:.4f}"
                        elif calculation_type == 'perimeter':
                            result = f"Perimeter: {4 * side:.4f}"
                    case "trapezium":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {0.5 * (a + b) * height:.4f}"
                        elif calculation_type == 'perimeter':
                            c = float(request.form['c'])
                            d = float(request.form['d'])
                            result = f"Perimeter: {a + b + c + d:.4f}"
                    case "parallelogram":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Area: {base * height:.4f}"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {2 * (base + side):.4f}"
                    case "rhombus":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {0.5 * p * q:.4f}"
                        elif calculation_type == 'perimeter':
                            side = float(request.form['side'])
                            result = f"Perimeter: {4 * side:.4f}"
                    case "kite":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        if calculation_type == 'area':
                            result = f"Area: {0.5 * p * q:.4f}"
                        elif calculation_type == 'perimeter':
                            a = float(request.form['a'])
                            b = float(request.form['b'])
                            result = f"Perimeter: {2 * (a + b):.4f}"
                    case "pentagon":
                        side = float(request.form['side'])
                        result = f"Area: {0.25 * math.sqrt(5 * (5 + 2 * math.sqrt(5))) * side ** 2:.4f}\nPerimeter: {5 * side:.4f}"
                    case "hexagon":
                        side = float(request.form['side'])
                        result = f"Area: {1.5 * math.sqrt(3) * side ** 2:.4f}\nPerimeter: {6 * side:.4f}"
                    case "heptagon":
                        side = float(request.form['side'])
                        result = f"Area: {0.5 * 7 * side * math.sqrt(3 + 2 * math.sqrt(5)):.4f}\nPerimeter: {7 * side:.4f}"
                    case "octagon":
                        side = float(request.form['side'])
                        result = f"Area: {2 * (1 + math.sqrt(2)) * side ** 2:.4f}\nPerimeter: {8 * side:.4f}"
                    case "nonagon":
                        side = float(request.form['side'])
                        result = f"Area: {0.5 * 9 * side * math.sqrt(4 - 2 * math.sqrt(3)):.4f}\nPerimeter: {9 * side:.4f}"
                    case "decagon":
                        side = float(request.form['side'])
                        result = f"Area: {2.5 * side ** 2 * math.sqrt(5 + 2 * math.sqrt(5)):.4f}\nPerimeter: {10 * side:.4f}"

            # 3d shapes
            elif request.form.get('category') == '3d':
                match shape:
                    case "cube":
                        side = float(request.form['side'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {6 * side ** 2:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {side ** 3:.4f}"
                    case "cylinder":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {2 * math.pi * radius * (radius + height):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {math.pi * radius ** 2 * height:.4f}"
                    case "cone":
                        radius = float(request.form['radius'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {math.pi * radius * (radius + math.sqrt(radius ** 2 + height ** 2)):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {math.pi * radius ** 2 * height / 3:.4f}"
                    case "trianglePrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {base * height + 3 * base * length:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {base * height * length:.4f}"
                    case "trapeziumPrism":
                        a = float(request.form['a'])
                        b = float(request.form['b'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {2 * (0.5 * (a + b) * height + a * length + b * length):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {0.5 * (a + b) * height * length:.4f}"
                    case "parallelogramPrism":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {2 * (base * height + base * length):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {base * height * length:.4f}"
                    case "rectanglePrism":
                        length = float(request.form['length'])
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {2 * (length * width + length * height + width * height):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {length * width * height:.4f}"
                    case "rhombusPrism":
                        p = float(request.form['p'])
                        q = float(request.form['q'])
                        h = float(request.form['h'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {2 * (p * q + p * length + q * length):.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {p * q * h:.4f}"
                    case "pentagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {5 * side ** 2 + 5 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {2.5 * side ** 2 * height * math.sqrt(5 + 2 * math.sqrt(5)):.4f}"
                    case "hexagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {6 * side ** 2 + 6 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {3 * side ** 2 * height * math.sqrt(3):.4f}"
                    case "heptagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {7 * side ** 2 + 7 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {3.5 * side ** 2 * height * math.sqrt(3 + 2 * math.sqrt(5)):.4f}"
                    case "octagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {8 * side ** 2 + 8 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {4 * side ** 2 * height * math.sqrt(2 + math.sqrt(2)):.4f}"
                    case "nonagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {9 * side ** 2 + 9 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {4.5 * side ** 2 * height * math.sqrt(4 - 2 * math.sqrt(3)):.4f}"
                    case "decagonPrism":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {10 * side ** 2 + 10 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {5 * side ** 2 * height * math.sqrt(5 + 2 * math.sqrt(5)):.4f}"

                    # pyramids
                    case "trianglePyramid":
                        base = float(request.form['base'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {base * height + 3 * 0.5 * base * length:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {0.5 * base * height * length / 3:.4f}"
                    case "rectanglePyramid":
                        width = float(request.form['width'])
                        height = float(request.form['height'])
                        length = float(request.form['length'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {width * height + 2 * 0.5 * width * length:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {width * height * length / 3:.4f}"
                    case "squarePyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {side ** 2 + 2 * 0.5 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {side ** 2 * height / 3:.4f}"
                    case "pentagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {5 * side ** 2 + 5 * 0.5 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {5 * side ** 2 * height / 3:.4f}"
                    case "hexagonPyramid":
                        side = float(request.form['side'])
                        height = float(request.form['height'])
                        if calculation_type == 'area':
                            result = f"Surface Area: {6 * side ** 2 + 6 * 0.5 * side * height:.4f}"
                        elif calculation_type == 'volume':
                            result = f"Volume: {6 * side ** 2 * height / 3:.4f}"

            # pythagorean theorem calculator
            elif request.form.get('category') == 'pythagorean':
                calculation_type = request.form.get('calculation_type')
                if calculation_type == 'hypotenuse':
                    a = float(request.form['a'])
                    b = float(request.form['b'])
                    c = math.sqrt(a ** 2 + b ** 2)
                    result = f"Hypotenuse: {c:.4f}"
                elif calculation_type == 'side':
                    hypotenuse = float(request.form['hypotenuse'])
                    side = float(request.form['side'])
                    other_side = math.sqrt(hypotenuse ** 2 - side ** 2)
                    result = f"Other Side: {other_side:.4f}"

        except Exception as e:
            result = f"Error in calculation: {e}"

    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)