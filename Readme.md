# Sentiment Analys Project

## Introduction
Sentiment analysis is a pivotal aspect of understanding and interpreting
conversations, especially in customer service interactions where emotions
play a significant role in conveying the caller's concerns, frustrations, and
expectations. The sentiment of the calling party is crucial as it provides
insights into the emotional state and intent of the caller, allowing the
service provider to tailor the response appropriately to address the caller's
needs effectively and empathetically.
In this approach, we aim to analyse the sentiment of each utterance in a
conversation by leveraging a Large Language Model (LLM). The model
classifies every utterance for its sentiment based on a predefined table
associating sentiments with specific colours. The sentiments considered
include Upset, Frustrated, Hopeful, Grateful, Delighted, Calm, Reassuring,
Satisfied, and Neutral, each represented by a unique color code.

## Diagram
![alt text](https://github.com/BondiAi/Call-center/blob/dev/diagram.png)

## Sentiment Color Association Table
- <span style="color:red;">Upset</span>: Red (`#FF0000`)
- <span style="color:#FFA500;">Frustrated/Impatient</span>: Orange (`#FFA500`)
- <span style="color:#FFFF00;">Hopeful</span>: Yellow (`#FFFF00`)
- <span style="color:#90EE90;">Grateful</span>: Light Green (`#90EE90`)
- <span style="color:#00FF00;">Delighted</span>: Bright Green (`#00FF00`)
- <span style="color:#0000FF;">Calm</span>: Blue (`#0000FF`)
- <span style="color:#ADD8E6;">Reassuring</span>: Light Blue (`#ADD8E6`)
- <span style="color:#008000;">Satisfied</span>: Green (`#008000`)
- <span style="color:#F5F5DC;">Neutral</span>: Grey (`#F5F5DC`)

## Methodology
The LLM model receives the utterances of the conversation and classifies
the sentiment of each utterance using the sentiment-colour association
table. The model operates iteratively, processing each utterance
sequentially and updating the sentiment classification based on the
received utterance. Importantly, the model retains the memory of the
previous utterance, using it as context to understand the progression of
sentiments in the conversation. This contextual understanding is vital as it
allows the model to discern the nuances in the conversation flow and
adjust the sentiment classification of the subsequent utterances more
accurately.
This methodology ensures a dynamic and context-aware sentiment
analysis that reflects the evolving emotional states of the calling party
throughout the conversation. By maintaining the context of previous
utterances, the model can comprehend the subtleties and shifts in
sentiments, providing a more coherent and holistic representation of the
caller's emotions and intentions.

## Objective
The primary objective of this sentiment analysis is to enhance the
understanding of the caller's emotional journey during the interaction. By
accurately identifying and tracking the sentiments throughout the
conversation, service providers can gain valuable insights into the caller's
experiences, concerns, and satisfaction levels, enabling them to improve
their communication strategies, address concerns more effectively, and
ultimately, enhance the overall customer service experience.

## How to run
**Backend**

https://github.com/BondiAi/Call-center/blob/dev/fastapi/Readme.md

**Frontend**
