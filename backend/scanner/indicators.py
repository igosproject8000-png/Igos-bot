import math

class TechnicalIndicators:
    @staticmethod
    def calculate_ema(closes, period=50):
        if len(closes) < period:
            return closes[-1] if closes else 0.0
        multiplier = 2 / (period + 1)
        ema = sum(closes[:period]) / period
        for price in closes[period:]:
            ema = (price - ema) * multiplier + ema
        return round(ema, 4)

    @staticmethod
    def calculate_stoch_rsi(closes, period=14, smooth_k=3, smooth_d=3):
        if len(closes) < period * 2:
            return 50.0, 50.0
        rsi_values = []
        gains, losses = 0, 0
        for i in range(1, len(closes)):
            change = closes[i] - closes[i-1]
            gains = change if change > 0 else 0
            losses = -change if change < 0 else 0
            if i <= period:
                avg_gain = gains / period
                avg_loss = losses / period
            else:
                avg_gain = (avg_gain * (period - 1) + gains) / period
                avg_loss = (avg_loss * (period - 1) + losses) / period
            if avg_loss == 0:
                rsi = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi = 100.0 - (100.0 / (1.0 + rs))
            rsi_values.append(rsi)
            
        if len(rsi_values) < period:
            return 50.0, 50.0
            
        stoch_k_list = []
        for i in range(period, len(rsi_values) + 1):
            window = rsi_values[i - period:i]
            min_rsi = min(window)
            max_rsi = max(window)
            if max_rsi - min_rsi == 0:
                stoch_k = 50.0
            else:
                stoch_k = ((rsi_values[i-1] - min_rsi) / (max_rsi - min_rsi)) * 100
            stoch_k_list.append(stoch_k)
            
        current_k = sum(stoch_k_list[-smooth_k:]) / len(stoch_k_list[-smooth_k:]) if stoch_k_list else 50.0
        return round(current_k, 2), round(current_k, 2)

    @staticmethod
    def check_volume_spike(volumes, multiplier=2.0):
        if len(volumes) < 21:
            return False
        return volumes[-1] > ((sum(volumes[-21:-1]) / 20) * multiplier)
