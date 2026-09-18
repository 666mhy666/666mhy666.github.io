# Revised longitudinal GCC analysis. No source data are redistributed.
suppressPackageStartupMessages(library(nlme))
args<-commandArgs(trailingOnly=TRUE);if(!length(args))stop("Usage: Rscript analysis.R data.csv results")
out<-if(length(args)>1)args[2] else "results";dir.create(out,recursive=TRUE,showWarnings=FALSE)
d<-read.csv(args[1],fileEncoding="UTF-8-BOM");req<-c("id","time","GCC","base_age");stopifnot(all(req%in%names(d)))
d<-d[complete.cases(d[,req]),req];d$id<-factor(d$id);d<-d[order(d$id,d$time),]
stopifnot(!anyDuplicated(d[c("id","time")]),all(d$time>=0))
ctl<-lmeControl(maxIter=200,msMaxIter=200,returnObject=FALSE)
fit_mean<-function(f)lme(f,data=d,random=~1|id,method="ML",control=ctl)
means<-list(null=fit_mean(GCC~1),linear=fit_mean(GCC~time),quadratic=fit_mean(GCC~time+I(time^2)),log=fit_mean(GCC~log(time+.01)))
tab<-function(models)do.call(rbind,lapply(names(models),function(n)data.frame(model=n,AIC=AIC(models[[n]]),BIC=BIC(models[[n]]),n=nobs(models[[n]]))))
mt<-tab(means);write.csv(mt,file.path(out,"mean-models-ml.csv"),row.names=FALSE)
mean_name<-mt$model[which.min(mt$BIC)];fixed<-formula(means[[mean_name]])
# All covariance candidates share the selected fixed-effects formula.
candidates<-list(RI=list(random=~1|id),RIAS=list(random=~time|id),
 RIAS_CAR1=list(random=~time|id,correlation=corCAR1(form=~time|id)))
models<-list();errors<-character()
for(n in names(candidates)){
 m<-tryCatch(do.call(lme,c(list(fixed=fixed,data=d,method="REML",control=ctl),candidates[[n]])),error=function(e)e)
 if(inherits(m,"error")){errors<-c(errors,paste(n,conditionMessage(m)))}else models[[n]]<-m
}
if(!length(models))stop("No candidate model converged")
ct<-tab(models);write.csv(ct,file.path(out,"covariance-models.csv"),row.names=FALSE)
best<-ct$model[which.min(ct$BIC)];fit<-models[[best]]
tt<-as.data.frame(summary(fit)$tTable);tt$term<-rownames(tt);rownames(tt)<-NULL
tt$lower<-tt$Value-qt(.975,tt$DF)*tt$Std.Error;tt$upper<-tt$Value+qt(.975,tt$DF)*tt$Std.Error
write.csv(tt,file.path(out,"coefficients.csv"),row.names=FALSE)
# One baseline per subject prevents a visit-count-weighted median.
baseline<-d[!duplicated(d$id),c("id","GCC")];cutoff<-median(baseline$GCC)
d$baseline_group<-factor(ifelse(baseline$GCC[match(d$id,baseline$id)]>=cutoff,"High","Low"),levels=c("Low","High"))
# Exploratory interaction uses follow-up outcomes only to reduce direct reuse of baseline in the response.
follow<-d[d$time>0,];subgroup<-lme(GCC~time*baseline_group,data=follow,random=~time|id,correlation=corCAR1(form=~time|id),method="REML",control=ctl)
st<-as.data.frame(summary(subgroup)$tTable);st$term<-rownames(st);rownames(st)<-NULL
write.csv(st,file.path(out,"exploratory-baseline-interaction.csv"),row.names=FALSE)
# Age comparison: ML, same sample, same random/correlation structure.
age0<-update(fit,method="ML");age1<-update(age0,fixed=update(fixed,~.+base_age+time:base_age))
write.csv(tab(list(without_age=age0,with_age=age1)),file.path(out,"age-models-ml.csv"),row.names=FALSE)
grid<-data.frame(time=seq(0,max(d$time),length.out=100),id=d$id[1]);grid$mean<-predict(fit,newdata=grid,level=0)
write.csv(grid[c("time","mean")],file.path(out,"mean-trajectory.csv"),row.names=FALSE)
png(file.path(out,"gcc-trajectory.png"),width=1100,height=650,res=150)
plot(grid$time,grid$mean,type="l",lwd=2,col="#23597a",xlab="Years since baseline",ylab="Predicted mean GCC (microns)",main="Model-estimated GCC trajectory");dev.off()
png(file.path(out,"diagnostics.png"),width=1100,height=550,res=140);par(mfrow=c(1,2));r<-resid(fit,type="normalized");plot(fitted(fit),r,xlab="Fitted",ylab="Normalized residual");abline(h=0,lty=2);qqnorm(r);qqline(r);dev.off()
writeLines(c(paste("Subjects:",nlevels(d$id)),paste("Observations:",nrow(d)),paste("Mean structure:",mean_name),paste("Covariance:",best),paste("Subject-level baseline median:",cutoff),"Baseline grouping is exploratory and susceptible to regression to the mean; it is not evidence for a biological mechanism.",errors),file.path(out,"run.txt"))
capture.output(sessionInfo(),file=file.path(out,"session-info.txt"));print(mt);print(ct);print(tt)
