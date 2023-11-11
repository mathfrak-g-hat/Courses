#################################################
##### TIME SERIES ANALYSIS HELPER FUNCTIONS #####
#################################################
### AJ Zerouali, 2023/05/29
### A collection of helper functions to deal with
### time series analysis.

# Python basics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
from copy import deepcopy

# Statsmodels
# Autocorrelation functions (ACF and PACF plotters)
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# Augmented Dickey-Fuller test
from statsmodels.tsa.stattools import adfuller 
# Ljung-Box test
from statsmodels.stats.diagnostic import acorr_ljungbox
# SARIMAX model
from statsmodels.tsa.statespace.sarimax import SARIMAX
# ARIMA model (Although we'll just look at the ARMA part)
from statsmodels.tsa.arima_process import ArmaProcess, arma_generate_sample
from statsmodels.tsa.arima.model import ARIMA


# DRL_PFOpt (data management)
from drl_pfopt import (PortfolioOptEnv, FeatureEngineer, data_split, AlpacaDownloader, YahooDownloader)
from drl_pfopt.common.data.data_utils import get_timeframe_info, get_market_calendar_day_list
from dual_timeframe_XP import (PFOptDualTFEnv, FeatureEngDualTF, data_dict_split)


'''
    ####################################
    ##### CLOSE PRICES AND RETURNS #####
    ####################################
    23/05/26 Version
'''
def get_daily_stock_returns(df_data: pd.DataFrame,
                            stock_tickers_list: list,
                            start_date: str,
                            end_date: str,
                            log_returns: bool = False
                           ):
    '''
        Function that isolates the close returns of a list
        of tickers from a dataframe. Returns a dataframe of 
        daily close prices and a dataframe of daily returns
        or log returns of the close prices.
        NOTES: 
        - The df_data parameter is assumed to be built
          by the drl_pfopt AlpacaDownloader.
        - If the dataframe is not on a daily timeframe for
          the data, this function will assign the close prices
          at 16:00 for the daily close prices. These timestamps must be
          in the "date" column of df_data.
        - The close price returns ARE NOT in percentage.
            
        :param df_data: pd.DataFrame. Should be produced by an object
                    of class drl_pfopt.common.data.downloaders.AlpacaDownloader.
        :param stock_tickers_list: list of stock tickers.
        :param start_date: str, start date in "%Y-%m-%d" format
        :param end_date: str, INCLUSIVE end date in "%Y-%m-%d" format
        :param log_returns: bool, False by default. Whether to compute
                    log returns instead of returns.
                    
        :return df_returns: pd.DataFrame of daily close price returns
                or log returns.
        :return df_close: pd.DataFrame of daily close prices.

    '''
    # Sort the tickers list
    stock_tickers_list.sort()
    
    # Check dataset contains the stock ticker selected
    data_ticker_list = list(df_data.tic.unique())
    for tic in stock_tickers_list:
        if tic not in list(df_data.tic.unique()):
            raise ValueError(f"ERROR: Ticker {tic} not found in df_data.")
    # Check dates are consistent with dataset
    data_timestamp_list = list(df_data.date.unique())
    data_start_date = data_timestamp_list[0][:10]
    data_end_date = data_timestamp_list[-1][:10]
    if end_date<= start_date:
        raise ValueError(f"ERROR: start_date={start_dat} parameter cannot be after end_date={end_date}.")
    if (end_date > data_end_date) or (end_date < data_start_date)\
        or (start_date > data_end_date) or (start_date < data_start_date):
        raise ValueError(f"ERROR: start_date and end_date are not in the dataset df_data."\
                         f"The dataset has: data_start_date = {data_start_date}, data_end_date = {data_end_date}."
                        )
        
    # Get data timeframe info dictionary
    data_timeframe_info = get_timeframe_info(data_timestamp_list)
    data_day_list_ = data_timeframe_info["day_list"] 
    
    # Get output day list (str and datetime formats)
    start_date_ = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_ = datetime.strptime(end_date, "%Y-%m-%d")
    ### Temporary day_list
    day_list_ = get_market_calendar_day_list(start_date_, end_date_+timedelta(days = 10))
    last_day_idx = day_list_.index(end_date_) # .index() 
    ## Final day list
    day_list = [x.strftime("%Y-%m-%d") for x in day_list_[:last_day_idx+1]]
    
    # Get list of close timestamps for dataset
    if data_timeframe_info["timeframe"] == "Day":
        close_timestamps_list = day_list
    else:
        close_timestamps_list = [x+" 16:00" for x in day_list]
            
    # Reduce dataframe
    df_X = df_data.copy()
    ### Keep tickers in stock_tickers_list
    df_X = df_X[df_X.tic.isin(stock_tickers_list)]
    ### Keep timestamps in close_timestamps_list
    df_X = df_X[df_X.date.isin(close_timestamps_list)]
    df_X = df_X.sort_values(["date", "tic"], ignore_index=True)
    
    # Make close prices dataframe
    #df_close = df_X.pivot_table(index = 'date', columns = 'tic', values = 'close')
    df_close = pd.DataFrame({'date': day_list})
    for tic in stock_tickers_list:
        df_close[tic] = df_X[(df_X.tic==tic)]['close'].to_numpy() # Bugs if you remove to_numpy()
    np_close = df_close[stock_tickers_list].to_numpy()
    
    # Make returns array
    np_returns = np.zeros(shape = np_close.shape)
    np_returns[1:,:] = (np_close[1:,:]-np_close[:-1,:])/np_close[:-1,:]
    if log_returns:
        np_returns = np_returns + np.ones(shape = np_returns.shape)
        np_returns = np.log(np_returns)
        
    # Make returns dataframe
    df_returns = pd.DataFrame({'date': day_list})
    for i in range(len(stock_tickers_list)):
        df_returns[stock_tickers_list[i]] = np_returns[:,i]
    
    return df_returns, df_close
    
