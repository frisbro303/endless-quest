//! Two bundles over the circle with interval fibres: the cylinder (left), a product globally, and the Möbius band
//! (right), a product only locally. The slider grows the fibres out of the base circles.

use std::f32::consts::TAU;
use wgw_widget::*;

const RADIUS: f32 = 1.6; // of the base circles
const HALF: f32 = 0.8; // half a fibre's length: the interval [-1, 1], scaled
const LEFT: f32 = -2.35; // where the two circles are centered, along x
const RIGHT: f32 = 2.35;
const NU: usize = 120; // the bands' meshes, around and across
const NV: usize = 8;
const FIBRES: usize = 20; // fibres drawn on each band

/// The point at angle u on the circle centered at x = `at`, v in [-1, 1] along its fibre, the fibre turning half
/// a turn around the circle if `twist` is 1.
fn band(u: f32, v: f32, twist: f32, at: f32, height: f32) -> [f32; 3] {
    let lean = twist * u / 2.0;
    let radial = [u.cos(), u.sin()];
    let fibre = [lean.sin() * radial[0], lean.sin() * radial[1], lean.cos()];
    let s = height * HALF * v;
    [at + RADIUS * radial[0] + s * fibre[0], RADIUS * radial[1] + s * fibre[1], s * fibre[2]]
}

fn surface(twist: f32, at: f32, height: f32, color: &str) -> Layer {
    let mut vertices = Vec::new();
    for i in 0..=NU {
        for j in 0..=NV {
            vertices.push(band(TAU * i as f32 / NU as f32, -1.0 + 2.0 * j as f32 / NV as f32, twist, at, height));
        }
    }
    let mut faces = Vec::new();
    for i in 0..NU {
        for j in 0..NV {
            let a = (i * (NV + 1) + j) as u32;
            let b = a + NV as u32 + 1;
            faces.extend([[a, b, a + 1], [a + 1, b, b + 1]]);
        }
    }
    Mesh::new(vertices, faces).color(color).pickable(false)
}

fn fibres(twist: f32, at: f32, height: f32, color: &str) -> Layer {
    let mut vertices = Vec::new();
    for k in 0..FIBRES {
        let u = TAU * k as f32 / FIBRES as f32;
        vertices.extend([band(u, -1.0, twist, at, height), band(u, 1.0, twist, at, height)]);
    }
    let segments = (0..FIBRES as u32).map(|k| [2 * k, 2 * k + 1]).collect();
    Lines::new(vertices).segments(segments).color(color).width(1.5)
}

fn circle(at: f32, color: &str) -> Layer {
    let vertices = (0..=NU).map(|i| band(TAU * i as f32 / NU as f32, 0.0, 0.0, at, 0.0)).collect();
    Lines::new(vertices).color(color).width(2.2)
}

/// A band is a pale tint of its color, its fibres and base circle the color itself.
fn pale(c: &str) -> String {
    format!("color-mix(in srgb, {c}, var(--bg) 62%)")
}

struct Bundles;

impl Widget for Bundles {
    fn new(_mesh: Option<MeshData>) -> Self {
        Bundles
    }

    fn setup(&self) -> Setup {
        // Fibres of 2% to all of their full length (at 0 the bands would be flat).
        Setup::new().slider("fibres", Slider::new(0.02, 1.0, 0.5).step(0.01))
    }

    fn scene(&self, state: &State) -> Scene {
        let height = state.value("fibres");
        Scene::new()
            .layer("leftCircle", circle(LEFT, "var(--link)"))
            .layer("rightCircle", circle(RIGHT, "var(--accent)"))
            .layer("cylinder", surface(0.0, LEFT, height, &pale("var(--link)")))
            .layer("mobius", surface(1.0, RIGHT, height, &pale("var(--accent)")))
            .layer("cylinderFibres", fibres(0.0, LEFT, height, "var(--link)"))
            .layer("mobiusFibres", fibres(1.0, RIGHT, height, "var(--accent)"))
    }
}

export!(Bundles);
