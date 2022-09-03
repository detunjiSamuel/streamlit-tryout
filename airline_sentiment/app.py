import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

data_path = 'tweets.csv'

# Main
st.title("Sentiment Analysis of tweets on U.S Airlines")
st.markdown("Streamlit based dashboard to analyze U.S Airlines tweets sentiment ")

# Sidebar
st.sidebar.title("Sentiment Analysis of Tweets")
st.sidebar.markdown("This application is a Streamlit dashboard used "
                    "to analyze sentiments of tweets ")


@st.cache(persist=True)
def get_data():
    data = pd.read_csv(data_path)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data


data = get_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio(
    'Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query(
    "airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])

st.sidebar.subheader("Number of Tweet by  Sentiment")
select = st.sidebar.selectbox(
    'Visualization type', ['Bar plot', 'Pie chart'], key='1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame(
    {'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide", False):
    st.markdown("### Number of Tweet by  Sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment',
                     y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)


st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Hide", False, key="2"):
    st.markdown("### Tweet locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" %
                (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Total number of tweets for each airline")
selected_airline_chart = st.sidebar.selectbox(
    'Visualization type', ['Bar plot', 'Pie chart'], key='airline_tweet_count_chart')
airline_sentiment_count = data.groupby(
    'airline')['airline_sentiment'].count().sort_values(ascending=False)
airline_sentiment_count = pd.DataFrame(
    {'Airline': airline_sentiment_count.index, 'Tweets': airline_sentiment_count.values.flatten()})

if not st.sidebar.checkbox("Hide", False, key='airline_tweet_count'):
    if selected_airline_chart == 'Bar plot':
        st.subheader("Total number of tweets for each airline")
        fig_1 = px.bar(airline_sentiment_count, x='Airline',
                       y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig_1)
    else:
        st.subheader("Total number of tweets for each airline")
        fig_2 = px.pie(airline_sentiment_count,
                       values='Tweets', names='Airline')
        st.plotly_chart(fig_2)


st.sidebar.header("Word Cloud")
# it was showing errors after plot
st.set_option('deprecation.showPyplotGlobalUse',
              False)
word_sentiment = st.sidebar.radio(
    'Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
if not st.sidebar.checkbox("Hide", False, key='sentiment_word_cloud'):
    st.subheader(f'Word cloud for {word_sentiment} sentiment')
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    # avoid - retweets , links , tweets calling a specifc user
    processed_words = ' '.join([word for word in words.split(
    ) if 'http' not in word and not word.startswith('@') and word != 'RT'])
    # st.write(processed_words)
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white',
                          width=800, height=640).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()


st.sidebar.subheader("Airline Tweet by sentiment")
choice = st.sidebar.multiselect("Choose Airline", ("US Airways", "United",
                                "American", "Southwest", "Delta", "Virgin America"), key="0")

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count", color="airline_sentiment",
                              facet_col="airline_sentiment", labels={"airline_sentiment": "tweets"}, height=600, width=800)
    st.plotly_chart(fig_choice)
