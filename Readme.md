## Otonasalone-english-quiz

### What's this ?
Fetch new English quizzes in [OTONA SALONE website](https://otonasalone.jp/tags/ichinichiichieigo/) and send them on LINE

##### Sample distributed message
```
英語「甘やかさないで」はなんて言う？
↓
↓
↓
英語で「甘やかさないで」＝Don't spoil

https://otonasalone.jp/456634/
```

### Prerequisites

Set information below in environment variable

- OPENAI\_API\_KEY
    - API key generated in OpenAI platform
- LINE\_CHANNEL\_ACCESS\_TOKEN
    - Channel access token of Messaging API generated in LINE Developers console
- LINE\_TARGET\_USER\_ID (Optional)
    - The LINE UID is a 33-character string starting with "U," issued by the LINE platform
    - This is different from the display name or LINE ID used for friend searches
```
export OPENAI_API_KEY=YOUR_OPENAI_API_KEY
export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
export LINE_TARGET_USER_ID=YOUR_LINE_USER_ID
```

### Get started

1. Install required packages
    ```
    $ pip install -r requirements.txt
    ```
1. Create database
    ```
    $ python create_db.py
    ```
1. Get new articles and send messages on LINE
    ```
    $ python main.py
    ```
