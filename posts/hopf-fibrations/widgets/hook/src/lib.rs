//! The hook at the top of the Hopf post: nested tori of linked Hopf fibres, flowing round, in S^3 drawn in R^3 by
//! stereographic projection. Each circle of latitude on S^2 lifts to one torus.

use std::f32::consts::TAU;
use wgw_widget::*;

const LATITUDES: [f32; 5] = [30.0, 50.0, 70.0, 90.0, 105.0]; // polar angles in degrees; nearer the south pole, the tori blow up
const FIBRES: usize = 14; // fibres per torus
const SEGMENTS: usize = 80; // straight pieces per fibre, more for the outer tori
const FRAMES: u32 = 48; // the fibres slide one fibre's spacing round their torus over the loop
const BREATH: f32 = 3.0; // degrees each latitude swells and shrinks, so the tori pulse into one another

/// A point of S^3 over (polar, longitude) on S^2, turned by `turn` around its fibre, carried to R^3.
fn fibre_point(polar: f32, longitude: f32, turn: f32) -> [f32; 3] {
    let (r1, r2) = ((polar / 2.0).cos(), (polar / 2.0).sin());
    let d = 1.0 - r2 * turn.sin();
    [r1 * (longitude + turn).cos() / d, r1 * (longitude + turn).sin() / d, r2 * turn.cos() / d]
}

/// One torus's fibres at a moment of the loop: teal to orange around it, outer tori fainter and thinner.
fn torus(index: usize, progress: f32) -> Layer {
    let pieces = SEGMENTS * (1 + index / 2);
    let polar = (LATITUDES[index] + BREATH * (TAU * progress + index as f32 * TAU / LATITUDES.len() as f32).sin()).to_radians();
    let (mut vertices, mut values, mut segments) = (Vec::new(), Vec::new(), Vec::new());
    for j in 0..FIBRES {
        let longitude = TAU * (j as f32 + progress) / FIBRES as f32;
        let first = vertices.len() as u32;
        for i in 0..=pieces {
            vertices.push(fibre_point(polar, longitude, TAU * i as f32 / pieces as f32));
            values.push((1.0 - longitude.cos()) / 2.0); // by where the fibre is, so the colors stay put as fibres pass
        }
        segments.extend((0..pieces as u32).map(|i| [first + i, first + i + 1]));
    }
    let faint = (60.0 * index as f32 / (LATITUDES.len() - 1) as f32).round(); // percent of the background mixed in
    let mix = |c: &str| format!("color-mix(in srgb, {c}, var(--bg) {faint}%)");
    Lines::new(vertices)
        .segments(segments)
        .values(values)
        .colors(&[&mix("var(--link)"), &mix("var(--accent)")])
        .width(2.6 - 0.3 * index as f64)
}

struct Hook;

impl Widget for Hook {
    fn new(_mesh: Option<MeshData>) -> Self {
        Hook
    }

    fn setup(&self) -> Setup {
        Setup::new().frames(FRAMES).fps(12.0)
    }

    fn scene(&self, state: &State) -> Scene {
        let progress = state.frame as f32 / FRAMES as f32;
        (0..LATITUDES.len()).fold(Scene::new(), |s, i| s.layer(&format!("torus{i}"), torus(i, progress)))
    }
}

export!(Hook);
