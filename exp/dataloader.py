from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd


def preprocess_data(df):
    if 'temp' in df.columns:
        df.drop(columns=['temp'], inplace=True)
    if 'counter' in df.columns:
        df['c_mean'] = df['counter']
        df['c_mean'].astype(float)

    # Differencing the 'finestep' to capture changes over time
    df['step_diff'] = df['finestep'].diff()
    
    # Exponential rolling sums
    for window_size in [60, 120, 300, 600]:
        df[f'step_{window_size}rsum_exp'] = df['step_diff'].rolling(window=window_size, win_type='exponential').sum(tau=window_size)

    # Normalizing the 'finestep' column
    df['finestep_norm'] = (df['finestep'] + np.power(2, 15)) / (2 * np.power(2, 15))

    # Additional features to scale
    df['c_mean_norm'] = df['c_mean']

    features_to_scale = ['step_diff', 'c_mean_norm'] + [f'step_{ws}rsum_exp' for ws in [60, 120, 300, 600]]
    #df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
    for feature in features_to_scale:
        df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())
    # Lagged features for 'c_mean'
    for steps in [10, 60, 120, 300, 600]:
        df[f'c_mean_lag{steps}'] = df['c_mean_norm'].shift(steps)
        df[f'c_mean_{steps}rmean'] = df['c_mean_norm'].rolling(window=steps).mean()

    # Drop rows with NA values created by lags and rolling functions
    #df.dropna(inplace=True)
    #df.reset_index(drop=True, inplace=True)
    
    return df

def construct_datasets(train_data, val_data, test_data, columns_input, columns_output = ['c_mean']):
    train_data.dropna(inplace=True)
    X_train = train_data[columns_input]
    y_train = train_data[columns_output]
    # # Prepare the features and target for testing
    val_data.dropna(inplace=True)
    X_val = val_data[columns_input]
    y_val = val_data[columns_output]

    test_data.dropna(inplace=True)
    X_test = test_data[columns_input]
    y_test = test_data[columns_output]

    return X_train, y_train, X_val, y_val, X_test, y_test