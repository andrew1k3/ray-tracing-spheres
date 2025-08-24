from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QSlider, QPushButton, QSpinBox, QColorDialog, QMessageBox, QComboBox, QCheckBox, QRadioButton, QGroupBox, QFormLayout, QFileDialog, QListWidget, QListWidgetItem
)
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt
from PySide6.QtGui import QPixmap, QColor
from scene import Scene
from light import Light
from vector3 import Vec3
from plane import Plane
from sphere import Sphere

colors = [
    Vec3(0.96, 0.40, 0.10),  # red
    Vec3(0.97, 0.58, 0.11),  # orange
    Vec3(0.97, 0.97, 0.46),  # yellow
    Vec3(0.64, 0.85, 0.31),  # green
    Vec3(0.05, 0.67, 0.93),  # blue
    Vec3(0.58, 0.39, 0.93),  # purple
]

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
        
        self.spheres_to_color = dict()

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(6)   # tighter stack

        grid = QGridLayout()

        # Name Input
        grid.addWidget(QLabel("Name:"), 0, 0)
        self.name_input = QLineEdit("output")
        self.name_input.setFixedWidth(100) 
        grid.addWidget(self.name_input, 0, 1)

        # Width and Height Inputs
        grid.addWidget(QLabel("Width:"), 1, 0)
        self.width_input = QSpinBox()
        self.width_input.setRange(1, 5000)
        self.width_input.setValue(640)
        self.width_input.setFixedWidth(100)
        grid.addWidget(self.width_input, 1, 1)
        grid.addWidget(QLabel("Height:"), 1, 2)
        self.height_input = QSpinBox()
        self.height_input.setRange(1, 5000)
        self.height_input.setValue(360)
        self.height_input.setFixedWidth(100)
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

        grid_widget = QWidget()
        grid_widget.setLayout(grid)
        root.addWidget(grid_widget, alignment=Qt.AlignTop | Qt.AlignLeft)

        # background color picker
        picker_label = QLabel("Background:")
        self.picker = QComboBox()
        self.picker.addItems(["🔴", "🟠", "🟡", "🟢", "🔵", "🟣"])
        self.picker.setCurrentIndex(4)
        self.picker.setFixedWidth(60)
        grid.addWidget(picker_label, 3, 0)
        grid.addWidget(self.picker, 3, 1)

        # platform checkbox
        self.platform_checkbox = QCheckBox("Add Platform")
        self.platform_checkbox.setChecked(True)
        grid.addWidget(self.platform_checkbox, 4, 0, 1, 2)

        # sphere placer grid
        self.sphere_placer = QGridLayout()
        self.sphere_placer.setHorizontalSpacing(0)
        self.sphere_placer.setVerticalSpacing(0)
        self.sphere_placer.setContentsMargins(0, 0, 0, 0)
        for i in range(9):
            for j in range(9):
                combo = QComboBox()
                combo.addItems([" ", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣"])
                combo.setCurrentIndex(0)
                combo.setFixedSize(40, 40)

                def update_spheres(x, y, idx):
                    if idx == 0 and (x, y) in self.spheres_to_color:
                        del self.spheres_to_color[(x, y)]
                        return
                    self.spheres_to_color[(x, y)] = colors[idx-1]

                combo.currentIndexChanged.connect(lambda idx, x=i, y=j: update_spheres(x-4, y-4, idx))
                self.sphere_placer.addWidget(combo, i, j)
        root.addLayout(self.sphere_placer)

        # Render Button
        self.render_button = QPushButton("Render")
        self.render_button.clicked.connect(self.render_scene)
        self.render_button.setEnabled(True)
        root.addWidget(self.render_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Show image
        self.image_label = QLabel()
        root.addWidget(self.image_label, alignment=Qt.AlignCenter)

        pass

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
            background=colors[self.picker.currentIndex()]*255,
            name=self.name_input.text()
        )

        if self.platform_checkbox.isChecked():
            # platform
            scene.add(Sphere(Vec3(0, -1004, -10), 1000, Vec3(0.62, 0.71, 0.28), Vec3(0, 0, 0)))

        # camera light
        scene.add(Light(Vec3(0, 2, 1), 0.1, 1))
        
        # sun light
        scene.add(Light(Vec3(0, 1000, -10), 1, 1))

        # spheres
        for (x, y), color in self.spheres_to_color.items():
            scene.add(Sphere(Vec3(y * 2, -x * 2, -10), 1, color, Vec3(0, 0, 0)))


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

    



