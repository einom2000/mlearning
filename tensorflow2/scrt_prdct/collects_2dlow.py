import os
import random
from collections import deque

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, Bidirectional
from tensorflow.keras.layers import LSTM
from tensorflow.keras.models import Sequential

import day_to_csv
import remove_file
import tool_day_off_filter
import tool_get_per_of_300


def shuffle_in_unison(a, b):
    # shuffle two arrays in the same way
    state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(state)
    np.random.shuffle(b)


def load_data(ticker, n_steps=50, scale=True, shuffle=True, lookup_step=1, split_by_date=True,
                test_size=0.2,
              feature_columns=('adjclose', 'volume', 'open', 'high', 'low', "pct_index_300", "pct_vol_300")):
    date_now = tool_day_off_filter.get_date_now()
    if isinstance(ticker, str):
        if os.path.isfile('csv-original\\' + ticker + '_' + date_now + '.csv'):
            df = pd.read_csv('csv-original\\' + ticker + '_' + date_now + '.csv')
        else:
            remove_file.remove('csv-original\\', startwith=ticker)
            day_to_csv.day_to_csv(single_code=ticker[2:], market=ticker[:2])
            # put 300 index growing percent to the csv
            tool_get_per_of_300.join_300(ticker)
            df = pd.read_csv('csv-original\\' + ticker + '_' + date_now + '.csv')
    elif isinstance(ticker, pd.DataFrame):
        df = ticker
    else:
        print(ticker)
        raise TypeError("ticker can be either a str or a `pd.DataFrame` instances")
    # this will contain all the elements we want to return from this function
    result = {}
    # we will also return the original dataframe itself
    result['df'] = df.copy()
    # make sure that the passed feature_columns exist in the dataframe
    for col in feature_columns:
        assert col in df.columns, f"'{col}' does not exist in the dataframe."
    # add date as a column
    if "date" not in df.columns:
        df["date"] = df.index
    if scale:
        column_scaler = {}
        # scale the data (prices) from 0 to 1
        for column in feature_columns:
            scaler = preprocessing.MinMaxScaler()
            df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
            column_scaler[column] = scaler
        # add the MinMaxScaler instances to the result returned
        result["column_scaler"] = column_scaler
    # add the target column (label) by shifting by `lookup_step`
    # defending by fredict the lowest tomorrow============================================================
    df['future'] = df['low'].shift(-lookup_step)
    # last `lookup_step` columns contains NaN in future column
    # get them before droping NaNs
    last_sequence = np.array(df[feature_columns].tail(lookup_step))
    # drop NaNs
    df.dropna(inplace=True)
    sequence_data = []
    sequences = deque(maxlen=n_steps)
    for entry, target in zip(df[feature_columns + ["date"]].values, df['future'].values):
        sequences.append(entry)
        if len(sequences) == n_steps:
            sequence_data.append([np.array(sequences), target])
    # get the last sequence by appending the last `n_step` sequence with `lookup_step` sequence
    # for instance, if n_steps=50 and lookup_step=10, last_sequence should be of 60 (that is 50+10) length
    # this last_sequence will be used to predict future stock prices that are not available in the dataset
    last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
    last_sequence = np.array(last_sequence).astype(np.float32)
    # add to result
    result['last_sequence'] = last_sequence
    # construct the X's and y's
    X, y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        y.append(target)
    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    if split_by_date:
        # split the dataset into training & testing sets by date (not randomly splitting)
        train_samples = int((1 - test_size) * len(X))
        result["X_train"] = X[:train_samples]
        result["y_train"] = y[:train_samples]
        result["X_test"]  = X[train_samples:]
        result["y_test"]  = y[train_samples:]
        if shuffle:
            # shuffle the datasets for training (if shuffle parameter is set)
            shuffle_in_unison(result["X_train"], result["y_train"])
            shuffle_in_unison(result["X_test"], result["y_test"])
    else:
        # split the dataset randomly
        result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y,
                                                                                test_size=test_size, shuffle=shuffle)
    # get the list of test set dates
    dates = result["X_test"][:, -1, -1]
    # retrieve test features from the original dataframe
    result["test_df"] = result["df"].loc[dates]
    # remove dates from the training/testing sets & convert to float32
    result["X_train"] = result["X_train"][:, :, :len(feature_columns)].astype(np.float32)
    result["X_test"] = result["X_test"][:, :, :len(feature_columns)].astype(np.float32)
    return result


def create_model(sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            # first layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
            else:
                model.add(cell(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            # last layer
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=False)))
            else:
                model.add(cell(units, return_sequences=False))
        else:
            # hidden layers
            if bidirectional:
                model.add(Bidirectional(cell(units, return_sequences=True)))
            else:
                model.add(cell(units, return_sequences=True))
        # add dropout after each layer
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
    return model


