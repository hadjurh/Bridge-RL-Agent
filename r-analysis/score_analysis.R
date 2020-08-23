rm(list = ls())

require("magrittr")
require("ggplot2")

scores <- read.csv2("Documents/PFE/Bridge_RL_Agent/database/no_trump_1000_2018-07-09_17-18-55_1.game", sep = ",")

# Plot
g <- ggplot(data = scores, aes(Contract, NS)) + 
    geom_jitter(height = 0.3, width = 0.3, alpha = 0.18) +
    scale_x_discrete(limits = 7:13) +
    scale_y_discrete(limits = 0:13) + 
    geom_segment(aes(x = 6.5, y = 6.5, xend = 7.5, yend = 6.5), col = "blue") +
    geom_segment(aes(x = 7.5, y = 6.5, xend = 7.5, yend = 7.5), col = "blue") +
    geom_segment(aes(x = 7.5, y = 7.5, xend = 8.5, yend = 7.5), col = "blue") +
    geom_segment(aes(x = 8.5, y = 7.5, xend = 8.5, yend = 8.5), col = "blue") +
    geom_segment(aes(x = 8.5, y = 8.5, xend = 9.5, yend = 8.5), col = "blue") +
    geom_segment(aes(x = 9.5, y = 8.5, xend = 9.5, yend = 9.5), col = "blue") +
    geom_segment(aes(x = 9.5, y = 9.5, xend = 10.5, yend = 9.5), col = "blue") +
    geom_segment(aes(x = 10.5, y = 9.5, xend = 10.5, yend = 10.5), col = "blue") + 
    geom_segment(aes(x = 10.5, y = 10.5, xend = 11.5, yend = 10.5), col = "blue") +
    geom_segment(aes(x = 11.5, y = 10.5, xend = 11.5, yend = 11.5), col = "blue") +
    geom_segment(aes(x = 11.5, y = 11.5, xend = 12.5, yend = 11.5), col = "blue") +
    geom_segment(aes(x = 12.5, y = 11.5, xend = 12.5, yend = 12.5), col = "blue") +
    geom_segment(aes(x = 12.5, y = 12.5, xend = 13.5, yend = 12.5), col = "blue") 
g

# Winning games
winning <- scores[scores$Contract <= scores$NS,]
nrow(winning)
nrow(winning) / nrow(scores)
