//! The Hopf map p: S^3 -> S^2, in two panes: S^3 drawn in R^3 by stereographic projection (left), and S^2 (right).
//! Click a point of S^2 and the circle over it appears; every point travels round its circle of latitude, and its
//! circle moves with it, sweeping out a torus.

use std::f32::consts::{PI, TAU};
use wgw_widget::*;

const SEGMENTS: usize = 96; // straight pieces per fibre
const FRAMES: u32 = 240; // a loop: 12 seconds round
const REACH: f32 = 3.4; // fibres are cut off this far out: over points near the south pole they reach to infinity
const MOST: usize = 10; // fibres shown at once; a click past this many replaces the oldest
const NU: usize = 64; // the sphere's mesh, in longitudes and latitudes
const NV: usize = 32;
const COLORS: [&str; 2] = ["var(--link)", "var(--accent)"];

/// A point of S^3 over (polar, longitude) on S^2, turned by `turn` around its fibre, carried to R^3.
fn fibre_point(polar: f32, longitude: f32, turn: f32) -> [f32; 3] {
    let (r1, r2) = ((polar / 2.0).cos(), (polar / 2.0).sin());
    let d = 1.0 - r2 * turn.sin();
    [r1 * (longitude + turn).cos() / d, r1 * (longitude + turn).sin() / d, r2 * turn.cos() / d]
}

fn on_sphere(polar: f32, longitude: f32) -> [f32; 3] {
    [polar.sin() * longitude.cos(), polar.sin() * longitude.sin(), polar.cos()]
}

/// Colors by where a point is: round the sphere from the link color to the accent and back, so nearby points, and
/// their fibres, look alike.
fn shade(longitude: f32) -> f32 {
    (1.0 - longitude.cos()) / 2.0
}

/// A point travelling round its circle of latitude, eastward, once over the loop like every other point, through
/// where it started at frame `start`.
struct Path {
    polar: f32,
    longitude: f32,
    start: u32,
}

impl Path {
    fn at(&self, frame: u32) -> (f32, f32) {
        (self.polar, self.longitude + TAU * (frame as f32 - self.start as f32) / FRAMES as f32)
    }
}

fn sphere() -> Layer {
    let mut vertices = Vec::new();
    for j in 0..=NV {
        for i in 0..=NU {
            vertices.push(on_sphere(PI * j as f32 / NV as f32, TAU * i as f32 / NU as f32));
        }
    }
    let mut faces = Vec::new();
    for j in 0..NV {
        for i in 0..NU {
            let a = (j * (NU + 1) + i) as u32;
            let b = a + NU as u32 + 1;
            faces.extend([[a, b, a + 1], [a + 1, b, b + 1]]);
        }
    }
    Mesh::new(vertices, faces).pane(1)
}

/// Lines of latitude and longitude on S^2, every 30 degrees, faint, so the points can be seen moving over it.
fn graticule() -> Layer {
    const N: usize = 96;
    let (mut vertices, mut segments) = (Vec::new(), Vec::new());
    let mut curve = |at: &dyn Fn(f32) -> (f32, f32)| {
        let first = vertices.len() as u32;
        for i in 0..=N {
            let (p, l) = at(i as f32 / N as f32);
            vertices.push(on_sphere(p, l).map(|c| 1.002 * c));
        }
        segments.extend((0..N as u32).map(|i| [first + i, first + i + 1]));
    };
    for lat in [-60.0f32, -30.0, 0.0, 30.0, 60.0] {
        curve(&|u| ((90.0 - lat).to_radians(), TAU * u));
    }
    for lon in [0.0f32, 30.0, 60.0, 90.0, 120.0, 150.0] {
        curve(&|u| (TAU * u, lon.to_radians())); // each a whole great circle
    }
    Lines::new(vertices).segments(segments).color("color-mix(in srgb, var(--text), var(--bg) 75%)").width(1.0).pickable(false).pane(1)
}

/// Invisible points that fix a pane's size: each pane is fitted to what's in it, so the fibres' pane stays at
/// REACH and never rescales, and S^2 takes half its pane's height.
fn frame(r: f32, pane: u32) -> Layer {
    let v = vec![[-r, 0.0, 0.0], [r, 0.0, 0.0], [0.0, -r, 0.0], [0.0, r, 0.0], [0.0, 0.0, -r], [0.0, 0.0, r]];
    Points::new(v).visible(false).pickable(false).pane(pane)
}

struct HopfMap;

impl Widget for HopfMap {
    fn new(_mesh: Option<MeshData>) -> Self {
        HopfMap
    }

    fn setup(&self) -> Setup {
        // Every click adds a point; the fibres get two thirds of the width.
        Setup::new().frames(FRAMES).fps(20.0).panes(&[2.0, 1.0]).keep_picks()
    }

    fn scene(&self, state: &State) -> Scene {
        // To start with, five points close behind one another on the equator, on the side facing the reader,
        // travelling round it together: their circles, neighbours on one torus, move as a bundle. Each click adds a
        // point exactly where it lands, setting off from there in step with the animation on screen.
        let mut paths: Vec<Path> = (0..5).map(|k| Path { polar: PI / 2.0, longitude: (-90.0 + 10.0 * k as f32).to_radians(), start: 0 }).collect();
        for pick in state.picks.iter().filter(|p| p.layer == "mesh") {
            let [x, y, z] = pick.point.unwrap_or([0.0, 0.0, 1.0]);
            let len = (x * x + y * y + z * z).sqrt().max(1e-9);
            paths.push(Path { polar: (z / len).clamp(-1.0, 1.0).acos(), longitude: y.atan2(x), start: pick.frame });
        }
        let paths = &paths[paths.len().saturating_sub(MOST)..];

        let (mut vertices, mut values, mut segments) = (Vec::new(), Vec::new(), Vec::new());
        let (mut bases, mut shades) = (Vec::new(), Vec::new());
        for path in paths {
            let (polar, longitude) = path.at(state.frame);
            let first = vertices.len() as u32;
            for i in 0..=SEGMENTS {
                let q = fibre_point(polar, longitude, TAU * i as f32 / SEGMENTS as f32);
                let far = (q[0] * q[0] + q[1] * q[1] + q[2] * q[2]).sqrt() >= REACH;
                vertices.push(if far { [f32::NAN; 3] } else { q }); // past REACH: not drawn
                values.push(shade(longitude));
            }
            segments.extend((0..SEGMENTS as u32).map(|i| [first + i, first + i + 1]));
            bases.push(on_sphere(polar, longitude));
            shades.push(shade(longitude));
        }
        Scene::new()
            .layer("mesh", sphere())
            .layer("grid", graticule())
            .layer("fibreFrame", frame(REACH, 0))
            .layer("sphereFrame", frame(2.0, 1))
            .layer("fibres", Lines::new(vertices).segments(segments).values(values).colors(&COLORS).width(2.5))
            .layer("points", Points::new(bases).values(shades).colors(&COLORS).size(9.0).pickable(false).pane(1))
    }
}

export!(HopfMap);
