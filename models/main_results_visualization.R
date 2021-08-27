#export the figs from main results to figures
#1. require packages ----
library('tidyverse')
library('ggpubr')
library(rms)
# library(htmltab)
#2. pre-functions ----

getor <- function(df, cilevel = c(0.025,0.975)){
  df %>%
    mutate(or = exp(mean),
           or.min = exp(mean + qnorm(cilevel[1])*sd ),
           or.max = exp(mean + qnorm(cilevel[2])*sd ))
}

get_model_stats = function(x) {
  cap = capture.output(print(x))
  
  #model stats
  stats = c()
  stats$R2.adj = str_match(cap, "R2 adj\\s+ (\\d\\.\\d+)") %>% na.omit() %>% .[, 2] %>% as.numeric()
  
  #coef stats lines
  coef_lines = cap[which(str_detect(cap, "Coef\\s+S\\.E\\.")):(length(cap) - 1)]
  
  #parse
  coef_lines_table = suppressWarnings(readr::read_table(coef_lines %>% stringr::str_c(collapse = "\n")))
  colnames(coef_lines_table)[1] = "Predictor"
  
  list(
    stats = stats,
    coefs = coef_lines_table
  )
}
#3. aadt forest flot ----
# df = read.csv('C:/Users/zhang/Box\ Sync/Workzone\ (zhuoran1@andrew.cmu.edu)/Paper_2019/figs/aadt_ors.csv')

wzid_new_list <- readRDS(file = "./outputData/wzid_new_list.rds")

df <- data.frame(aadt = c('All', '(0, 10,000]','(10,000, 20,000]','(20,000, ...)'),mean = c(get_model_stats(df_raw[1])$coefs[[2,2]],                                                                 get_model_stats(df_raw[2])$coefs[[2,2]],                                                                 get_model_stats(df_raw[3])$coefs[[2,2]],                                                                  get_model_stats(df_raw[4])$coefs[[2,2]]),
        sd = c(get_model_stats(df_raw[1])$coefs[[2,3]],
               get_model_stats(df_raw[2])$coefs[[2,3]],
               get_model_stats(df_raw[3])$coefs[[2,3]],
               get_model_stats(df_raw[4])$coefs[[2,3]]))

df$aadt <- as.character(df$aadt)
df$aadt <- factor(df$aadt, levels=unique(df$aadt))

getor(df)  %>%
  ggplot(aes(x = or, y = aadt)) + 
  geom_line()+geom_point()+
  # geom_text(hjust=0, vjust=2,color='blue')+
  geom_errorbarh(aes(xmin=or.min, xmax=or.max), height=.1)+
  geom_vline(xintercept=1, linetype="dashed",color = "red",size=1)+
  # scale_linetype_manual(name = 'Legend',values = c(dashed = "dashed"), labels = c("Same crash occurrence"))+
  xlab("Odds ratio") + ylab("AADT(vehicles per day)") +theme_minimal()
ggsave("./figs2021/aadt_ors.png",width = 20, height = 15, units = "cm")



#4. daytime ----

df_raw <- readRDS(file = "./outputData/results_aadt_daytime.rds")

df <- data.frame(aadt = c('All', '(0, 10,000]','(10,000, 20,000]','(20,000, ...)',
                          'All','(10,000, 20,000]','(20,000, ...)'),
                 mean = c(get_model_stats(df_raw[2])$coefs[[2,2]],                                                              get_model_stats(df_raw[3])$coefs[[2,2]],                                                              get_model_stats(df_raw[5])$coefs[[2,2]],                                                              get_model_stats(df_raw[7])$coefs[[2,2]],
                          get_model_stats(df_raw[1])$coefs[[2,2]],
                          get_model_stats(df_raw[4])$coefs[[2,2]],
                          get_model_stats(df_raw[6])$coefs[[2,2]]),
                 sd = c(get_model_stats(df_raw[2])$coefs[[2,3]],
                        get_model_stats(df_raw[3])$coefs[[2,3]],
                        get_model_stats(df_raw[5])$coefs[[2,3]],
                        get_model_stats(df_raw[7])$coefs[[2,3]],
                        get_model_stats(df_raw[1])$coefs[[2,3]],
                        get_model_stats(df_raw[4])$coefs[[2,3]],
                        get_model_stats(df_raw[6])$coefs[[2,3]]),
                 group = c('day','day','day','day','night','night','night'))

# df = read.csv('C:/Users/zhang/Box\ Sync/Workzone\ (zhuoran1@andrew.cmu.edu)/Paper_2019/figs/daytime_ors.csv')
df$aadt <- as.character(df$aadt)
df$aadt <- factor(df$aadt, levels=unique(df$aadt))

getor(df)  %>%
  ggplot(aes(y = or, x = aadt,color = group)) + 
  geom_point(position = position_dodge(width=0.15))+
  geom_errorbar(aes(ymin=or.min, ymax=or.max),width=0.2,position = position_dodge(0.15))+
  geom_hline(yintercept=1, linetype="dashed", 
             color = "red", size=1)+
  ylab("Odds ratio") + xlab("AADT(vehicles per day)")+ coord_flip()+theme_minimal()
ggsave("./figs2021/daytime_ors.png",width = 20, height = 15, units = "cm")


#5. length ----
df_raw <- readRDS(file = "./outputData/results_aadt_length.rds")

df <- data.frame(aadt = c('All', '(0, 10,000]','(10,000, 20,000]','(20,000, ...)',
                          'All', '(0, 10,000]','(10,000, 20,000]','(20,000, ...)'),
                 mean = c(get_model_stats(df_raw[2])$coefs[[2,2]],                                                              get_model_stats(df_raw[4])$coefs[[2,2]],                                                              get_model_stats(df_raw[6])$coefs[[2,2]],                                                              get_model_stats(df_raw[8])$coefs[[2,2]],
                          get_model_stats(df_raw[1])$coefs[[2,2]],
                          get_model_stats(df_raw[3])$coefs[[2,2]],
                          get_model_stats(df_raw[5])$coefs[[2,2]],
                          get_model_stats(df_raw[7])$coefs[[2,2]]),
                 sd = c(get_model_stats(df_raw[2])$coefs[[2,3]],
                        get_model_stats(df_raw[4])$coefs[[2,3]],
                        get_model_stats(df_raw[6])$coefs[[2,3]],
                        get_model_stats(df_raw[8])$coefs[[2,3]],
                        get_model_stats(df_raw[1])$coefs[[2,3]],
                        get_model_stats(df_raw[3])$coefs[[2,3]],
                        get_model_stats(df_raw[5])$coefs[[2,3]],
                        get_model_stats(df_raw[7])$coefs[[2,3]]),
                 group = c('long','long','long','long','short','short','short','short'))


df$aadt <- as.character(df$aadt)
df$aadt <- factor(df$aadt, levels=unique(df$aadt))

getor(df) %>%
  ggplot(aes(y = or, x = aadt,color = group)) + 
  geom_point(position = position_dodge(width=0.15))+
  geom_errorbar(aes(ymin=or.min, ymax=or.max),width=0.2,position = position_dodge(0.15))+
  geom_hline(yintercept=1, linetype="dashed", 
             color = "red", size=1)+
  ylab("Odds ratio") + xlab("AADT(vehicles per day)")+ coord_flip()+theme_minimal()
ggsave("./figs2021/length_ors.png",width = 20, height = 15, units = "cm")
