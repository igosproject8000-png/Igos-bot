class StrategySelector:
    @staticmethod
    def detect_market_regime(ohlcv_data):
        """Определяет текущую фазу рынка для автоматического выбора лучшей стратегии"""
        if len(ohlcv_data) < 50:
            return "UNKNOWN"
            
        closes = [candle[4] for candle in ohlcv_data]
        highs = [candle[2] for candle in ohlcv_data]
        lows = [candle[1] for candle in ohlcv_data]
        
        ema_50 = sum(closes[-50:]) / 50
        current_price = closes[-1]
        price_range = (max(highs[-20:]) - min(lows[-20:])) / current_price
        
        if price_range > 0.08:
            return "HIGH_VOLATILITY_BREAKOUT"
        elif abs(current_price - ema_50) / ema_50 > 0.03:
            return "STRONG_TREND"
        else:
            return "RANGE_FLAT"
