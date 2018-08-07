rm(list = ls())

require(magrittr)
require(ggplot2)

setwd("~/Documents/documents_hugo/PFE/Bridge_RL_Agent")

perf <- read.csv("performances/performances_2.csv", sep = ";")
colnames(perf) <- c("Games_Learned", "Games_Test", "Agent", "Random", "States_Recognized", "States_Total")
perf_mean <- setNames(aggregate(. ~ perf$Games_Learned, perf[-1], mean), colnames(perf))

plot_data <- perf[perf$Games_Learned < 50000,] %>% na.omit()
g <- ggplot() + 
    geom_jitter(data = plot_data, size = 2, width = 30, alpha = 0.1, 
                aes(x = Games_Learned, y = Agent / Games_Test, colour = "dodgerblue1")) + 
    geom_jitter(data = plot_data, aes(x = Games_Learned, y = Random / Games_Test, colour = "firebrick4"), size = 2, width = 30, 
                alpha = 0.1) + 
    geom_smooth(data = plot_data,
                aes(x = Games_Learned, y = Agent / Games_Test),colour = "dodgerblue4") +
    xlab("Number of games used to learn") +
    ylab("Performance") +
    scale_colour_manual(name = '', guide = 'legend',
                    values = c('dodgerblue1', 'firebrick'), labels = c('RL Agent against heuristic', 'Random Strategy against heuristic')) +
    guides(colour = guide_legend(override.aes = list(alpha = 1)))
g

g <- ggplot(data = plot_data, aes(x = Games_Learned, y = States_Recognized / States_Total)) + 
    geom_point(size = 2, alpha = 0.1) + 
    geom_smooth() +
    xlab("Number of games used to learn") +
    ylab("% of states recognized")
g
