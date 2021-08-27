strati_regress <- function(formula, data) {
    fitlrm1.months_obs<- lrm(as.formula(formula),
                           x = T,
                           y = T,
                           data = data)
    return (robcov(fitlrm1.months_obs, cluster = data$wzid_new))

}

visualize_func <- function(x = 'real_speed_61_detreat_ind', xname = "Actual speed detreated 2 (mph) ",
                           y = 'crash_61', y_transform = 'logodds', yname = "Log odds of crash occurrence", digits_form = 0.5,
                           data = df[wzid_new<100000000 & location=='in' & avet_exists==1 & speed_61_exists==1] ) {
  
  rawpoints <- data %>%
    select(treatment_use,!!y,!!x)%>%
    mutate(temp:=as.integer(get(x)*digits_form)/digits_form) %>%  
    group_by(treatment_use,temp) %>%
    summarise(prop := mean(get(y)),sd :=sd(get(y)),
              logodds:=log(mean(get(y))/(1-mean(get(y)))),
              crash_counts:=sum(get(y)),
              logodds_sd := sqrt(1/sum(get(y))+1/(n()-sum(get(y))))) %>%
    select(treatment_use,temp,logodds,prop)
  
  picture<-
    ggplot() +
    geom_point( data = rawpoints,aes(x=temp,y=get(y_transform),group = factor(treatment_use),color=factor(treatment_use)))+
    # geom_smooth()+
    theme_minimal()+
    scale_x_continuous(name = xname)+
    scale_color_manual(labels = c("No", "Yes"), values = c("blue", "red"))+
    labs(x = "",y = yname,col="Roadwork")+
    theme(legend.position="bottom")
  
  results <- list(picture)
  # names(results) <- c("rawpoints","picture")
  
  return(results)
}

trimlatexoutput <- function(filename = "output/fading_comparison_1hour.tex"){

    texfile = readtext::readtext(filename)
    tex = str_replace_all(texfile$text,coll("\n\\begin{table}[!htbp] \\centering \n  \\caption{} \n  \\label{} "),'')
    tex = str_replace_all(tex, coll("\n\\end{table}"),'')
    # if (i<=7){
    #   tex = str_replace_all(tex,coll("& \\multicolumn{2}{c}{crash\\_61}"),'')
    #   tex = str_replace_all(tex,coll(" \\multicolumn{1}{c}{Crash occurrence}"),
    #                         ' \\multicolumn{3}{c}{Crash occurrence}')
    # }else{
    #   tex = str_replace_all(tex,coll("& \\multicolumn{1}{c}{crash\\_61}"),'')
    #   tex = str_replace_all(tex,coll(" \\multicolumn{1}{c}{Crash occurrence}"),
    #                         ' \\multicolumn{2}{c}{Crash occurrence}')    }
    
    sink(file=filename)
    cat(tex)
    sink()
   
}

hist_ggplot <- function(variablename,data,density = FALSE ){
    if(density){
    pic <- ggplot(data, aes(x=get(variablename))) + 
            geom_histogram(aes(x=get(variablename),y = (..density..)),colour="black", fill="white")+
             geom_density(alpha=.2, fill="#FF6666") + 
             labs(x = variablename)+
             theme_minimal()
    return(list(pic))
    }else{
    pic <- ggplot(data, aes(x=get(variablename))) + 
            geom_histogram(aes(x=get(variablename)),colour="black", fill="white")+
             labs(x = variablename)+
             theme_minimal()
    return(list(pic))
    }

# TODO: use the 2nd y axis to combine density and frequency, make sure that these graphs can be combined as facewarp later
}
