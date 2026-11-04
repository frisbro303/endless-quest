#set document(
  title: "Fiber Bundles and the Hopf Fibration",
  description: "I discuss fiber bundles, with the beautiful Hopf fibration as a special case.",
)

#import "/template.typ": *
#import "@preview/fletcher:0.5.8" as fletcher: diagram, edge, node

The logo image of this website is a visualization of the Hopf fibration.
The Hopf fibration is perhaps one of the most famous examples of a fiber bundle.
With this in mind, it is only right that my first post should be about fiber bundles to give some more intuition for this beautiful object.
I will try to give a bare-bones intuitive picture, even though both fiber bundles and the Hopf fibration are much, much deeper than what is presented here.
The exposition will roughly follow the Wikipedia articles on #link("https://en.wikipedia.org/wiki/Fiber_bundle")[fiber bundles] and the #link("https://en.wikipedia.org/wiki/Hopf_fibration")[Hopf fibration].

#themed-gif(
  "figures/Hook",
  [The Hopf fibration of $SS^3$, drawn after stereographic projection to $RR^3$.],
) <fig:hook>

= Fiber Bundles
A fiber bundle is a space that is locally a product space. A familiar example is the cylinder, which is formed by gluing an interval to each point in a circle, that is $SS^1 times [-1, 1]$.
The cylinder is a kind of non-example in that it is not only locally a product space, but in fact globally one. The simplest example of a non-trivial fiber bundle is the Möbius band. Locally it looks like we are doing the exact same gluing of an interval to a circle, but globally it is not a product. @fig:bundles shows this difference.

#themed-gif(
  "figures/Bundles",
  [Two distinct bundles over the circle with interval fibers: the cylinder (left side), which is a product globally, and the Möbius band (right side), which is a product only locally.],
) <fig:bundles>

When thinking about fiber bundles I am reminded of the following quote.

#quote(block: true, attribution: [Geoffrey Hinton])[
  To deal with hyper-planes in a 14-dimensional space, visualize a 3-D space and say "fourteen" to yourself very loudly. Everyone does it.
]

In the same spirit: to deal with a non-trivial fiber bundle, picture the Möbius band (in contrast to the cylinder) and say "fiber bundle" to yourself very loudly. This is the mental image to hold dear.

Now make sure you are sitting down, because here comes the rather technical definition of a fiber bundle.
#definition(title: "Fiber bundle")[
  A _fiber bundle_ with base $B$ and fiber $F$ is a continuous surjection $p: E -> B$ such that every point of $B$ has an open neighborhood $U$ with a homeomorphism $phi: p^(-1)(U) -> U times F$ making the diagram commute:
  #html.elem("div", attrs: (class: "diagram"), html.frame(text(size: 14pt, diagram(
    $
      p^(-1)(U) edge("rr", phi, ->) edge("dr", p, ->, label-side: #right) &   & U times F edge("dl", "pr"_1, ->) \
                                                                          & U &
    $,
  ))))
]

In other words, every point of $B$ has a neighborhood $U$ over which $E$ looks like the product $U times F$. Commuting with the projections means $phi$ keeps track of where on the base we are: a point above $u in U$ is sent to $(u, f)$ for some $f in F$. This property is referred to as local triviality.

For the cylinder, take $E = SS^1 times [-1, 1]$ and $p(x, t) = x$. Here we can get away with choosing a single neighborhood $U = SS^1$ and letting $phi$ be the identity. This covers all of $B$ and is what makes the bundle a product globally.

For the Möbius band, take the square $[0, 1] times [-1, 1]$ and glue its ends with a twist, $(0, t) tilde (1, -t)$. Then
$
  p(s, t) = (cos 2 pi s, sin 2 pi s).
$
On $U = SS^1 without {(1, 0)}$, we let $phi(s, t) = (p(s, t), t)$.
To cover the remaining point $(1, 0)$, we take $V = SS^1 without {(-1, 0)}$, which is where
$s in [0, 1/2) union (1/2, 1]$, and let $psi(s, t) = (p(s, t), t)$ for $s < 1/2$ and $(p(s, t), -t)$ for $s > 1/2$. These two neighborhoods suffice, but no single $phi$ works over all of $SS^1$, since going once around the circle flips the fiber, $t |-> -t$.