def plot_graph(test_df, plot_filename):
    """
    This function plots true close price along with predicted close price
    with blue and red colors respectively
    """
    # plt.plot(test_df[f'true low_{LOOKUP_STEP}'], c='b')
    # plt.plot(test_df[f'low_{LOOKUP_STEP}'], c='r')
    # plt.xlabel("Days")
    # plt.ylabel("Price")
    # plt.legend(["Actual Price", "Predicted Price"])
    # plt.savefig(plot_filename)
    pass

def get_final_df(model, data):
    """
    This function takes the `model` and `data` dict to
    construct a final dataframe that includes the features along
    with true and predicted prices of the testing dataset
    """
    # if predicted future price is higher than the current,
    # then calculate the true future price minus the current price, to get the buy profit
    reachability = lambda currentlow, true_futurelow, pred_futurelow: true_futurelow - pred_futurelow
    # a positive reachability means predicted high are reachable
    reachability_2 = lambda ccurrentlow, true_futurelow, pred_futurelow: true_futurelow - pred_futurelow * 1.005
    X_test = data["X_test"]
    y_test = data["y_test"]
    # perform prediction and get prices
    y_pred = model.predict(X_test)
    if SCALE:
        y_test = np.squeeze(data["column_scaler"]["low"].inverse_transform(np.expand_dims(y_test, axis=0)))
        y_pred = np.squeeze(data["column_scaler"]["low"].inverse_transform(y_pred))
    test_df = data["test_df"]
    # add predicted future prices to the dataframe
    test_df[f"low_{LOOKUP_STEP}"] = y_pred
    # add true future prices to the dataframe
    test_df[f"true_low_{LOOKUP_STEP}"] = y_test
    # sort the dataframe by date
    test_df.sort_index(inplace=True)
    final_df = test_df
    # add the buy profit column
    final_df["buy_profit"] = list(map(reachability,
                                    final_df["low"],
                                    final_df[f"low_{LOOKUP_STEP}"],
                                    final_df[f"true_low_{LOOKUP_STEP}"])
                                    # since we don't have profit for last sequence, add 0's
                                    )
    # add the sell profit column
    final_df["sell_profit"] = list(map(reachability_2,
                                    final_df["low"],
                                    final_df[f"low_{LOOKUP_STEP}"],
                                    final_df[f"true_low_{LOOKUP_STEP}"])
                                    # since we don't have profit for last sequence, add 0's
                                    )
    return final_df


def predict(model, data):
    # retrieve the last sequence from data
    last_sequence = data["last_sequence"][-N_STEPS:]
    # expand dimension
    last_sequence = np.expand_dims(last_sequence, axis=0)
    # get the prediction (scaled from 0 to 1)
    prediction = model.predict(last_sequence)
    # get the price (by inverting the scaling)
    if SCALE:
        predicted_price = data["column_scaler"]["low"].inverse_transform(prediction)[0][0]
    else:
        predicted_price = prediction[0][0]
    return predicted_price


