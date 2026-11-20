# Portfolio revision of the original normal-normal LDL planning analysis.
# Fixed-effect success probability is not design-prior averaged assurance.
args <- commandArgs(trailingOnly=TRUE)
out <- if(length(args)) args[1] else "results"
dir.create(out, recursive=TRUE, showWarnings=FALSE)
sigma <- 4.5; prior_mean <- 0; prior_sd <- 100; target <- .95

posterior <- function(D, n, sigma=4.5, m0=0, s0=100) {
  stopifnot(n>=1, sigma>0, s0>0)
  variance <- 1/(1/s0^2+n/(2*sigma^2))
  list(mean=variance*(m0/s0^2+n*D/(2*sigma^2)), sd=sqrt(variance))
}
critical_difference <- function(n, threshold=.95, sigma=4.5, m0=0, s0=100) {
  stopifnot(threshold>0, threshold<1)
  variance <- 1/(1/s0^2+n/(2*sigma^2))
  (qnorm(threshold)/sqrt(variance)-m0/s0^2)*2*sigma^2/n
}
success_probability <- function(n, delta, threshold=.95, sigma=4.5, m0=0, s0=100) {
  pnorm(critical_difference(n,threshold,sigma,m0,s0),mean=delta,sd=sqrt(2*sigma^2/n),lower.tail=FALSE)
}
design_assurance <- function(n, design_mean, design_sd, threshold=.95) {
  stopifnot(design_sd>=0)
  # Integrates uncertainty in the true effect under a Normal design prior.
  pnorm(critical_difference(n,threshold), mean=design_mean,
        sd=sqrt(2*sigma^2/n+design_sd^2), lower.tail=FALSE)
}
find_n <- function(delta, threshold=.95, maximum=10000) {
  n<-seq_len(maximum); eligible<-which(success_probability(n,delta,threshold)>=target)
  if(!length(eligible)) return(NA_integer_)
  n[min(eligible)]
}
classical_n <- function(delta, alpha=.05) {
  ceiling(2*sigma^2*(qnorm(1-alpha)+qnorm(target))^2/delta^2)
}
delta<-c(5,10,15,20)
results<-data.frame(delta=delta,bayes_threshold_95=sapply(delta,find_n),
  classical_alpha_05=sapply(delta,classical_n),
  bayes_threshold_975=sapply(delta,find_n,threshold=.975),
  classical_alpha_025=sapply(delta,classical_n,alpha=.025))
write.csv(results,file.path(out,"sample-sizes.csv"),row.names=FALSE)
set.seed(203)
validation<-do.call(rbind,lapply(delta,function(d){
 n<-find_n(d); D<-rnorm(100000,d,sqrt(2*sigma^2/n)); pp<-posterior(D,n)
 mc<-mean(pnorm(0,pp$mean,pp$sd,lower.tail=FALSE)>.95)
 data.frame(delta=d,n=n,analytic=success_probability(n,d),simulation=mc,mc_se=sqrt(mc*(1-mc)/length(D)))
}))
write.csv(validation,file.path(out,"simulation-check.csv"),row.names=FALSE)
stopifnot(all(abs(validation$analytic-validation$simulation)<5*validation$mc_se+.0001))
stopifnot(is.na(find_n(.0001,maximum=2)))
stopifnot(all(diff(success_probability(1:100,5))>=-1e-12))
png(file.path(out,"success-probability.png"),width=1280,height=720,res=150)
par(mar=c(4.2,5.1,2.3,1.5), family="sans")
sample_sizes <- 1:30
colors <- c("#23597a", "#a2451f", "#1b7669", "#714d87")
styles <- c(1, 2, 3, 4)
symbols <- c(16, 17, 15, 18)
plot(sample_sizes, rep(0,length(sample_sizes)), type="n", axes=FALSE,
     xlim=c(1,30), ylim=c(0,1.02), xlab="Sample size per arm",
     ylab="Design success probability", main="Posterior evidence threshold 0.95")
axis(1, at=c(1,5,10,15,20,25,30))
axis(2, at=seq(0,1,.25), labels=paste0(seq(0,100,25),"%"), las=1)
abline(h=target,lty=2,col="#687b8a")
text(29.5,target-.048,"95% design target",adj=1,col="#435c70",cex=.85)
for(i in seq_along(delta)) {
  lines(sample_sizes,success_probability(sample_sizes,delta[i]),
        col=colors[i],lty=styles[i],lwd=2.5)
  n <- results$bayes_threshold_95[i]
  points(n,success_probability(n,delta[i]),col=colors[i],pch=symbols[i],cex=1.1)
}
legend("bottomright",inset=.03,legend=delta,title="Assumed difference",
       col=colors,lty=styles,pch=symbols,lwd=2.5,bty="n",cex=.88)
dev.off()
capture.output(sessionInfo(),file=file.path(out,"session-info.txt"))
print(results)
