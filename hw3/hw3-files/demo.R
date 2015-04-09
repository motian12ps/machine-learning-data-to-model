library(plyr)

source("probs.R")
source("inference.R")

#' -----------------------------------------------------------------------
#' First let's compute the full joint and compute the marginal of E and F.
#' 

full <- make.full.joint(prob.all)
ef.full <- ddply(full, ~ E + F, summarize, Pr=sum(Pr))
cat("True marginal of E and F:\n")
ef.full

#' -----------------------------------------------------------------------
#' Let's use the mean field approximation.
#' 

mean.field <- mean.field.inference()
ef.mean.field <- ddply(mean.field, ~ E + F, summarize, Pr=sum(Pr))
cat("Mean field approximation of marginal of E and F:\n")
ef.mean.field
cat("KL Div: ", ef.kl.div(ef.full, ef.mean.field), "\n")

#' -----------------------------------------------------------------------
#' That didn't work well... now let's try a structured mean field.
#' 

struct.mean.field <- struct.mean.field.inference()
ef.struct.mean.field <- ddply(struct.mean.field, ~ E + F, summarize, Pr=sum(Pr))
cat("Structured mean field approximation of marginal of E and F:\n")
ef.struct.mean.field
cat("KL Div: ", ef.kl.div(ef.full, ef.struct.mean.field), "\n")
