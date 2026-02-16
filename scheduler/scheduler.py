"""
Scan Scheduler — Cron-style automatic scanning
=================================================

Scheduling rules (all at HH:02):
    - 30m + 1h: every hour
    - 2h: even hours (hour % 2 == 0)
    - 4h: hours divisible by 4 (hour % 4 == 0)

Before each scan, incrementally updates data from Binance.
Uses threading.Timer for simplicity (no APScheduler dependency).

Delegates all scan logic to ScanOrchestrator (single source of truth).
"""

import logging
import threading
from datetime import datetime, timedelta
from typing import Optional, List

import pytz

logger = logging.getLogger(__name__)


class ScanScheduler:
    """Cron-style scheduler for automated pattern scanning"""

    def __init__(self, config, scan_orchestrator, notifier, data_manager=None,
                 symbol_manager=None):
        self.config = config
        self.orchestrator = scan_orchestrator
        self.notifier = notifier
        self.data_manager = data_manager
        self.symbol_manager = symbol_manager

        self._timer: Optional[threading.Timer] = None
        self._stop_event = threading.Event()
        self._running = False

    # ================================================================
    # Lifecycle
    # ================================================================

    def start(self):
        """Start the scheduler — schedules the next tick"""
        self._stop_event.clear()
        self._running = True

        # Run initial data check in background
        thread = threading.Thread(
            target=self._initial_data_check, daemon=True, name="initial-data-check"
        )
        thread.start()

        self._schedule_next()
        logger.info("Scan scheduler started")

    # ================================================================
    # First-Start Data Check
    # ================================================================

    def _initial_data_check(self):
        """
        On first start, check if any Parquet data exists.
        If not, trigger an initial download for all timeframes.
        """
        if not self.data_manager or not self.symbol_manager:
            return

        try:
            has_data = False
            for tf in self.config.scan_timeframes:
                symbols = self.data_manager.list_symbols_for_timeframe(tf)
                if symbols:
                    has_data = True
                    logger.info(f"[startup] {tf}: {len(symbols)} symbols found locally")
                else:
                    logger.info(f"[startup] {tf}: no local data")

            if has_data:
                logger.info("[startup] Local data exists, skipping initial download")
                return

            logger.info("[startup] No local data found — starting initial download...")
            self.notifier.send_message(
                "<b>First Start</b>\n"
                "No local data found. Starting initial data download...\n"
                "This may take a while."
            )

            symbols = self.symbol_manager.get_active_symbols()
            if not symbols:
                logger.warning("[startup] Could not get symbol list for initial download")
                return

            logger.info(f"[startup] Downloading data for {len(symbols)} symbols...")

            for tf in self.config.scan_timeframes:
                updated = self.orchestrator.update_data(tf)
                logger.info(f"[startup] {tf}: downloaded data for {updated} symbols")
                if self._stop_event.is_set():
                    break

            self.notifier.send_message(
                "<b>Initial Download Complete</b>\n"
                f"Downloaded data for {len(self.config.scan_timeframes)} timeframes."
            )
        except Exception as e:
            logger.error(f"[startup] Initial data check failed: {e}")
            self.notifier.send_message(f"Initial data check error: {e}")

    def stop(self):
        """Stop the scheduler"""
        self._stop_event.set()
        self._running = False
        if self._timer:
            self._timer.cancel()
            self._timer = None
        logger.info("Scan scheduler stopped")

    @property
    def is_running(self) -> bool:
        return self._running

    # ================================================================
    # Scheduling Logic
    # ================================================================

    def _schedule_next(self):
        """Calculate seconds until next HH:02 and schedule a timer"""
        if self._stop_event.is_set():
            return

        now = datetime.now(pytz.timezone(self.config.timezone))
        minute_offset = self.config.scan_minute_offset

        # Next trigger = current hour + minute_offset, or next hour if past
        next_run = now.replace(minute=minute_offset, second=0, microsecond=0)
        if now >= next_run:
            next_run += timedelta(hours=1)

        delay = (next_run - now).total_seconds()
        delay = max(1, delay)  # safety floor

        logger.info(
            f"Next scheduled scan at {next_run.strftime('%Y-%m-%d %H:%M')} "
            f"({delay:.0f}s from now)"
        )

        self._timer = threading.Timer(delay, self._tick)
        self._timer.daemon = True
        self._timer.start()

    def _tick(self):
        """Timer callback — determine timeframes and run scan"""
        if self._stop_event.is_set():
            return

        now = datetime.now(pytz.timezone(self.config.timezone))
        hour = now.hour
        timeframes = self._get_timeframes_for_hour(hour)

        logger.info(
            f"Scheduled scan triggered at {now.strftime('%H:%M')} — "
            f"timeframes: {timeframes}"
        )

        # Run scan in a thread so we don't block the timer scheduling
        thread = threading.Thread(
            target=self._run_scheduled_scan,
            args=(timeframes,),
            daemon=True,
            name="scheduled-scan",
        )
        thread.start()

        # Schedule next tick immediately (don't wait for scan to finish)
        self._schedule_next()

    @staticmethod
    def _get_timeframes_for_hour(hour: int) -> List[str]:
        """
        Determine which timeframes to scan based on the hour.

        Rules:
            - 30m, 1h: every hour
            - 2h: even hours (hour % 2 == 0)
            - 4h: hours divisible by 4 (hour % 4 == 0)
        """
        timeframes = ["30m", "1h"]

        if hour % 2 == 0:
            timeframes.append("2h")

        if hour % 4 == 0:
            timeframes.append("4h")

        return timeframes

    # ================================================================
    # Scan Execution — delegates to ScanOrchestrator
    # ================================================================

    def _run_scheduled_scan(self, timeframes: List[str]):
        """Execute a scheduled scan via orchestrator"""
        try:
            total_alerts = self.orchestrator.run_scan(
                timeframes=timeframes, send_notifications=True
            )

            if total_alerts > 0:
                self.notifier.send_message(
                    f"Scheduled scan complete: <b>{total_alerts}</b> alerts.\n"
                    f"Dashboard: {self.config.web_base_url}"
                )
            else:
                logger.info("Scheduled scan complete: no alerts")

        except RuntimeError as e:
            # "A scan is already running"
            logger.warning(f"Skipping scheduled scan — {e}")
        except Exception as e:
            logger.error(f"Scheduled scan error: {e}", exc_info=True)
            self.notifier.send_message(f"Scheduled scan failed: {e}")
