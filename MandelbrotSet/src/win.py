from typing import Tuple, Optional
from matplotlib import cm
from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
from .calc import mandelbrot, fc, initialize_grid, ComplexArrayFunction

class MandelbrotWindow:
    def __init__(self,
                 size: Tuple[int, int],
                 aabb: Tuple[int, int, int, int],
                 overflow_limit: float,
                 max_iter: float,
                 func: Optional[ComplexArrayFunction] = None
                 ) -> None:
        self.size = size
        self.init_aabb = aabb
        self.aabb = aabb
        self.overflow_limit = overflow_limit
        self.max_iter = max_iter
        self.func = func if func is not None else fc

        # Initialize Tkinter
        self.root = tk.Tk()
        self.root.title("Mandelbrot Set")
        self.root.geometry(f"{size[0]}x{size[1]}")

        self.canvas = tk.Canvas(self.root, width=size[0], height=size[1])
        self.canvas.pack()

        # Bind mouse events
        self._bind_events()

        self.rect = None
        self.start_x = self.start_y = 0

        # Draw the initial Mandelbrot set
        self._draw_mandelbrot()

    def _bind_events(self):
        """Bind mouse events to the canvas."""
        self.canvas.bind("<ButtonPress-1>", self._on_button_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_button_release)

    def _on_button_press(self, event):
        """Handle mouse button press."""
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red'
        )

    def _on_mouse_drag(self, event):
        """Handle mouse drag to update rectangle."""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def _on_button_release(self, event):
        """Handle mouse button release to update the zoomed region."""
        self.canvas.delete(self.rect)
        self.rect = None

        # Normalize rectangle coordinates
        end_x, end_y = event.x, event.y
        left, right = sorted((self.start_x, end_x))
        top, bottom = sorted((self.start_y, end_y))

        # Adjust the rectangle to maintain the aspect ratio
        left, right, top, bottom = self._adjust_aspect_ratio(left, right, top, bottom)

        # Map the rectangle coordinates to the AABB
        self._update_aabb(left, right, top, bottom)
        self._draw_mandelbrot()

    def _adjust_aspect_ratio(self, left, right, top, bottom):
        """Adjust the rectangle to maintain the aspect ratio of the canvas."""
        canvas_aspect_ratio = self.size[0] / self.size[1]
        rect_width = right - left
        rect_height = bottom - top
        rect_aspect_ratio = rect_width / rect_height

        if rect_aspect_ratio > canvas_aspect_ratio:
            # Add vertical padding
            target_height = rect_width / canvas_aspect_ratio
            padding = (target_height - rect_height) / 2
            top -= padding
            bottom += padding
        else:
            # Add horizontal padding
            target_width = rect_height * canvas_aspect_ratio
            padding = (target_width - rect_width) / 2
            left -= padding
            right += padding

        # Clamp to canvas bounds
        left = max(0, min(left, self.size[0]))
        right = max(0, min(right, self.size[0]))
        top = max(0, min(top, self.size[1]))
        bottom = max(0, min(bottom, self.size[1]))

        return left, right, top, bottom

    def _update_aabb(self, left, right, top, bottom):
        """Update the axis-aligned bounding box based on the selection."""
        x_range = self.aabb[1] - self.aabb[0]
        y_range = self.aabb[3] - self.aabb[2]

        self.aabb = (
            self.aabb[0] + x_range * left / self.size[0],   # New left boundary
            self.aabb[0] + x_range * right / self.size[0],  # New right boundary
            self.aabb[2] + y_range * (self.size[1] - bottom) / self.size[1],  # New bottom boundary
            self.aabb[2] + y_range * (self.size[1] - top) / self.size[1],     # New top boundary
        )

    def _draw_mandelbrot(self):
        """Draw the Mandelbrot set on the canvas with a 'hot' colormap."""
        # Generate the grid and calculate the Mandelbrot set
        grid = initialize_grid(self.size, *self.aabb)
        raw_img = mandelbrot(grid, self.max_iter, self.overflow_limit, self.func, use_tqdm=True)

        # print min max value to know what's currently dispayed
        min_complexe = grid.imag.min()
        max_complexe = grid.imag.max()
        min_real = grid.real.min()
        max_real = grid.real.max()
        print(f"{min_real=}, {max_real=}, {min_complexe=}, {max_complexe=}")

        # Normalize the raw_img values to [0, 1] for colormap application
        normalized_img = raw_img / self.max_iter

        # Apply the 'hot' colormap
        colormap = cm.get_cmap('hot')
        colored_img = colormap(normalized_img)  # This gives an RGBA array

        # Convert to an 8-bit RGB image
        img = (colored_img[:, :, :3] * 255).astype(np.uint8)
        img = Image.fromarray(img)

        # Update the canvas with the new image
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
