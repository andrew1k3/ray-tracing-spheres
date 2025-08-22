from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QSlider, QPushButton, QSpinBox, QColorDialog, QMessageBox
)
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtGui import QPixmap, QColor
from scene import Scene
from light import Light
from vector3 import Vec3
from plane import Plane
from sphere import Sphere

class RenderThread(QThread):
    finished = Signal(Scene)

    def __init__(self, scene: Scene):
        super().__init__()
        self.scene = scene

    @Slot()
    def run(self):
        self.scene.render()
        self.finished.emit(self.scene)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raytracing Scene Renderer")
        self.thread = None
        self.worker = None

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(6)   # tighter stack

        grid = QGridLayout()

        # Name Input
        grid.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit("output")
        self.name_input.setFixedWidth(120) 
        grid.addWidget(self.name_input, 0, 1)

        # Width and Height Inputs
        grid.addWidget(QLabel("Width:"), 1, 0)
        self.width_input = QSpinBox()
        self.width_input.setRange(100, 2560)
        self.width_input.setValue(640)
        self.width_input.setFixedWidth(120)
        grid.addWidget(self.width_input, 1, 1)
        grid.addWidget(QLabel("Height:"), 1, 2)
        self.height_input = QSpinBox()
        self.height_input.setRange(100, 1440)
        self.height_input.setValue(360)
        self.height_input.setFixedWidth(120)
        grid.addWidget(self.height_input, 1, 3)
        
        # FOV Slider
        slider_label = QLabel("FOV:")
        self.fov_slider = QSlider(Qt.Horizontal)
        self.fov_slider.setRange(10, 180)
        self.fov_slider.setValue(90)
        self.fov_slider_label = QLabel("90")
        self.fov_slider.setTickPosition(QSlider.TicksBelow)
        self.fov_slider.setTickInterval(10)
        self.fov_slider.valueChanged.connect(lambda v: self.fov_slider_label.setText(str(v)))
        grid.addWidget(slider_label, 2, 0)
        grid.addWidget(self.fov_slider, 2, 1)
        grid.addWidget(self.fov_slider_label, 2, 2)


        # Render Button
        self.render_button = QPushButton("Render")
        self.render_button.clicked.connect(self.render_scene)
        self.render_button.setEnabled(True)
        grid.addWidget(self.render_button, 4, 0)

        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        root.addWidget(grid_widget, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Show image
        self.image_label = QLabel()
        root.addWidget(self.image_label, alignment=Qt.AlignCenter)



    def render_scene(self):
        print("Rendering scene..."
              f" Name: {self.name_input.text()}, "
              f"Width: {self.width_input.value()}, "
              f"Height: {self.height_input.value()}, "
              f"FOV: {self.fov_slider.value()}")
        
        self.render_button.setEnabled(False)

        scene = Scene(
            width=self.width_input.value(),
            height=self.height_input.value(),
            fov=self.fov_slider.value(),
            background=Vec3(27, 125, 171),
            name=self.name_input.text()
        )

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

        self.thread = QThread(self)
        self.worker = RenderThread(scene)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_render_finished)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_render_finished(self, scene: Scene):
        self.render_button.setEnabled(True)
        self.thread.quit()
        self.thread.wait()
        print(f"Rendering complete! Output saved as assets/{scene.name}.png")

        self.pixmap = QPixmap(f"./assets/{scene.name}.png")
        self.pixmap = self.pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setMaximumSize(400, 300)

    