= The Hopf Fibration
The Hopf fibration is a fiber bundle with total space $SS^3$, base $SS^2$ and fiber $SS^1$. To see why, we start by finding a continuous surjection from $SS^3$ to $SS^2$ that is locally trivial.

The Hopf map $p : SS^3 -> SS^2$, given by
#responsive(
  $
    p(x_1, x_2, x_3, x_4) = (2(x_1 x_3 + x_2 x_4), 2(x_2 x_3 - x_1 x_4), x_1^2 + x_2^2 - x_3^2 - x_4^2),
  $,
  $
    p(x_1, x_2, x_3, x_4) = (
      2(x_1 x_3 + x_2 x_4), \
      2(x_2 x_3 - x_1 x_4), \
      x_1^2 + x_2^2 - x_3^2 - x_4^2
    ),
  $,
)
is exactly the map we are looking for.

To show that the map is well defined we note that
#responsive(
  $
    norm(p(x))^2 & = 4(x_1 x_3 + x_2 x_4)^2 + 4(x_2 x_3 - x_1 x_4)^2 + (x_1^2 + x_2^2 - x_3^2 - x_4^2)^2 \
                 & = 4(x_1^2 + x_2^2)(x_3^2 + x_4^2) + (x_1^2 + x_2^2 - x_3^2 - x_4^2)^2 \
                 & = (x_1^2 + x_2^2 + x_3^2 + x_4^2)^2 = 1,
  $,
  $
    norm(p(x))^2 = 4(x_1 x_3 + x_2 x_4)^2 + 4(x_2 x_3 - x_1 x_4)^2 \
    + (x_1^2 + x_2^2 - x_3^2 - x_4^2)^2 \
    = 4(x_1^2 + x_2^2)(x_3^2 + x_4^2) \
    + (x_1^2 + x_2^2 - x_3^2 - x_4^2)^2 \
    = (x_1^2 + x_2^2 + x_3^2 + x_4^2)^2 = 1,
  $,
)
for $(x_1, x_2, x_3, x_4) in SS^3$, which shows that $p(x) in SS^2$.

Note that $p$ is continuous since it is a polynomial map. Next we show that $p$ is surjective.

Let $(y_1, y_2, y_3) in SS^2$.
If $y_3 = -1$, then $p(0, 0, 1, 0) = (0, 0, -1)$.
Otherwise set
#responsive(
  $
    x_1 = sqrt((1 + y_3) / 2), quad x_2 = 0, quad x_3 = y_1 / (2 x_1), quad x_4 = -y_2 / (2 x_1).
  $,
  $
    x_1 = sqrt((1 + y_3) / 2), quad x_2 = 0, \ x_3 = y_1 / (2 x_1), quad x_4 = -y_2 / (2 x_1).
  $,
)
Since $y_1^2 + y_2^2 = 1 - y_3^2$ and $4 x_1^2 = 2(1 + y_3)$, this $(x_1, x_2, x_3, x_4)$ lies on $SS^3$:
#responsive(
  $
    x_1^2 + x_2^2 + x_3^2 + x_4^2 & = (1 + y_3)/2 + (y_1^2 + y_2^2)/(4 x_1^2) \
                                  & = (1 + y_3)/2 + ((1 - y_3)(1 + y_3))/(2(1 + y_3)) \
                                  & = (1 + y_3)/2 + (1 - y_3)/2 = 1.
  $,
  $
    x_1^2 + x_2^2 + x_3^2 + x_4^2 \
    = (1 + y_3)/2 + (y_1^2 + y_2^2)/(4 x_1^2) \
    = (1 + y_3)/2 + ((1 - y_3)(1 + y_3))/(2(1 + y_3)) \
    = (1 + y_3)/2 + (1 - y_3)/2 = 1.
  $,
)
Evaluating $p$ at this point, we see that
#responsive(
  $
    p(x) & = (2 x_1 x_3, -2 x_1 x_4, x_1^2 - x_3^2 - x_4^2) \
         & = (2 x_1 dot y_1 / (2 x_1), -2 x_1 dot (-y_2 / (2 x_1)), (1+y_3)/2 - y_1^2/(4x_1^2) - y_2^2/(4x_1^2)) \
         & = (y_1, y_2, (1+y_3)/2 - ((1-y_3)(1+y_3))/(2(1+y_3))) \
         & = (y_1, y_2, (1+y_3)/2 - (1-y_3)/2) \
         & = (y_1, y_2, y_3).
  $,
  $
    p(x) = (2 x_1 x_3, -2 x_1 x_4, x_1^2 - x_3^2 - x_4^2) \
    = (
      2 x_1 dot y_1 / (2 x_1), \
      -2 x_1 dot (-y_2 / (2 x_1)), \
      (1+y_3)/2 - y_1^2/(4x_1^2) - y_2^2/(4x_1^2)
    ) \
    = (y_1, y_2, (1+y_3)/2 - ((1-y_3)(1+y_3))/(2(1+y_3))) \
    = (y_1, y_2, (1+y_3)/2 - (1-y_3)/2) \
    = (y_1, y_2, y_3).
  $,
)
This shows that $p$ is indeed surjective.

