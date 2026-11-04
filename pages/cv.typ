#set document(title: "Curriculum Vitae")
#set page(margin: (x: 2.2cm, y: 1.8cm))
#set text(size: 10.5pt)

// The website opens with a short about before the CV; the PDF is just the CV.
#context if target() == "paged" {
  align(center, title())
} else {
  [I am Felix Granum, an aspiring researcher interested in _mathematics_ and _computing_ with a focus on _shape analysis_. You can read about my thoughts and ideas on my #link("../")[blog].]
  parbreak()
  [My CV is available below or in #html.elem("a", attrs: (href: "cv.pdf", download: ""))[PDF form].]
  parbreak()
  html.elem("h1")[Curriculum Vitae]
}

= Felix Granum

Email: #link("mailto:felix.granum@pm.me")[felix.granum\@pm.me]\; #link("mailto:felix.granum@duke.edu")[felix.granum\@duke.edu]

GitHub: #link("https://github.com/frisbro303")[github.com/frisbro303]

ORCID: #link("https://orcid.org/0009-0007-3158-0553")[0009-0007-3158-0553]

= Current Position

Associate in Research; September 2026 - Present; Duke University; supervised by Prof. Ingrid Daubechies.

= Educational Background

BSc, Mathematics; 2023 - 2026; University of Southern Denmark.

= Research Experience

- *Collaborative Research & Bachelor Thesis Project*; 2024 - 2026; Duke University & University of Southern Denmark.
  - Developed a framework for jointly landmarking shape collections via Gaussian Processes defined on fiber bundles.
  - Used Horizontal Diffusion Maps to provide a geometric anchor for the Gaussian Process.
- *Collaborative Research*; 2024 - Present; Duke University & University of Southern Denmark.
  - Researched and implemented signDNE, a method for robustly computing direction of curvature energy; 2024.
  - Applying Horizontal Diffusion Maps for morphometric analysis of Drosophila (fruit flies); 2025 - Present.
- *Collaborative Research*; 2025 - Present; Duke University, University of Minnesota (AMAAZE labs) & University of Southern Denmark.
  - Collaborative research at the intersection of data science and shape analysis applied to complex biological materials.
  - Computational pipeline development: automating the extraction of break-related geometric features from 3D meshes of bone fragments to identify agents of breakage.

= Publications

== Preprints

- Felix Risbro Hjerrild\*, Shan Shan, Doug Boyer, Ingrid Daubechies. 2024; signDNE: A python package for ariaDNE and its sign-oriented extension; arXiv preprint. #link("https://arxiv.org/abs/2409.05549")[arXiv:2409.05549]\; implementation: #link("https://github.com/frisbro303/SignDNE")[github.com/frisbro303/SignDNE]\; (\*Written under my former name).

== Posters

- Felix Granum et al. 2026; Learning the Geometry of Shape Families: A Fiber Bundle Framework; NITMB workshop #link("https://www.nitmb.org/event/representing-and-learning-morphology-and-shape-dynamics-from-biological-data/")[Representing and Learning Morphology and Shape Dynamics from Biological Data], Chicago, October 2026.

= Teaching

- TA in Calculus for Mathematics; MM536, MM558; Fall Semester 2025; University of Southern Denmark.
- TA in Advanced Linear Algebra; MM562; Spring Semester 2026; University of Southern Denmark.

= Research Interests

Shape Analysis; Differential Geometry; Computational Geometry; Gaussian Processes; Numerical Analysis.