'''
    ##############################################
    ##### FORECASTS VS OBSERVATIONS PLOTTING #####
    ##############################################
    23/05/24 Version
'''

def plot_forecasts(Y_train: np.ndarray,
                   n_train_plot_pts: int,
                   Y_test: np.ndarray,
                   Y_pred: np.ndarray,
                   n_forecast_plot_pts: int,
                   fig_title: str = "Original process and forecasts",
                   legend_loc: int = 1,
                   x_label: str = "Time",
                   y_label: str = "Y",
                   Y_pred_conf_int: np.ndarray = None,
                   plot_confidence_band: bool = False,
                   plot_upper_lower_curves: bool = False,
                  ):
    '''
        :param Y_train: np.ndarray, training data
        :param n_train_pts: int, number of points to plot from training data
        :param Y_test: np.ndarray, test data
        :param Y_pred: np.ndarray, out-of-sample forecasts
        :param n_forecast_pts: int, no. of points to plot from test data and forecasts
        :param fig_title: str, title of the figure
        :param legend_loc: int = 1,
        :param x_label: str = "Time", self-explanatory
        :param y_label: str = "Y", self-explanatory
        :param Y_pred_conf_int: np.ndarray = None, confidence interval start and end points.
                    If Y_pred.shape = (N,), should have Y_pred_conf_int.shape = (N,2),
                    with Y_pred_conf_int[:,0] giving the lower bound of the conf. interval
                    and  Y_pred_conf_int[:,1] giving the upper bound of the conf. interval
        :param plot_confidence_band: bool = False, whether or not to plot the confidence band
        :param plot_upper_lower_curves: bool = False, whetehr or not to not the upper and lower bounds
    '''
    # Initializations
    n_train_pts = len(Y_train)
    n_test_pts = len(Y_test)
    n_forecast_pts = len(Y_pred)
    
    # Check lengths and shapes
    if n_train_pts<n_train_plot_pts:
        raise ValueError(f"n_train_plot_pts = {n_train_plot_pts} is greater than len(Y_train) = {len(Y_train)}")
    if (Y_train.shape != (n_train_pts,)) or (Y_test.shape != (n_test_pts,)) or (Y_pred.shape != (n_forecast_pts,)):
        raise ValueError("The parameters Y_train, Y_test, and Y_pred must all be one-dimensional arrays.")
    if n_forecast_plot_pts>n_forecast_pts:
        raise ValueError(f"n_forecast_plot_pts = {n_forecast_plot_pts} is greater than len(Y_pred) = {len(Y_pred)}")
    if plot_confidence_band:
        if Y_pred_conf_int.shape != (n_forecast_pts,2):
            print(f"WARNING: Will not plot confidence band, param. Y_pred_conf_int has wrong shape.\n"\
                  f"Plotting the confidence band requires Y_pred_conf_int.shape = (len(Y_pred),2)"
                 )
            plot_confidence_band = False
    
    # Make x-axis ranges for sample and out-of-sample data
    #x_plot_start = n_train_pts - n_train_plot_pts
    x_sample = np.arange(n_train_pts - n_train_plot_pts, n_train_pts)
    x_oos_data = np.arange(n_train_pts, n_train_pts+ n_test_pts)
    x_oos_pred = np.arange(n_train_pts, n_train_pts+ n_forecast_plot_pts)
    
    # Init. figure
    fig_pred, ax_pred = plt.subplots()
    
    # Plot the original process (train+test data)
    Y_vals = np.concatenate([Y_train[-n_train_plot_pts:], Y_test], axis = 0)
    x_vals = np.concatenate([x_sample, x_oos_data], axis = 0)
    ax_pred.plot(x_vals, Y_vals, color = 'b', label = 'Original Process')
    
    # Shade the out-of-sample region
    ax_pred.axvspan(n_train_pts, n_train_pts+max(n_test_pts,n_forecast_plot_pts), color='#808080', alpha=0.2)
    
    # Plot the forecats
    ax_pred.plot(x_oos_pred, Y_pred[:n_forecast_plot_pts], color = 'r', label = 'Forecast')
    
    # Plot the confidence band
    if plot_confidence_band:
        if plot_upper_lower_curves:
            # Upper limit of predictions
            ax_pred.plot(x_oos_pred, Y_pred_conf_int[:,1], color = 'g', label = 'Forecast upper lim')
            # Lower limit of predictions
            ax_pred.plot(x_oos_pred, Y_pred_conf_int[:,0], color = 'g', label = 'Forecast lower lim')
        # Shading of the 95% confidence band
        ## Ref: https://matplotlib.org/stable/gallery/lines_bars_and_markers/fill_between_demo.html
        ax_pred.fill_between(x_oos_pred, Y_pred_conf_int[:,0], Y_pred_conf_int[:,1], 
                              color = 'g', alpha=0.35)
    
    # Title, axes and legend
    ax_pred.legend(loc=legend_loc)
    ax_pred.set_xlabel(x_label)
    ax_pred.set_ylabel(y_label)
    ax_pred.set_title(fig_title)
    
    plt.show()
    
    # Compute and display the forecast MSE
    n_pts_mse = min(n_test_pts, n_forecast_pts)
    MSE_pred = ((Y_pred[:n_pts_mse]-Y_test[:n_pts_mse])**2).mean()
    print(f"MSE over first {n_pts_mse} points of Y_test and Y_pred:\n"\
          f"MSE(Y_pred[:{n_pts_mse}],Y_test[:{n_pts_mse}]) = {MSE_pred}"
         )
    

