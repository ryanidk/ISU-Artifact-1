# ISU Artifact 1 - Shape Calculator

### [Access the website here](https://isu-artifact-1.ryanidk.com/)

This code is for my first ISU artifact, focusing on volume relationships, measurement calculations in three dimensions, and the effects of changing dimensions. This website functions mainly as a calculator with an AI-powered explainer for various shapes, including 2D and 3D figures and a Pythagorean theorem calculator for right triangles. The 2D calculators find both the area and perimeter (or circumference for circles), while the 3D calculators find the surface area and volume of the shapes. The Pythagorean theorem calculator finds the hypotenuse and an unknown side of the triangle.

The website also features a multiple-choice quiz which allows users to choose their quiz length and difficulty level. Questions are based on volume and area calculations, including working backwards (but does not include surface area or perimeter as they require more data). At the end, the user can review their results, and for any incorrect answers, they can receive AI-generated explanations on how to solve the questions.

This project is built with Python and Flask for the backend, with a HTML/CSS/JS frontend. It is run using Gunicorn on a free Oracle Cloud Ampere A1 instance. The AI functions are powered by Llama 3.1 8B, running on Groq cloud.