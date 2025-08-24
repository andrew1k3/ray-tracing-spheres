from scene import Scene
from vector3 import Vec3
from light import Light
from sphere import Sphere
from gui import MainWindow
from PySide6.QtWidgets import (    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QSlider, QPushButton)
from PySide6.QtCore import Qt
import argparse

def console_input() -> Scene:
    width = input("Enter width: ")
    if width == "":
        width = 640 
        height = 360
        fov = 80
    else:
        height = input("Enter height: ")
        fov = input("Enter FOV: ")

    # scene
    scene = Scene(int(width), int(height), int(fov), Vec3(27, 125, 171))
    
    # # platform
    scene.add(Sphere(Vec3(0, -1004, -10), 1000, Vec3(0.62, 0.71, 0.28), Vec3(0, 0, 0)))

    # # plane
    # scene.add(Plane(Vec3(0, -10, 0), Vec3(0, 1, 0), Vec3(0.62, 0.71, 0.28)))

    # # lights
    # scene.add(Sphere(Vec3(0, 2, 1), 0.1, Vec3(1, 1, 1),  Vec3(0.25, 0.25, 0.25)))
    # scene.add(Sphere(Vec3(0, -2, 1), 0.1, Vec3(1, 1, 1), Vec3(0.25, 0.25, 0.25)))
    # scene.add(Sphere(Vec3(2, 0, 1), 0.1, Vec3(1, 1, 1),  Vec3(0.25, 0.25, 0.25)))
    # scene.add(Sphere(Vec3(-2, 0, 1), 0.1, Vec3(1, 1, 1), Vec3(0.25, 0.25, 0.25)))
    
    # camera light
    scene.add(Light(Vec3(0, 2, 1), 0.1, 1))
    
    # sun light
    scene.add(Light(Vec3(0, 1000, -10), 1, 1))

    # spheres
    scene.add(Sphere(Vec3(-0.35, 0.75, -10), 1, Vec3(0.96, 0.40, 0.10), Vec3(0, 0, 0)))
    scene.add(Sphere(Vec3(0.615, 0.25, -10), 1, Vec3(0.64, 0.85, 0.31), Vec3(0, 0, 0)))
    scene.add(Sphere(Vec3(-1, -0.5, -10), 1, Vec3(0.05, 0.67, 0.93), Vec3(0, 0, 0)))
    scene.add(Sphere(Vec3(0, -1, -10), 1, Vec3(0.97, 0.97, 0.46), Vec3(0, 0, 0)))

    # # clouds
    # scene.add(Sphere(Vec3(5, 10, -20), 6, Vec3(0.62, 0.71, 0.28), Vec3(0, 0, 0)))

    return scene

def gui_input() -> Scene:
    app = QApplication([])
    window = MainWindow()
    window.setFixedWidth(400)
    window.show()
    exit(app.exec())


def main():
    parser = argparse.ArgumentParser(description="Raytracing Scene Renderer")
    parser.add_argument("--console", "-c", action="store_true", help="Run in console mode")
    
    args = parser.parse_args()
    if args.console:
        scene = console_input()
        scene.render()
    else:
        gui_input()

    print("Rendering complete!")

if __name__ == "__main__":
    main()