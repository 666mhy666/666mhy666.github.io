# Revised from Heyang Ma's UCLA longitudinal analysis.
# Usage: Rscript analysis.R path/to/riesby.csv results
suppressPackageStartupMessages(library(nlme))
args<-commandArgs(trailingOnly=TRUE)
if(length(args)<1)stop("Supply a CSV exported from multilevelmod::riesby; see DATA_ACCESS.md")
out<-if(length(args)>1)args[2] else "results"
dir.create(out,recursive=TRUE,showWarnings=FALSE)
d<-read.csv(args[1]);required<-c("subject","week","depr_score","endogenous","imipramine","desipramine")
stopifnot(all(required %in% names(d)))
input_n<-nrow(d);d<-d[complete.cases(d[,required]),required]
d$subject<-factor(d$subject);d$endogenous<-factor(d$endogenous)
d<-d[order(d$subject,d$week),];d$visit<-match(d$week,sort(unique(d$week)))
stopifnot(!anyDuplicated(d[c("subject","week")]))
control<-lmeControl(maxIter=200,msMaxIter=200,returnObject=FALSE)
safe_fit<-function(expr)tryCatch(expr,error=function(e)structure(list(message=conditionMessage(e)),class="failed_fit"))
model_table<-function(models)do.call(rbind,lapply(names(models),function(nm){
 m<-models[[nm]]
 if(inherits(m,"failed_fit"))return(data.frame(model=nm,AIC=NA,BIC=NA,n=NA,status=m$message))
 data.frame(model=nm,AIC=AIC(m),BIC=BIC(m),n=nobs(m),status="converged")
}))
# Different fixed effects are compared using ML on the same complete-case cohort.
formulas<-list(diagnosis=depr_score~week+endogenous,
 diagnosis_interaction=depr_score~week*endogenous,
 imipramine=depr_score~week*imipramine+endogenous,
 desipramine=depr_score~week*desipramine+endogenous,
 both=depr_score~week*desipramine+imipramine+endogenous)
mean_models<-lapply(formulas,function(f)safe_fit(lme(f,data=d,random=~1|subject,method="ML",control=control)))
write.csv(model_table(mean_models),file.path(out,"mean-models-ml.csv"),row.names=FALSE)
# The original drug-by-time question is held fixed across all covariance candidates.
fixed<-formulas$desipramine
models<-list(
 RI=safe_fit(lme(fixed,data=d,random=~1|subject,method="REML",control=control)),
 RIAS=safe_fit(lme(fixed,data=d,random=~week|subject,method="REML",control=control)),
 CS=safe_fit(gls(fixed,data=d,correlation=corCompSymm(form=~1|subject),method="REML")),
 AR1=safe_fit(lme(fixed,data=d,random=~1|subject,correlation=corAR1(form=~week|subject),method="REML",control=control)),
 ARH1=safe_fit(lme(fixed,data=d,random=~1|subject,correlation=corAR1(form=~week|subject),weights=varIdent(form=~1|week),method="REML",control=control)),
 UN=safe_fit(gls(fixed,data=d,correlation=corSymm(form=~visit|subject),weights=varIdent(form=~1|week),method="REML")))
comparison<-model_table(models);write.csv(comparison,file.path(out,"covariance-models.csv"),row.names=FALSE)
best<-comparison$model[which.min(comparison$BIC)];fit<-models[[best]]
tt<-as.data.frame(summary(fit)$tTable);tt$term<-rownames(tt);rownames(tt)<-NULL
df_col<-if("DF" %in% names(tt))tt$DF else rep(nrow(d)-length(coef(fit)),nrow(tt))
tt$lower<-tt$Value-qt(.975,df_col)*tt$Std.Error;tt$upper<-tt$Value+qt(.975,df_col)*tt$Std.Error
write.csv(tt,file.path(out,"coefficients.csv"),row.names=FALSE)
summaries<-do.call(rbind,lapply(split(d,list(d$week,d$endogenous),drop=TRUE),function(x){
 data.frame(week=x$week[1],diagnosis=as.character(x$endogenous[1]),n=nrow(x),mean=mean(x$depr_score),se=sd(x$depr_score)/sqrt(nrow(x)))
}))
write.csv(summaries,file.path(out,"weekly-means.csv"),row.names=FALSE)
png(file.path(out,"depression-trajectories.png"),width=1100,height=700,res=150)
plot(range(d$week),range(c(summaries$mean-summaries$se,summaries$mean+summaries$se)),type="n",xlab="Week",ylab="Mean change in depression score",main="Descriptive mean changes by diagnosis group")
for(g in levels(d$endogenous)){s<-summaries[summaries$diagnosis==g,];s<-s[order(s$week),];color<-c("#23597a","#ad6b34")[match(g,levels(d$endogenous))];lines(s$week,s$mean,type="b",pch=16,col=color,lwd=2);arrows(s$week,s$mean-s$se,s$week,s$mean+s$se,angle=90,code=3,length=.05,col=color)}
legend("topright",c("Non-endogenous","Endogenous"),col=c("#23597a","#ad6b34"),lty=1,pch=16,bty="n");dev.off()
png(file.path(out,"diagnostics.png"),width=1200,height=900,res=140);par(mfrow=c(2,2))
r<-resid(fit,type="normalized");plot(fitted(fit),r,xlab="Fitted",ylab="Normalized residual");abline(h=0,lty=2)
qqnorm(r);qqline(r);plot(d$week,r,xlab="Week",ylab="Normalized residual");abline(h=0,lty=2);hist(r,main="Normalized residuals",xlab="Residual");dev.off()
writeLines(c(paste("Input rows:",input_n),paste("Complete rows:",nrow(d)),paste("Subjects:",nlevels(d$subject)),paste("Selected covariance:",best),"Fixed effects: depr_score ~ week * desipramine + endogenous","Associations only. P-values and intervals do not account for model selection."),file.path(out,"run.txt"))
capture.output(sessionInfo(),file=file.path(out,"session-info.txt"));print(comparison);print(tt)
