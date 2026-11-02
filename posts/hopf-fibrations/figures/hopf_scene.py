"""A point looping over S^2 and its fibre under the Hopf map, animated with Manim. Writes HopfMap.gif next to this file."""
import subprocess
import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # the project root, where palette.py is
from palette import ACCENT, INK, PAPER, PRIMARY, SURFACE

config.background_color = PAPER
config.pixel_width, config.pixel_height = 1280, 560
config.frame_height = config.frame_width * 7 / 16
config.frame_rate = 15
config.video_dir = str(Path(__file__).parent)
config.partial_movie_dir = "media/partial_movie_files/{scene_name}"
config.disable_caching = True  # hashing thousands of fibre segments takes longer than rendering them

FIBRE_AT = np.array([-3.5, -0.1, 0.0])
FIBRE_SCALE = 0.8
FIBRE_ELEV = np.radians(50)
FIBRE_AZIMUTH = PI
SPHERE_AT = np.array([4.0, 0.0, 0.0])
SPHERE_RADIUS = 2.0
ELEV = np.radians(28)
CAMERA_DISTANCE = 9.0

# The point spirals down the sphere and back up, closing the loop. It stays away from the south pole,
# whose fibre runs off to infinity.
POLAR_TOP, POLAR_BOTTOM = 0.12 * PI, 0.6 * PI
LONGITUDE_START = PI / 2
SPIRAL_TURNS = 3  # a whole number, so that the path closes up
LOOP_SECONDS = 18
FIBRES = 48  # how many fibres stay behind on the way around the loop
TAIL = 0.5  # the fraction of the loop it takes for what the point leaves behind to fade away
SEGMENTS = 96  # how many straight pieces each fibre is drawn with
TRAIL_PIECES = 400



def hopf(z1, z2):
    """The Hopf map, as a point of S^2 inside C x R = R^3."""
    w = 2 * z1 * np.conj(z2)
    return np.array([w.real, w.imag, abs(z1) ** 2 - abs(z2) ** 2]).T


def spiral(progress):
    """The moving point's polar angle and longitude on S^2. Progress 0 and 1 are the same point."""
    middle, reach = (POLAR_TOP + POLAR_BOTTOM) / 2, (POLAR_BOTTOM - POLAR_TOP) / 2
    return middle - reach * np.cos(TAU * progress), LONGITUDE_START + progress * SPIRAL_TURNS * TAU


def lift(polar, longitude, turn=0.0):
    """A point of S^3 over the given point of S^2. Changing `turn` moves it around the fibre."""
    phase = np.exp(1j * turn)
    return phase * np.cos(polar / 2) * np.exp(1j * longitude), phase * np.sin(polar / 2)


def stereographic(z1, z2):
    """S^3 minus the point (0, i), carried to R^3."""
    return np.array([z1.real, z1.imag, z2.real]).T / (1 - z2.imag)[..., None]


def view(points, elev):
    """Tilt points towards the viewer, returning their (x, y) on screen and their depth, positive being away."""
    x, y, z = points.T
    return np.array([x, y * np.sin(elev) + z * np.cos(elev)]).T, y * np.cos(elev) - z * np.sin(elev)


def on_screen(flat, at, scale):
    return at + scale * np.column_stack([flat, np.zeros(len(flat))])


def fibre_view(points):
    """Where points of R^3 land in the left panel, in perspective, with their depths."""
    x, y, z = points.T
    turned = np.array([x * np.cos(FIBRE_AZIMUTH) - y * np.sin(FIBRE_AZIMUTH), x * np.sin(FIBRE_AZIMUTH) + y * np.cos(FIBRE_AZIMUTH), z]).T
    flat, depth = view(turned, FIBRE_ELEV)
    return on_screen(flat * (CAMERA_DISTANCE / (CAMERA_DISTANCE + depth))[:, None], FIBRE_AT, FIBRE_SCALE), depth


def sphere_view(points):
    """Where points of S^2 land in the right panel, with their depths."""
    flat, depth = view(points, ELEV)
    return on_screen(flat, SPHERE_AT, SPHERE_RADIUS), depth


def spiral_color(progress):
    """Teal near the top of the path and orange near the bottom."""
    blend = (spiral(progress)[0] - POLAR_TOP) / (POLAR_BOTTOM - POLAR_TOP)
    return interpolate_color(ManimColor(PRIMARY), ManimColor(ACCENT), blend)


def fading(now, then):
    """How visible something left behind at progress `then` is at progress `now`, going around the loop."""
    return max(0.0, 1 - ((now - then) % 1) / TAIL)


def line(start, end, color, width, opacity=1.0):
    return VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity).set_points_as_corners([start, end])


