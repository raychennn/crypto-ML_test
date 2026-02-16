"""
Add Sample References — Run this once to populate reference patterns
=====================================================================

All datetimes are in GMT+8 (Asia/Taipei) by default.
Change config.reference_input_timezone to use a different timezone.

Usage:
    python scripts/add_references.py
"""

import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SystemConfig
from data.data_manager import DataManager
from visualization.chart_generator import ChartGenerator
from telegram_bot.notifier import TelegramNotifier
from references.reference_manager import ReferenceManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def main():
    config = SystemConfig()
    config.ensure_directories()

    dm = DataManager(config)
    cg = ChartGenerator(config)
    notifier = TelegramNotifier(config)
    ref_mgr = ReferenceManager(config, data_manager=dm, chart_generator=cg, notifier=notifier)

    print(f"Timezone: {config.reference_input_timezone}")
    print(f"Existing references: {ref_mgr.count()}\n")

    # ================================================================
    # Define your reference patterns here (all times in GMT+8)
    #
    # Find patterns on TradingView/Binance, note the start/end times,
    # then add them below. Each entry needs:
    #   symbol      — Binance pair, e.g. "AVAXUSDT"
    #   timeframe   — must match downloaded data, e.g. "4h"
    #   start_dt    — pattern start in "YYYY-MM-DD HH:MM" (GMT+8)
    #   end_dt      — pattern end in "YYYY-MM-DD HH:MM" (GMT+8)
    #   label       — short unique label (used in ID generation)
    #   description — what makes this pattern interesting
    # ================================================================

    references_to_add = [
        # ----- Example: uncomment and modify these, or add your own -----
        #
        # {
        #     "symbol": "AVAXUSDT",
        #     "timeframe": "4h",
        #     "start_dt": "2023-11-09 20:00",
        #     "end_dt": "2023-11-14 08:00",
        #     "label": "standard_uptrend",
        #     "description": "AVAX classic accumulation -> breakout pattern",
        # },
        # {
        #     "symbol": "SOLUSDT",
        #     "timeframe": "4h",
        #     "start_dt": "2023-10-15 00:00",
        #     "end_dt": "2023-10-23 00:00",
        #     "label": "breakout_run",
        #     "description": "SOL strong breakout with volume confirmation",
        # },
        # {
        #     "symbol": "ETHUSDT",
        #     "timeframe": "4h",
        #     "start_dt": "2023-11-01 00:00",
        #     "end_dt": "2023-11-10 00:00",
        #     "label": "accumulation",
        #     "description": "ETH range accumulation before rally",
        # },
        {
            "symbol": "AUCTIONUSDT",
            "timeframe": "1h",
            "start_dt": "2024-08-17 13:00",
            "end_dt": "2024-08-20 00:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "POLUSDT",
            "timeframe": "2h",
            "start_dt": "2026-01-01 22:00",
            "end_dt": "2026-01-08 20:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "BDXNUSDT",
            "timeframe": "30m",
            "start_dt": "2026-01-14 19:00",
            "end_dt": "2026-01-16 06:30",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "ADAUSDT",
            "timeframe": "1h",
            "start_dt": "2024-11-06 08:00",
            "end_dt": "2024-11-10 05:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "DOGEUSDT",
            "timeframe": "1h",
            "start_dt": "2025-09-07 19:00",
            "end_dt": "2025-09-12 05:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "PUMPUSDT",
            "timeframe": "30m",
            "start_dt": "2025-12-31 05:00",
            "end_dt": "2026-01-01 19:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "SOONUSDT",
            "timeframe": "1h",
            "start_dt": "2025-08-05 20:00",
            "end_dt": "2025-08-08 20:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "ARCUSDT",
            "timeframe": "1h",
            "start_dt": "2025-10-31 08:00",
            "end_dt": "2025-11-03 12:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "ARCUSDT",
            "timeframe": "30m",
            "start_dt": "2026-01-19 08:00",
            "end_dt": "2026-01-20 12:30",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "DEEPUSDT",
            "timeframe": "1h",
            "start_dt": "2025-10-31 08:00",
            "end_dt": "2025-11-03 12:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "PIPPINUSDT",
            "timeframe": "1h",
            "start_dt": "2026-02-08 16:00",
            "end_dt": "2026-02-10 11:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(without downswing)"
        },
        {
            "symbol": "PIPPINUSDT",
            "timeframe": "30m",
            "start_dt": "2026-02-08 16:00",
            "end_dt": "2026-02-10 08:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "1INCHUSDT",
            "timeframe": "1h",
            "start_dt": "2025-07-06 00:00",
            "end_dt": "2025-07-08 17:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "CRVUSDT",
            "timeframe": "4h",
            "start_dt": "2024-11-06 08:00",
            "end_dt": "2024-11-30 12:00",
            "label": "knot_trend_2",
            "description": "previous consolidation that two sma and current close price eventually at approximate price then slowly goes up end up with super tiny consolidation (3~5 candle or even less) -> ready to pump up"
        },
        {
            "symbol": "FETUSDT",
            "timeframe": "4h",
            "start_dt": "2024-02-09 12:00",
            "end_dt": "2024-02-28 12:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "FETUSDT",
            "timeframe": "2h",
            "start_dt": "2024-02-07 20:00",
            "end_dt": "2024-02-17 20:00",
            "label": "perfect_trend_with_v",
            "description": "similar to perfect_trend but price once fall down to 60sma and then V-shape reversal or pin bar very soon "
        },
        {
            "symbol": "GALAUSDT",
            "timeframe": "1h",
            "start_dt": "2024-11-05 19:00",
            "end_dt": "2024-11-09 12:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "GUNUSDT",
            "timeframe": "30m",
            "start_dt": "2025-12-12 04:30",
            "end_dt": "2025-12-13 15:30",
            "label": "knot_trend_2",
            "description": "consolidation that two sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "PHBUSDT",
            "timeframe": "30m",
            "start_dt": "2024-09-23 08:30",
            "end_dt": "2024-09-24 14:30",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "XLMUSDT",
            "timeframe": "2h",
            "start_dt": "2024-11-15 00:00",
            "end_dt": "2024-11-22 00:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "XLMUSDT",
            "timeframe": "1h",
            "start_dt": "2025-07-06 03:00",
            "end_dt": "2025-07-09 00:00",
            "label": "knot_trend_2",
            "description": "consolidation that two sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "XLMUSDT",
            "timeframe": "1h",
            "start_dt": "2025-07-09 01:00",
            "end_dt": "2025-07-11 17:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "XRPUSDT",
            "timeframe": "4h",
            "start_dt": "2024-11-06 08:00",
            "end_dt": "2024-11-21 20:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "XRPUSDT",
            "timeframe": "4h",
            "start_dt": "2024-11-06 08:00",
            "end_dt": "2024-11-28 20:00",
            "label": "knot_trend_2",
            "description": "consolidation that two sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "ZECUSDT",
            "timeframe": "2h",
            "start_dt": "2024-10-03 22:00",
            "end_dt": "2024-10-10 06:00",
            "label": "knot_trend_2",
            "description": "consolidation that two sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "TRBUSDT",
            "timeframe": "4h",
            "start_dt": "2023-08-26 08:00",
            "end_dt": "2023-09-09 08:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "TRBUSDT",
            "timeframe": "2h",
            "start_dt": "2023-09-07 12:00",
            "end_dt": "2023-09-14 16:00",
            "label": "perfect_trend_with_v",
            "description": "similar to perfect_trend but price once fall down to 60sma and then V-shape reversal or pin bar very soon "
        },
        {
            "symbol": "SOLUSDT",
            "timeframe": "4h",
            "start_dt": "2023-10-16 12:00",
            "end_dt": "2023-10-30 12:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "BTCUSDT",
            "timeframe": "2h",
            "start_dt": "2023-10-16 04:00",
            "end_dt": "2023-10-20 08:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "DOGEUSDT",
            "timeframe": "30m",
            "start_dt": "2021-04-13 06:00",
            "end_dt": "2021-04-16 02:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "RSRUSDT",
            "timeframe": "30m",
            "start_dt": "2024-05-15 20:30",
            "end_dt": "2024-05-17 16:30",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "NOTUSDT",
            "timeframe": "1h",
            "start_dt": "2024-05-27 13:00",
            "end_dt": "2024-06-01 23:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "NOTUSDT",
            "timeframe": "1h",
            "start_dt": "2024-05-27 13:00",
            "end_dt": "2024-05-30 06:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "XRPUSDT",
            "timeframe": "2h",
            "start_dt": "2024-11-12 04:00",
            "end_dt": "2024-11-22 00:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "XRPUSDT",
            "timeframe": "2h",
            "start_dt": "2024-11-06 04:00",
            "end_dt": "2024-11-10 04:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
        {
            "symbol": "FETUSDT",
            "timeframe": "2h",
            "start_dt": "2024-02-17 20:00",
            "end_dt": "2024-02-28 12:00",
            "label": "knot_trend_2",
            "description": "consolidation that two sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "GMTUSDT",
            "timeframe": "4h",
            "start_dt": "2022-03-15 20:00",
            "end_dt": "2022-03-28 08:00",
            "label": "knot_trend_3",
            "description": "consolidation that three sma and current close price eventually at approximate price-> ready to pump up"
        },
        {
            "symbol": "GMTUSDT",
            "timeframe": "30m",
            "start_dt": "2022-03-28 14:00",
            "end_dt": "2022-03-30 00:00",
            "label": "perfect_trend",
            "description": "classic consolidation -> strong trend pattern(three sma goes up without downswing)"
        },
    ]

    if not references_to_add:
        print("No references defined!")
        print("Edit scripts/add_references.py and uncomment/add patterns.")
        print("Then re-run this script.\n")
        print("After adding references, train models with:")
        print("  python scripts/train_model.py --timeframes 4h --workers 2")
        return

    added = 0
    for ref_def in references_to_add:
        try:
            ref = ref_mgr.add_reference_by_datetime(**ref_def)
            print(f"  Added: {ref.id}")
            added += 1
        except ValueError as e:
            print(f"  Skipped: {e}")
        except Exception as e:
            print(f"  Error: {ref_def.get('symbol', '?')} — {e}")

    print(f"\nDone! Added {added} reference(s).")
    print(f"Total active references: {ref_mgr.count()}")
    print(f"Charts saved to: {config.image_dir}/references/")
    print(f"\nNext step:")
    print(f"  python scripts/train_model.py --timeframes 4h --workers 2")


if __name__ == "__main__":
    main()