For the local triviality, let $U = SS^2 without {(0, 0, -1)}$. On $p^(-1)(U)$ we have $x_1^2 + x_2^2 = (1 + y_3)/2 > 0$, so we can set
$
  phi(x) = (p(x), ((x_1, x_2)) / sqrt(x_1^2 + x_2^2)) in U times SS^1.
$
Its inverse is then
#responsive(
  $
    phi^(-1)(y, (c, s)) = (r c, r s, (c y_1 + s y_2)/(2 r), (s y_1 - c y_2)/(2 r)),
  $,
  $
    phi^(-1)(y, (c, s)) = (
      r c, r s, \
      (c y_1 + s y_2)/(2 r), (s y_1 - c y_2)/(2 r)
    ),
  $,
)
with $r = sqrt((1 + y_3)/2)$.

Both $phi$ and $phi^(-1)$ are continuous, so $phi$ is a homeomorphism, and its first coordinate is $p$, so the diagram commutes.

To cover the south pole, let $V = SS^2 without {(0, 0, 1)}$. On $p^(-1)(V)$ we have $x_3^2 + x_4^2 = (1 - y_3)/2 > 0$, so we set
$
  psi(x) = (p(x), ((x_3, x_4)) / sqrt(x_3^2 + x_4^2)) in V times SS^1,
$
with inverse
#responsive(
  $
    psi^(-1)(y, (c, s)) = ((c y_1 - s y_2)/(2 rho), (s y_1 + c y_2)/(2 rho), rho c, rho s),
  $,
  $
    psi^(-1)(y, (c, s)) = (
      (c y_1 - s y_2)/(2 rho), (s y_1 + c y_2)/(2 rho), \
      rho c, rho s
    ),
  $,
)
for $rho = sqrt((1 - y_3)/2)$.

As before, $psi$ is a homeomorphism whose first coordinate is $p$. Since $U$ and $V$ cover $SS^2$, $p$ is a fiber bundle with fiber $SS^1$.

Let $y = (y_1, y_2, y_3) in U subset.eq SS^2$. Then by local triviality
#responsive(
  $
    p^(-1)(y) & = { x in SS^3 : p(x) = y } = phi^(-1)({y} times SS^1) \
              & = { phi^(-1)(y, (c, s)) : (c, s) in SS^1 } tilde.equiv {y} times SS^1 tilde.equiv SS^1,
  $,
  $
    p^(-1)(y) = { x in SS^3 : p(x) = y } \
    = phi^(-1)({y} times SS^1) \
    = { phi^(-1)(y, (c, s)) : (c, s) in SS^1 } \
    tilde.equiv {y} times SS^1 tilde.equiv SS^1,
  $,
)
where $tilde.equiv$ means homeomorphic. The same holds for $y in V$ using $psi$.

@fig:hopf shows the preimages $p^(-1)(y) subset SS^3$ of points $y in SS^2$, each a copy of $SS^1$, drawn in $RR^3$ by stereographic projection. I will hopefully get around to covering the stereographic projection another time.

#themed-gif(
  "figures/HopfMap",
  [The Hopf map $p$. The preimage of each point of $SS^2$ is a circle in $SS^3$, drawn here after stereographic projection to $RR^3$.],
) <fig:hopf>

The logo image is the same kind of projection as @fig:hook, only viewed from above with a different color scheme.

