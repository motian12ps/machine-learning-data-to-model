mean.field.inference <- function()
{
  q.a <- new.joint(1)
  q.b <- new.joint(1)
  q.c <- new.joint(1)
  q.d <- new.joint(1)
  q.e <- new.joint(1)
  q.f <- new.joint(1)

  a.up <- function(a)
  {
    stop("You need to implement the update for Q(A)")
  }

  b.up <- function(b)
  {
    stop("You need to implement the update for Q(B)")
  }

  c.up <- function(c)
  {
    stop("You need to implement the update for Q(C)")
  }

  d.up <- function(d)
  {
    stop("You need to implement the update for Q(D)")
  }

  e.up <- function(e)
  {
    stop("You need to implement the update for Q(E)")
  }

  f.up <- function(f)
  {
    stop("You need to implement the update for Q(F)")
  }

  niter <- 0
  converged <- FALSE
  tol <- 1e-3

  close.enough <- function(q, q.old)
  {
    max(abs(q - q.old)) < tol
  }

  while (!converged)
  {
    q.a.old <- q.a
    q.b.old <- q.b
    q.c.old <- q.c
    q.d.old <- q.d
    q.e.old <- q.e
    q.f.old <- q.f

    q.a <- c(a.up(1), a.up(2)) / sum(a.up(1), a.up(2))
    q.b <- c(b.up(1), b.up(2)) / sum(b.up(1), b.up(2))
    q.c <- c(c.up(1), c.up(2)) / sum(c.up(1), c.up(2))
    q.d <- c(d.up(1), d.up(2)) / sum(d.up(1), d.up(2))
    q.e <- c(e.up(1), e.up(2)) / sum(e.up(1), e.up(2))
    q.f <- c(f.up(1), f.up(2)) / sum(f.up(1), f.up(2))

    niter <- niter + 1

    converged <- all(close.enough(q.a, q.a.old),
                     close.enough(q.b, q.b.old),
                     close.enough(q.c, q.c.old),
                     close.enough(q.d, q.d.old),
                     close.enough(q.e, q.e.old),
                     close.enough(q.f, q.f.old))
  }

  q.full <- function(a, b, c, d, e, f)
  {
    q.a[a] * q.b[b] * q.c[c] * q.d[d] * q.e[e] * q.f[f]
  }

  make.full.joint(q.full)
}

struct.mean.field.inference <- function()
{
  q.abc <- new.joint(3)
  q.def <- new.joint(3)

  q.b <-  function(b)    sum(q.abc[, b, ])
  q.c <-  function(c)    sum(q.abc[, , c])
  q.d <-  function(d)    sum(q.def[d, , ])
  q.de <- function(d, e) sum(q.def[d, e, ])

  abc.up <- function(a, b, c)
  {
    stop("You need to implement the update for Q(ABC)")
  }

  def.up <- function(d, e, f)
  {
    stop("You need to implement the update for Q(DEF)")
  }

  niter <- 0
  converged <- FALSE
  tol <- 1e-3

  close.enough <- function(q, q.old)
  {
    max(abs(q - q.old)) < tol
  }

  while (!converged)
  {
    q.abc.old <- q.abc
    q.def.old <- q.def

    combs <- as.matrix(expand.grid(1:2, 1:2, 1:2))

    ## Update A,B,C

    for (i in seq_len(nrow(combs)))
    {
      a <- combs[i, 1]
      b <- combs[i, 2]
      c <- combs[i, 3]

      q.abc[a, b, c] <- abc.up(a, b, c)
    }

    q.abc <- q.abc / sum(q.abc)

    ## Update D,E,F

    for (i in seq_len(nrow(combs)))
    {
      d <- combs[i, 1]
      e <- combs[i, 2]
      f <- combs[i, 3]

      q.def[d, e, f] <- def.up(d, e, f)
    }

    q.def <- q.def / sum(q.def)

    niter <- niter + 1

    converged <- all(close.enough(q.abc, q.abc.old),
                     close.enough(q.def, q.def.old))
  }

  q.full <- function(a, b, c, d, e, f)
  {
    q.abc[a, b, c] * q.def[d, e, f]
  }

  make.full.joint(q.full)
}
