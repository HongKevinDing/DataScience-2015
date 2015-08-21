## CDIPS 2015 Workshop Project
## Team: Acronyms
## Members: Hong Ding, Philipp Dumitrescu, Herman Leung
## July 11 - Aug 1, 2015


# The following 3 files are generated from bootstrap_preprocess_compare_acronyms_sets.py

AF_freq = read.csv('AF_bootstrap_percent.csv')
W_freq = read.csv('Wiki_bootstrap_percent.csv')
D_freq = read.csv('Diff_bootstrap_percent.csv')


# Create an empty numeric dataframe of 5000 x 3

c1 = numeric(5000)
c2 = numeric(5000)
c3 = numeric(5000)
ci.df = data.frame(Lower=c1, Upper=c2, Pvalue=c3)


# Fill that dataframe with Wilcoxon Test results of confidence intervals and p-values

for(i in 1:R){
wt = wilcox.test(as.numeric(AF_freq[i,]), as.numeric(D_freq[i,]), na.omit=T, conf.int=T)
ci.df[i,1] = wt$conf.int[1]
ci.df[i,2] = wt$conf.int[2]
ci.df[i,3] = wt$p.value
}


# Plot comparison between AcronymFinder and Wikipedia letter frequency densities

plot(density(as.numeric(AF_freq[1,])), ylim=c(0,30), xlim=c(-0.05,0.15), col='blue')
for(i in 2:R){
v = AF_freq[i,]
v = v[!is.na(v)]
lines(density(v), col='blue')
}

lines(density(as.numeric(W_freq[1,])), ylim=c(0,30), xlim=c(-0.05,0.15), col=rgb(1,0,0,alpha=0.05)))
for(i in 2:R){
v = W_freq[i,]
v = v[!is.na(v)]
lines(density(v), col=rgb(1,0,0,alpha=0.05))
}


# Plot comparison between Wikipedia and 'difference2' letter frequency densities

plot(density(as.numeric(D_freq[1,])), ylim=c(0,30), xlim=c(-0.05,0.15), col='blue')
for(i in 2:R){
v = D_freq[i,]
v = v[!is.na(v)]
lines(density(v), col='blue')
}

lines(density(as.numeric(W_freq[1,])), ylim=c(0,30), xlim=c(-0.05,0.15), col=rgb(1,0,0,alpha=0.05))
for(i in 2:R){
v = W_freq[i,]
v = v[!is.na(v)]
lines(density(v), col=rgb(1,0,0,alpha=0.05))
}
