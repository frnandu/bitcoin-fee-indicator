#!/usr/bin/env python3

import os
import signal
import sys
import time
import requests
import json
import gi
import cairosvg
import random

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as appindicator

class BitcoinFeeIndicator:
    def __init__(self):
        # Create the application indicator
        self.indicator = appindicator.Indicator.new(
            "bitcoin_fee_indicator",
            "",  # Placeholder for icon path
            appindicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # Create a menu for the indicator
        self.menu = Gtk.Menu()

        # Add a fee rate item to the menu
        self.fastest_fee_item = Gtk.MenuItem(label="Fetching fee rate...")
        self.menu.append(self.fastest_fee_item)

        self.half_hour_fee_item = Gtk.MenuItem(label="...")
        self.menu.append(self.half_hour_fee_item)

        self.hour_fee_item = Gtk.MenuItem(label="...")
        self.menu.append(self.hour_fee_item)

        self.economy_fee_item = Gtk.MenuItem(label="...")
        self.menu.append(self.economy_fee_item)

        self.minimum_fee_item = Gtk.MenuItem(label="...")
        self.menu.append(self.minimum_fee_item)

        # Add a refresh item to the menu
        refresh_item = Gtk.MenuItem(label="Refresh")
        refresh_item.connect("activate", self.update_fee)
        self.menu.append(refresh_item)

        # Add a quit item to the menu
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self.quit)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        # Set the API base URL from environment variable or default to the current value
        self.api_base_url = os.getenv("FEE_API_BASE_URL", "https://mempool.space")
        self.api_url = f"{self.api_base_url}/api/v1/fees/recommended"  # Construct the full API URL

        # Update the fee immediately on start
        self.update_fee()

        # Set a timer to update the fee every 5 minutes
        GLib.timeout_add_seconds(300, self.update_fee)

    def update_fee(self, *args):
        try:
            response = requests.get(self.api_url)  # Use the configurable API URL
            fee_data = response.json()
            fastest_fee = fee_data['fastestFee']
            half_hour_fee = fee_data['halfHourFee']
            hour_fee= fee_data['hourFee']
            economy_fee= fee_data['economyFee']
            minimum_fee= fee_data['minimumFee']

            print(f"Fee data from {self.api_base_url}: {fee_data}")
            self.fastest_fee_item.set_label(f"Fastest: {fastest_fee} sat/vB")
            self.half_hour_fee_item.set_label(f"1/2 Hour: {half_hour_fee} sat/vB")
            self.hour_fee_item.set_label(f"Hour: {hour_fee} sat/vB")
            self.economy_fee_item.set_label(f"Economy: {economy_fee} sat/vB")
            self.minimum_fee_item.set_label(f"Minimum: {minimum_fee} sat/vB")

            # Create SVG content with larger white text
            svg_content = f"""
            <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64">
                <rect width="100%" height="100%" fill="transparent" />
                <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="50" fill="white">{fastest_fee}</text>
            </svg>
            """

            # Save SVG to a file
            svg_path = "/tmp/fee_rate.svg"
            with open(svg_path, "w") as svg_file:
                svg_file.write(svg_content)

            # Convert SVG to PNG (if needed by the indicator)
            png_path = f"/tmp/fee_rate_{fastest_fee}.png"
            cairosvg.svg2png(url=svg_path, write_to=png_path)

            # Set the indicator icon to the generated PNG
            self.indicator.set_icon_full(png_path,f"{fastest_fee}")

        except Exception as e:
            print(f"Error: {str(e)}")
            self.fastest_fee_item.set_label(f"Error: {str(e)}")
            self.indicator.set_label("Error", "Fee Rate")  # Set the indicator label to "Error" in case of an exception

        return True  # Continue the timer

    def quit(self, *args):
        Gtk.main_quit()
        sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    BitcoinFeeIndicator()
    Gtk.main()

if __name__ == "__main__":
    main()

