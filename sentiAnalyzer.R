#!/usr/bin/env Rscript
#COMMAND TO RUN : Rscript --vanilla sentiAnalyzer.R 'Colorado National Monument'
args = commandArgs(trailingOnly=TRUE)
library(tm)
library(mongolite)
library(dplyr)
library(ggplot2)
library(stringr)
library(SnowballC) # Provides wordStem() for stemming.
library(RColorBrewer) 


df <- mongo(collection = "REVIEWS", db="DATASET")
#"Colorado National Monument"
place = args[1]
print(place)
df <- df$find(
  query = paste('{"NAME" : "',place , '"}', sep=""),
  fields = '{"REVIEWS" : true}'
)


docs <- df$REVIEWS[[1]][3][,1]
docs <- Corpus(VectorSource(docs))


###########################################################################################
# Data Cleaning - Applying Transformations
###########################################################################################
toSpace <- content_transformer(function(x, pattern) gsub(pattern, " ", x))
docs <- tm_map(docs, toSpace, "/|@|//|$|:|:)|*|&|!|?|_|-|#|")  ## replace special characters by space
docs <- tm_map(docs, content_transformer(tolower)) # Conversion to Lower Case
docs <- tm_map(docs, removePunctuation) # Punctuation can provide gramatical context which supports 
docs <- tm_map(docs, removeWords, stopwords("english")) # common stop Words like for, very, and, of, are, etc,
docs <- tm_map(docs, removeWords, c("the", "will", "The", "also", "that", "and", "for", "in", "is", "it", "not", "to"))
docs <- tm_map(docs, removeNumbers) # removal of numbers
docs <- tm_map(docs, stripWhitespace) # removal of whitespace
docs <- tm_map(docs, stemDocument) # Stemming uses an algorithm that removes common word endings for English

dtm <- DocumentTermMatrix(docs)
tdm <- TermDocumentMatrix(docs)

freq <- sort(colSums(as.matrix(dtm)), decreasing=TRUE)


##########################################################################################
# 								WORD FREQ GRAPH
#########################################################################################



wf <- data.frame(word=names(freq), freq=freq)
png("wordFreqPlot.png")

wordFreqPlot <-barplot(wf[1:20,]$freq, las = 2, 
        names.arg = wf[1:20,]$word,
        col ="lightblue", main ="Most frequent words",
        ylab = "Word frequencies")

# wordFreqPlot <- subset(wf, freq>10)    %>% #this results in crowding in x axis
#         ggplot(aes(word, freq)) +
#         geom_bar(stat="identity", fill="darkred", colour="darkgreen") +
#         theme(axis.text.x=element_text(angle=90, hjust=1))
print(wordFreqPlot)
dev.off()

# ##########################################################################################
# # 								WORD CLOUD
# #########################################################################################

library(wordcloud)
set.seed(100)
png("wordcloud.png")
wordCloudPic <- wordcloud(names(freq), freq, min.freq=10, max.words=100,colors=brewer.pal(6, "Dark2"))
print(wordCloudPic)
dev.off()

# ########################################################################################
# #								POPULAR MONTH GRAPH
# # ########################################################################################
months <- c("January","February","March","April","May","June","July","August","September","October","November","December")
count_df =  data.frame(Month = factor(), Popularity = numeric()) 

review_dates <- df$REVIEWS[[1]]$DATE
review_dates <- word(review_dates,1)
month_freq <- as.data.frame(table(review_dates)) 

for( i in 1:length(months)){
	count_df <- rbind(count_df, data.frame(Month = month_freq[which(month_freq$review_dates == months[i]),][[1]], Popularity = month_freq[which(month_freq$review_dates == months[i]),][[2]]))
}

ggplot(count_df,aes(factor(Month,level = Month), Popularity)) +
        geom_bar(stat="identity", fill="darkred", colour="darkgreen") +
        theme(axis.text.x=element_text(angle=45, hjust=1))
ggsave("popularMonthGraph.png")


# ###############################################################################
# #								TEST
# ###############################################################################
# # month <- "2009-03"
# # as.Date(paste(month,"-01",sep=""))


# # review_dates <- df$REVIEWS[[1]]$DATE

# # review_dates <- word(review_dates,1)


# # review_dates_mod <- paste("01",review_dates, sep=" ")
# # review_dates_mod<- as.Date(review_dates,"%d %B %Y")


# # dim(df$REVIEWS[[1]]); min(review_dates); max(review_dates)

# # ggplot(review_dates,aes(DATE, n)) + ggtitle('The Number of Reviews Per Week')






