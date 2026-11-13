// The home page: the posts, newest first.
#import "/template.typ": *
#show: home.with("index", title: "Endless Quest")

= blog
#listing("post")