def go_collect(ticker, n_steps=50, lookup_step=15, scale=True, shuffle=True, split_by_date=False, test_size=0.2,
              feature_columns=["adjclose", "volume", "open", "high", "low", "pct_index_300", "pct_vol_300"],
              n_layers=2, cell=LSTM, units=256,
              dropout=0.4, bidirectional=False, epochs=500, flush_result=False, only_forecast=False):
    # set seed, so we can get the same results after rerunning several times
    np.random.seed(314)
    tf.random.set_seed(314)
    random.seed(314)
    global N_STEPS, LOOKUP_STEP, SCALE, date_now
    # global SHUFFLE, SPLIT_BY_DATE, TEST_SIZE, FEATURE_COLUMNS, N_LAYERS, CELL
    # global UNITS, DROPOUT, BIDIRECTIONAL, LOSS, OPTIMIZER, BATCH_SIZE, EPOCHS,
    # Window size or the sequence length
    N_STEPS = n_steps
    # Lookup step, 1 is the next day
    LOOKUP_STEP = lookup_step // lookup_step  # just T+1 day needed
    # whether to scale feature columns & output price as well
    SCALE = scale
    scale_str = f"sc-{int(SCALE)}"
    # whether to shuffle the dataset
    SHUFFLE = shuffle
    shuffle_str = f"sh-{int(SHUFFLE)}"
    # whether to split the training/testing set by date
    SPLIT_BY_DATE = split_by_date
    split_by_date_str = f"sbd-{int(SPLIT_BY_DATE)}"
    # test ratio size, 0.2 is 20%
    TEST_SIZE = test_size
    # features to use
    FEATURE_COLUMNS = feature_columns
    # date now
    date_now = tool_day_off_filter.get_date_now()
    ### model parameters
    N_LAYERS = n_layers
    # LSTM cell
    CELL = cell
    # 256 LSTM neurons
    UNITS = units
    # 40% dropout
    DROPOUT = dropout
    # whether to use bidirectional RNNs
    BIDIRECTIONAL = bidirectional
    ### training parameters
    # mean absolute error loss
    # LOSS = "mae"
    # huber loss
    LOSS = "huber_loss"
    OPTIMIZER = "adam"
    BATCH_SIZE = 64
    EPOCHS = epochs
    # ticker = "sh600585"
    ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")
    # model name to save, making it as unique as possible based on parameters
    model_name = \
        f"collectlow_{date_now}_{ticker}-{shuffle_str}-{scale_str}-{split_by_date_str}-{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
    if BIDIRECTIONAL:
        model_name += "-b"
    # create these folders if they does not exist
    if not os.path.isdir("results"):
        os.mkdir("results")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    if not os.path.isdir("data"):
        os.mkdir("data")

    if flush_result:
        try:
            os.remove(os.path.join("results", model_name + ".h5"))
        except FileNotFoundError:
            pass

    # load the data
    data = load_data(ticker, N_STEPS, scale=SCALE, split_by_date=SPLIT_BY_DATE,
                     shuffle=SHUFFLE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE,
                     feature_columns=FEATURE_COLUMNS)
    # save the dataframe
    for fname in os.listdir('data\\'):
        if fname.startswith(ticker):
            os.remove(os.path.join('data\\', fname))
        data["df"].to_csv(ticker_data_filename, index=False)
    # construct the model
    try:
        model = tf.keras.models.load_model(os.path.join("results", model_name + ".h5"))
    except OSError or FileNotFoundError:
        model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                             dropout=DROPOUT, optimizer=OPTIMIZER, bidirectional=BIDIRECTIONAL)
    # some tensorflow callbacks
    checkpointer = ModelCheckpoint(os.path.join("results", model_name[:] + ".h5"), save_best_only=True, verbose=1)
                # save_weights_only=True,
    callbacks_list = [checkpointer]
    # tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
    # train the model and save the weights whenever we see
    # a new optimal model using ModelCheckpoint

    if not only_forecast:
        history = model.fit(data["X_train"], data["y_train"],
                            batch_size=BATCH_SIZE,
                            epochs=EPOCHS,
                            validation_data=(data["X_test"], data["y_test"]),
                            callbacks=callbacks_list,
                            verbose=0)

    # -----------------------------------------------------------prediction-------------------------------------------------

    # load optimal model weights from results folder
    model_path = os.path.join("results", model_name[:]) + ".h5"
    try:
        model.load_weights(model_path)
        # evaluate the model
        loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
        # calculate the mean absolute error (inverse scaling)
        if SCALE:
            mean_absolute_error = data["column_scaler"]["low"].inverse_transform([[mae]])[0][0]
        else:
            mean_absolute_error = mae

        # get the final dataframe for the testing set
        final_df = get_final_df(model, data)

        # predict the future price
        future_price = predict(model, data)

        # we calculate the accuracy by counting the number of positive profits
        # accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) + len(final_df[final_df['buy_profit'] > 0]))\
        #                  / len(final_df)
        reachability = round((len(final_df[final_df['buy_profit'] < 0]) / len(final_df['buy_profit'])) * 100, 2)
        reachability_2 = round((len(final_df[final_df['sell_profit'] < 0]) / len(final_df['sell_profit'])) * 100, 2)
        # printing metrics
        increased_future_low = round(future_price * 0.995, 2)
        print(f"{ticker} T+1 possible low price is {future_price:.2f}$")
        print(f"{LOSS} loss:", loss)
        print("Mean Absolute Error:", mean_absolute_error)
        print(f"Possiblity of reachability is {reachability}%")
        print(f"If you decrease the low up 0.5% at {increased_future_low}:")
        print(f"The reachability will be {reachability_2}")

        foresees_filename = os.path.join("foresees", f"{ticker}_{LOOKUP_STEP}_forecast_collectlow.csv")
        plot_filename = os.path.join("foresees", f"{ticker}_{LOOKUP_STEP}_forecast_collectlow.png")
        ifile = open(foresees_filename, 'a')
        linename = "forecast_day" + ',' + "days_in_future" + ',' + "T+2_lowest" + ',' + "LOSS" + ',' + "MAE" +\
                   ',' + "Reachability" + "lowhest * 100.5%" + "Reachability_2" + '\n'
        ifile.write(linename)
        line = date_now + ',' + str(LOOKUP_STEP) + ',' + str(future_price) + ',' + str(loss) + ',' + \
               str(mean_absolute_error) + ',' + str(reachability) + str(increased_future_low) + str(reachability_2) + \
               '\n'
        ifile.write(line)
        ifile.close()

        plot_graph(final_df, plot_filename)

        # print(final_df.tail(10))
        # save the final dataframe to csv-results folder
        csv_results_folder = "csv-results"
        if not os.path.isdir(csv_results_folder):
            os.mkdir(csv_results_folder)
        csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
        final_df.to_csv(csv_filename, index=False)
        return future_price, reachability, reachability_2
    except OSError or FileNotFoundError:
        print(f"collect_{ticker}'s h5 model file can't be found in 'result\\' folder!  Abandon...")
        return None, None




