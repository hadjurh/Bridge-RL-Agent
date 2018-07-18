rm(list = ls())

require(magrittr)
require(ggplot2)

setwd("Documents/documents_hugo/PFE/Bridge-RL-Agent/")

perf <- read.csv("performances/performances_2.csv", sep = ";")

perf <- perf[perf$Nb_of_games_learned <= 50e3,] %>% na.omit()
g <- ggplot() + 
    geom_point(data = perf, aes(x = Nb_of_games_learned, 
                                y = Agent_game_won / Nb_of_games_test),
               alpha = 0.3,
               color = "dodgerblue2") + 
    geom_point(data = perf, aes(x = Nb_of_games_learned, 
                                y = Random_game_won / Nb_of_games_test),
               alpha = 0.3, 
               color = "firebrick") + 
    guides(colour = guide_legend(override.aes = list(alpha = 1)))
g
