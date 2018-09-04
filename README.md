# NeuroBasnya

## In English:
LSTM-neural network, trained on the corpus of fables of different nations. 5 models are available - Armenian, Indian, Sufi, Hasidic and Jewish.

The corpora of the fables are small, so 200 iterations was enough to get the Russian words on a char-level LSTM.


### Files in the directory:

examples.zip - examples of nagenienny texts.

training.zip - data for training

flask_app.py - bot code for telegrams.

lstm_for_generating_text.py - LSTM

---

## По-русски:
LSTM-нейросеть, обученная на корпусе басен разных народов. Всего 5 моделей - армянская, индийская, суфийская, хасидская и еврейская.

Корпуса басен небольшие, поэтому 200 итераций было вполне достаточно, чтобы на посимвольной LSTM получить русские слова.

Это мой первый опыт работы с нейросетями. 
Лучше всего работают армянская и еврейская модель, для остальных чуть хуже, потому что я не успела нагенерить "разумных текстов" для них - разумных, в данном случае, это начинающихся с "\n" и заканчивающихся точкой. 
Еще через день нагенерю, и тогда это будет выглядеть чуть приличнее. Генерация текста происходит очень медленно, почти так же, как обучение.

## Файлы в директории:

examples.zip - примеры нагенеренных текстов.

training.zip - данные для обучения

flask_app.py - код бота для телеграм.

lstm_for_generating_text.py - LSTM
