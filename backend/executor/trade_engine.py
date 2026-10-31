import asyncio
import ccxt.async_support as ccxt
import sys
import os

sys.path.append(os.path.join(os.path.expanduser('~'), 'igos', 'backend', 'scanner'))
from indicators import TechnicalIndicators
from risk_manager import RiskManager

async def run_bot():
    print("Запуск торгового движка IGOS (Режим DRY_RUN)...")
    exchange = ccxt.bingx({
        'enableRateLimit': True,
        'options': {'defaultType': 'swap'}
    })
    
    risk_manager = RiskManager(max_risk_pct=2.0, max_leverage=5, dry_run=True)
    virtual_balance = 1000.0
    
    try:
        await exchange.load_markets()
        tickers = await exchange.fetch_tickers()
        
        usdt_pairs = [
            symbol for symbol, data in tickers.items() 
            if symbol.endswith('/USDT:USDT') and data['quoteVolume'] is not None
        ]
        usdt_pairs.sort(key=lambda s: tickers[s]['quoteVolume'], reverse=True)
        top_coin = usdt_pairs[0]
        
        print("Анализируем актив: " + top_coin)
        
        ohlcv = await exchange.fetch_ohlcv(top_coin, timeframe='15m', limit=50)
        closes = [candle[4] for candle in ohlcv]
        
        tr_list = [max(c[2]-c[1], abs(c[2]-closes[i-1]), abs(c[1]-closes[i-1])) for i, c in enumerate(ohlcv) if i > 0]
        atr = sum(tr_list[-14:]) / 14 if tr_list else closes[-1] * 0.01
        
        k_val, _ = TechnicalIndicators.calculate_stoch_rsi(closes)
        
        print("Цена: " + str(closes[-1]) + " | StochRSI K: " + str(k_val) + " | ATR: " + str(round(atr, 4)))
        
        if k_val < 25:
            print("Обнаружена зона перепроданности! Рассчитываем виртуальный ордер...")
            trade_params = risk_manager.calculate_position_parameters(
                balance=virtual_balance,
                entry_price=closes[-1],
                atr=atr,
                direction="long"
            )
            if trade_params:
                print("Параметры виртуальной сделки (DRY_RUN):")
                for k, v in trade_params.items():
                    print("   - " + str(k) + ": " + str(v))
        else:
            print("Рынок в нейтральной зоне. Сигналов на вход нет.")
            
    except Exception as e:
        print("Ошибка: " + str(e))
    finally:
        await exchange.close()
        print("Сеанс завершен.")

if __name__ == '__main__':
    asyncio.run(run_bot())
