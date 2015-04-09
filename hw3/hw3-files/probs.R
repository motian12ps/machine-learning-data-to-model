prob.a <- function(a) 0.5

prob.b.given.a <- function(b, a)
{
  if (b == a) 0.9 else 0.1
}

prob.c.given.ab <- function(c, a, b)
{
  if (a == b) {
    if (c == a) 0.9 else 0.1
  } else {
    0.5
  }
}

prob.d.given.b <- function(d, b)
{
  if (b == 1) {
    switch(d, 0.6, 0.4)
  } else {
    switch(d, 0.4, 0.6)
  }
}

prob.e.given.cd <- function(e, c, d)
{
  if (c == 1) {
    if (e == d) 0.9 else 0.1
  } else {
    if (e == d) 0.7 else 0.3
  }
}

prob.f.given.d <- function(f, d) {
  if (f == d) 0.9 else 0.1
}

prob.all <- function(a, b, c, d, e, f)
{
  p <- 1
  p <- p * prob.a(a)
  p <- p * prob.b.given.a(b, a)
  p <- p * prob.c.given.ab(c, a, b)
  p <- p * prob.d.given.b(d, b)
  p <- p * prob.e.given.cd(e, c, d)
  p <- p * prob.f.given.d(f, d)
  p
}

make.table <- function()
{
  A <- B <- C <- D <- E <- F <- 1:2
  joint <- expand.grid(A=A, B=B, C=C, D=D, E=E, F=F)
  joint
}

make.full.joint <- function(q.full)
{
  joint <- make.table()

  prob.of.row <- function(i)
  {
    with(joint[i, ], q.full(A, B, C, D, E, F))
  }

  probs <- vapply(1:nrow(joint), prob.of.row, numeric(1))
  joint[["Pr"]] <- probs
  joint
}

new.joint <- function(d)
{
  q <- array(runif(2^d), dim=rep(2, d))
  q <- q / sum(q)
  q
}

ef.kl.div <- function(p, q)
{
  p.probs <- p$Pr
  q.probs <- q$Pr

  sum(p.probs * log2(p.probs / q.probs))
}
