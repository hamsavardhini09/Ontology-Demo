#install.packages("miscTools")
library(miscTools)
library(tm)
library(e1071)

args <- commandArgs(TRUE)

## Read
argument1 <- as.String(args[1])


##Pre-processing
corpus = Corpus(VectorSource(argument1))
dtm = DocumentTermMatrix(corpus, control = list(weighting=function(x) weightBin(x), stopwords = TRUE))
m = as.matrix(dtm)
d = data.frame(m)

## Load model and predict
load("predictionModel/myModel.RData")
prede10 = predict(e10, d, type = "raw")

prede10 = prede10*100

## Write
write(prede10, stdout())
