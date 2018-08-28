rm(list = ls())

require(magrittr)
require(ggplot2)

setwd("~/Documents/PFE/Bridge_RL_Agent")

#################
# Small sets
#################
perf2 <- read.csv("performances/performances_2.csv", sep = ";")
colnames(perf2) <- c("Games_Learned", "Games_Test", "Agent", "Random", "States_Recognized", "States_Total")
perf2_mean <- setNames(aggregate(. ~ perf2$Games_Learned, perf2[-1], mean), colnames(perf2))
perf2_mean <- rbind(perf2_mean, c(0, 1000, 300, 300, 0, 1))

perf3 <- read.csv("performances/performances_3_info.csv", sep = ";")
colnames(perf3) <- c("Games_Learned", "Games_Test", "Agent", "Random", "States_Recognized", "States_Total")
perf3_mean <- setNames(aggregate(. ~ perf3$Games_Learned, perf3[-1], mean), colnames(perf3))
perf3_mean <- rbind(perf3_mean, c(0, 1000, 300, 300, 0, 1))

plot_data_2 <- perf2_mean
plot_data_3 <- perf3_mean
g <- ggplot() + 
    geom_line(data = plot_data_2, size = 1, alpha = 1, 
              aes(x = Games_Learned, y = Agent / Games_Test, colour = "dodgerblue")) + 
    geom_line(data = plot_data_3, size = 1, alpha = 1, 
              aes(x = Games_Learned, y = Agent / Games_Test, colour = "dodgerblue4")) + 
    geom_line(data = plot_data_2, aes(x = Games_Learned, y = Random / Games_Test, colour = "firebrick4"), size = 1, 
                alpha = 1) + 
    xlab("Training time (number of games)") +
    ylab("Performance against heuristic strategy") +
    scale_colour_manual(name = '', guide = 'legend',
                    values = c('dodgerblue', "dodgerblue4", 'firebrick'), labels = c('Q-Learning Unknown Hands', 'Q-Learning Known Hands', 'Random Strategy')) +
    guides(colour = guide_legend(override.aes = list(alpha = 1))) +
    scale_x_continuous(breaks = c(0, 5000, 10000, 15000),
                       labels = c('0', '5,000', '10,000', '15,000')) +
    scale_y_continuous(breaks = c(0.3, 0.5, 0.7, 0.9)) +
    theme_classic() +
    theme(legend.justification = c(1, 0), 
          legend.position = c(0.95, 0.3),
          legend.text = element_text(size = 19),
          axis.text = element_text(size = 19),
          axis.title = element_text(size = 21))
g
ggsave("q-learning_perf.pdf", width = 22, height = 20, units = "cm")

g <- ggplot() + 
    geom_line(data = plot_data_2, aes(x = Games_Learned, y = States_Recognized / States_Total, colour = "dodgerblue"), 
              size = 1, alpha = 1) +
    geom_line(data = plot_data_3, aes(x = Games_Learned, y = States_Recognized / States_Total, colour = "dodgerblue4"), 
              size = 1, alpha = 1) +
    xlab("Training time (number of games)") +
    ylab("Ratio of recognized states") + 
    scale_colour_manual(name = '', guide = 'legend',
                        values = c('dodgerblue', "dodgerblue4"), labels = c('Q-Learning Unknown Hands', 'Q-Learning Known Hands')) +
    scale_x_continuous(breaks = c(0, 5000, 10000, 15000),
                       labels = c('0', '5,000', '10,000', '15,000')) +
    guides(colour = guide_legend(override.aes = list(alpha = 1))) +
    theme_classic() +
    theme(legend.justification = c(1, 0), 
          legend.position = c(0.95, 0.3),
          legend.text = element_text(size = 19),
          axis.text = element_text(size = 19),
          axis.title = element_text(size = 21)) 
g
ggsave("q-learning_states_recog.pdf", width = 22, height = 20, units = "cm")
#################

perf <- read.csv("performances/performances.csv", sep = ";")
colnames(perf) <- c("Games_Learned", "Games_Test", "Agent", "Random", "States_Recognized", "States_Total")
perf_mean <- setNames(aggregate(. ~ perf$Games_Learned, perf[-1], mean), colnames(perf))
perf_mean <- rbind(perf_mean, c(0, 1000, 300, 300, 0, 1))

plot_data <- perf_mean[perf_mean$Games_Learned <= 62000,] %>% na.omit()
g <- ggplot() + 
    geom_line(data = plot_data, size = 1, alpha = 1, 
              aes(x = Games_Learned, y = Agent / Games_Test, colour = "darkslateblue")) + 
    geom_line(data = plot_data, aes(x = Games_Learned, y = Random / Games_Test, colour = "firebrick4"), size = 1, 
              alpha = 1) + 
    geom_hline(yintercept = c(900.5/1000, 740/1000), color = c('dodgerblue', "dodgerblue4")) + 
    xlab("Training time (number of games)") +
    ylab("Performance against heuristic strategy") +
    scale_colour_manual(name = '', guide = 'legend',
                        values = c('darkslateblue','firebrick'), labels = c('Q-Learning Mix', 'Random Strategy')) +
    annotate("text", x = 40000, y = 0.915, label = "Q-Learning Unknown Hands Max", size = 7, colour = "dodgerblue") +
    annotate("text", x = 40000, y = 0.755, label = "Q-Learning Known Hands Max", size = 7, colour = "dodgerblue4") +
    guides(colour = guide_legend(override.aes = list(alpha = 1))) +
    scale_x_continuous(breaks = c(0, 20000, 40000, 60000),
                       labels = c('0', '20,000', '40,000', '60,000')) +
    theme_classic() +
    theme(legend.justification = c(1, 0), 
          legend.position = c(0.95, 0.3),
          legend.text = element_text(size = 19),
          axis.text = element_text(size = 19),
          axis.title = element_text(size = 21))
g
ggsave("q-learning_bis_perf.pdf", width = 22, height = 20, units = "cm")

plot_data[plot_data$Games_Learned == 9000,]$States_Total <- 24000
g <- ggplot(data = plot_data, aes(x = Games_Learned, y = States_Recognized / States_Total)) + 
    geom_line(size = 1, alpha = 1) +
    theme_classic() +
    theme(axis.text = element_text(size = 19),
          axis.title = element_text(size = 21)) +
    scale_x_continuous(breaks = c(0, 20000, 40000, 60000),
                       labels = c('0', '20,000', '40,000', '60,000')) +
    scale_y_continuous(breaks = c(0, 0.25, 0.5)) +
    # scale_x_continuous(breaks = c(0, 1000, 2000, 3000),
    #                    labels = c('0', '1,000', '2,000', '3,000')) +
    xlab("Training time (number of games)") +
    ylab("Ratio of recognized states")
g
ggsave("q-learning_bis_states_recog.pdf", width = 22, height = 20, units = "cm")