def fibre_pieces(progress, width=1.6):
    """The fibre over the moving point at `progress`, as (depth, halo, line) for drawing back to front."""
    turns = np.linspace(0, TAU, SEGMENTS + 1)
    points, depth = fibre_view(stereographic(*lift(*spiral(progress), turns)))
    color = spiral_color(progress)
    return [((depth[i] + depth[i + 1]) / 2,
             line(points[i], points[i + 1], PAPER, width + 2.2),  # a gap in the far strand shows which one passes in front
             line(points[i], points[i + 1], color, width).set_cap_style(CapStyleType.ROUND))  # hides the seams between pieces
            for i in range(SEGMENTS)]


def sphere():
    """S^2 with its near side's lines of latitude and longitude."""
    grid = VGroup()
    angles = np.linspace(0, TAU, 73)
    curves = [np.column_stack([np.cos(a) * np.cos(angles), np.cos(a) * np.sin(angles), np.full_like(angles, np.sin(a))])
              for a in np.radians((-60, -30, 0, 30, 60))]
    curves += [np.column_stack([np.cos(angles) * np.cos(a), np.cos(angles) * np.sin(a), np.sin(angles)])
               for a in np.radians((0, 45, 90, 135))]
    for curve in curves:
        points, depth = sphere_view(curve)
        grid.add(*[line(points[i], points[i + 1], INK, 0.8, 0.25) for i in range(72) if depth[i] + depth[i + 1] < 0])
    disk = Circle(SPHERE_RADIUS, stroke_color=INK, stroke_width=1.5, fill_color=SURFACE, fill_opacity=1).move_to(SPHERE_AT)
    return VGroup(disk, grid)


def spiral_trail():
    """The moving point's path as short pieces with their full opacities, fainter behind the sphere."""
    progress = np.linspace(0, 1, TRAIL_PIECES + 1)
    points, depth = sphere_view(hopf(*lift(*spiral(progress))))
    return [(line(points[i], points[i + 1], spiral_color(progress[i]), 2.5), 1 if depth[i] < 0 else 0.3)
            for i in range(TRAIL_PIECES)]


class HopfMap(Scene):
    def render(self, preview=False):
        """Render as usual, then swap the movie for a GIF. Manim's own GIF output is about 70 times larger."""
        result = super().render(preview)
        movie = Path(self.renderer.file_writer.movie_file_path)
        palette = "split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=none:diff_mode=rectangle"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(movie), "-filter_complex", palette,
                        str(Path(__file__).parent / "HopfMap.gif")], check=True)
        movie.unlink()
        return result

    def construct(self):
        progress = ValueTracker(0)
        strands = [fibre_pieces(index / FIBRES) for index in range(FIBRES)]
        trail_pieces = spiral_trail()

        def update_fibres(fibres):
            now = progress.get_value()
            pieces = fibre_pieces(now, width=3.2)
            for index, strand in enumerate(strands):
                opacity = fading(now, index / FIBRES)
                if opacity > 0:
                    for _, halo, stroke in strand:
                        halo.set_stroke(opacity=opacity)
                        stroke.set_stroke(opacity=opacity)
                    pieces += strand
            pieces.sort(key=lambda piece: piece[0], reverse=True)
            fibres.submobjects = [part for _, halo, stroke in pieces for part in (halo, stroke)]

        def update_trail(trail):
            now = progress.get_value()
            shown = []
            for index, (piece, full) in enumerate(trail_pieces):
                opacity = fading(now, index / TRAIL_PIECES)
                if opacity > 0:
                    shown.append(piece.set_stroke(opacity=full * opacity))
            trail.submobjects = shown

        def update_image(dot):
            # The dot is computed by applying the map to a point of the fibre.
            position, depth = sphere_view(np.atleast_2d(hopf(*lift(*spiral(progress.get_value())))))
            dot.move_to(position[0]).set_fill(spiral_color(progress.get_value()), opacity=1 if depth[0] < 0 else 0.45)

        # These two groups start empty: Manim would keep drawing whatever they hold when play() starts, on every frame.
        self.add(sphere(), VGroup().add_updater(update_trail))
        self.add(VGroup().add_updater(update_fibres))
        arrow = CurvedArrow([-0.55, 0.0, 0], [1.6, 0.0, 0], angle=-0.35, color=INK, stroke_width=2.5, tip_length=0.2)
        self.add(arrow)
        self.add(Dot(radius=0.1, stroke_color=INK, stroke_width=1.5).add_updater(update_image, call_updater=True))
        self.play(progress.animate.set_value(1), run_time=LOOP_SECONDS, rate_func=linear)
