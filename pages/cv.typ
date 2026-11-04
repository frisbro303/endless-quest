#set document(title: "Felix Granum – CV", author: "Felix Granum")
#set page(margin: (x: 2.2cm, y: 1.8cm))
#set text(size: 10.5pt)

// The website opens with a short about before the CV; the PDF is just the CV.
#context if target() == "paged" {
  align(center, title())
} else {
  [I am Felix Granum, a researcher interested in _mathematics_ and _computing_ with a focus on _shape analysis_. You can read about my thoughts and ideas on my #link("../")[blog].]
  parbreak()
  [My CV is available below or in #html.elem("a", attrs: (href: "cv.pdf", download: ""))[PDF form].]
  parbreak()
  html.elem("h1")[Curriculum Vitae]
}

Email: #link("mailto:felix.granum@pm.me")[felix.granum\@pm.me], #link("mailto:felix.granum@duke.edu")[felix.granum\@duke.edu] \
Website/Blog: #link("https://frisbro303.github.io/endless-quest/")[frisbro303.github.io/endless-quest] \
GitHub: #link("https://github.com/frisbro303")[github.com/frisbro303] \
ORCID: #link("https://orcid.org/0009-0007-3158-0553")[0009-0007-3158-0553]

= Research Interests

Shape analysis, differential geometry, computational geometry, Gaussian processes, numerical analysis.

= Current Position

*Associate in Research*, Duke University, September 2026 – present \
Supervised by Prof. Ingrid Daubechies.

= Education

*BSc in Mathematics*, University of Southern Denmark, 2023 – 2026

= Research Experience

*Landmarks Are Sections: Gaussian Process Landmarking on Fiber Bundles*, Duke University & University of Southern Denmark, 2024 – present \
Developing a framework I conceived for jointly landmarking shape collections via Gaussian processes defined on fiber bundles. _Manuscript in preparation._

*Statistical Shape Analysis of _Drosophila_ Wings*, Duke University, University of Chicago & University of Southern Denmark, 2024 – present \
Using diffusion maps and horizontal diffusion maps to analyze the wing shapes of _Drosophila_ (fruit flies). _Manuscript in preparation._

*Automated Analysis of Bone Fragment Breakage*, Duke University, University of Minnesota (AMAAZE) & University of Southern Denmark, 2025 – present \
Developing and implementing methods, based on statistical shape analysis and topological data analysis, that identify break faces on 3D meshes of bone fragments. The goal is to investigate whether early hominins were the agents of breakage.

= Research Outputs

== Preprints

*Felix Risbro Hjerrild*, Shan Shan, Doug Boyer, Ingrid Daubechies (2024). _signDNE: A python package for ariaDNE and its sign-oriented extension_. #link("https://arxiv.org/abs/2409.05549")[arXiv:2409.05549]. Implementation: #link("https://github.com/frisbro303/SignDNE")[github.com/frisbro303/SignDNE]. Written under my former name.

== Posters

*Felix Granum* et al. (2026). _Learning the Geometry of Shape Families: A Fiber Bundle Framework_. NITMB workshop #link("https://www.nitmb.org/event/representing-and-learning-morphology-and-shape-dynamics-from-biological-data/")[Representing and Learning Morphology and Shape Dynamics from Biological Data], Chicago, October 2026.

== Software

*HDMaps*, #link("https://github.com/MorphMath/HDMaps")[github.com/MorphMath/HDMaps] \
Co-developed the Python implementation of horizontal diffusion maps.

*signDNE*, #link("https://github.com/frisbro303/SignDNE")[github.com/frisbro303/SignDNE] \
Developed a Python package for ariaDNE and its sign-oriented extension.

= Teaching

*Teaching Assistant, Calculus for Mathematics* (MM536, MM558), University of Southern Denmark, Fall 2025

*Teaching Assistant, Advanced Linear Algebra* (MM562), University of Southern Denmark, Spring 2026
