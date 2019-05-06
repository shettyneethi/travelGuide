
## Travel Recommendation System <br />
This repository is an implementation of travel based recommendation system. This is an attempt to recommend places by including following features:<br />
- Past and Current weather data <br />
- Twitter popularity <br />
- TripAdvisor reviews <br />
### Demo link <br />
  https://youtu.be/RrdsDVKTWQU
### website hosted at <br />

### Dataset <br />
- Scrapped TripAdvisor's reviews for selected places from 4 states: Colorado, California, Arizona, New York <br />
- Collected tweets for the same places using Twitter REST API
- Collected weather data on a monthly basis averaged over past 12 years from WorldWeatherOnline API
- Collected one recent image per location by scraping Instagram
- Generated latitude and longitude for these places using OpenCage API

### Design <br />

![Architrcture Diagram 1](https://user-images.githubusercontent.com/45861860/57256912-2f32e700-7015-11e9-9e61-f3dd5c6454d4.jpg)

- Created various collections for each kind and stored the above mentioned dataset in MongoDB Atlas cluster hosted on GCP
- Used VADER for sentiment analysis of TripAdvisor's reviews and generated an overall score for a place by giving importance more recent reviews and reviews having more upvotes.
- Our algorithm gives more weightage to tweets over reviews from TripAdvisor. 








