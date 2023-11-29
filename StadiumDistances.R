#install.packages("geosphere")
library(geosphere)
#distm (c(lon1, lat1), c(lon2, lat2), fun = distHaversine)

# Data source: https://github.com/gboeing/data-visualization/blob/main/ncaa-football-stadiums/data/stadiums-geocoded.csv
data <- read.csv("stadiums-geocoded.csv")

big10 <- subset(data, data$conference %in% "Big Ten")
teams <- big10$team

dist <- matrix(nrow = 14, ncol = 14)

for (i in 1:14) {
  for (j in 1:14) {
    # Distance between point i and j "as the crow flies"
    dist[i, j] <- distm (c(big10$longitude[i], big10$latitude[i]), c(big10$longitude[j], big10$latitude[j]), fun = distHaversine)
  }
}

# convert to km
dist <- dist/1000.0

dist <- format(round(dist, 4), nsmall=4)

row.names(dist) <- teams
colnames(dist) <- teams

write.csv(dist, file="Big10Distances.csv")