'''
    #################################
    ##### ARMA(p,q) GRID SEARCH #####
    #################################
    23/05/29 Version
'''

def ARMA_grid_search(Y: np.ndarray,
                     p_min: int,
                     p_max: int,
                     q_min: int,
                     q_max: int,
                     ):
    '''
        Grid search for (p,q) orders that fit the time series
        Y to an ARMA(p,q) model, where p is in [p_min, p_max],
        amd where q is in [q_min, q_max].
        This function fits Y to all the ARMA(p,q) models and
        returns the model with the lowest Akaike Information
        Criterion (AIC).
        
        :param Y: np.ndarray, time series to fit
        :param p_min: int, min autoregressive order
        :param p_max: int, max autoregressive order
        :param q_min: int, min moving average order
        :param q_max: int, max moving average order
        
        :return ARIMA_fit: ARIMAResults object (statsmodels), minimal AIC
            obtained during grid search
        :return df_results: pd.DataFrame of results. Showcases the AIC
            for each value of (p,q) used by the function.
        :return model_fit_results_dict: dict of all ARIMAResults objects created
        :return model_dict: dict of all statsmodels ARMA objects created
    '''
    # Make list of (p,q) values
    order_list = []
    for p in range(p_min, p_max+1):
        for q in range(q_min, q_max+1):
            order_list.append((p,q))
    
    # Output initializations
    model_dict = {}
    model_fit_results_dict = {}
    df_results = pd.DataFrame(index=range(len(order_list)),columns = ["p","q","AIC"])
    AIC_list = []
    
    # AIC_dict = {}
    
    # Main loop
    for i in range(len(order_list)):
        # (p,q)
        order = order_list[i]
        p = order[0]
        q = order[1]
        
        # Instantiate temp model
        model_temp = ARIMA(endog = Y,
                           order=(p, 0, q), 
                           trend = 'c')
        ## Store model
        model_dict[order] = deepcopy(model_temp)
        
        # Fit the model
        model_fit_res_temp = model_temp.fit()
        ## Store results obj
        model_fit_results_dict[order] = deepcopy(model_fit_res_temp)
        
        # Get the AIC
        model_aic_temp = model_fit_res_temp.aic
        AIC_list.append(model_aic_temp)
        ### Store in dataframe
        df_results.iloc[i] = pd.Series({"p":p, "q":q, "AIC":model_aic_temp})
        
        # Delete model and results
        del model_temp, model_fit_res_temp
        
    # Get the model with lowest AIC
    np_AIC = df_results["AIC"].to_numpy()
    min_idx = np_AIC.argmin()
    ARIMA_fit = model_fit_results_dict[order_list[min_idx]]
    
    # Finished message
    print(f"Model with minimal AIC is ARIMA({order_list[min_idx][0]},{order_list[min_idx][1]})")
    
    
    return ARIMA_fit, df_results, model_fit_results_dict, model_dict