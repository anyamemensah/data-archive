# Data Archive

This repository contains a collection of (semi)automated open data snapshots.

The project folders in this directory track changes in public or open-source datasets over time, creating a versioned history of information.

## Structure

### Project Files
* `/scripts`: The Python logic that automates data collection.
* `.github/workflows`: GitHub Actions that schedule and trigger the scripts.

### Data
* `/data`: All snapshots are stored here, organized by source.
    * `/data/septa_elevator_outages`: Historical logs tracking SEPTA elevator outages.