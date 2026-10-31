class RiskManager:
    def __init__(self, max_risk_pct=2.0, max_leverage=5, dry_run=True):
        self.max_risk_pct = max_risk_pct
        self.max_leverage = max_leverage
        self.dry_run = dry_run

    def calculate_position_parameters(self, balance, entry_price, atr, direction="long"):
        if balance <= 0 or entry_price <= 0 or atr <= 0:
            return None

        leverage = min(self.max_leverage, 5)
        stop_loss_distance = atr * 1.5
        
        if direction == "long":
            stop_loss = round(entry_price - stop_loss_distance, 4)
            take_profit = round(entry_price + (stop_loss_distance * 2.5), 4)
        else:
            stop_loss = round(entry_price + stop_loss_distance, 4)
            take_profit = round(entry_price - (stop_loss_distance * 2.5), 4)

        risk_amount_usdt = balance * (self.max_risk_pct / 100)
        risk_per_unit = abs(entry_price - stop_loss)
        
        if risk_per_unit == 0:
            return None
            
        position_size_coins = risk_amount_usdt / risk_per_unit
        position_cost_usdt = position_size_coins * entry_price
        
        max_allowed_cost = balance * leverage
        if position_cost_usdt > max_allowed_cost:
            position_cost_usdt = max_allowed_cost
            position_size_coins = position_cost_usdt / entry_price

        return {
            "dry_run": self.dry_run,
            "leverage": leverage,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "position_size": round(position_size_coins, 4),
            "position_cost": round(position_cost_usdt, 2)
        }
