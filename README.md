# RockScan Fossil Detector

A Python-based image processing tool designed to analyze Micro-CT rock slice scans (`rockscan.png`), segment structures using median thresholding, and identify feature centers (such as pore spaces or fossil cross-sections) using spatial proximity criteria and coordinate clustering.

---

## Project Overview

This repository contains scripts developed to automate feature detection from rock CT imaging data:
- **Image Preprocessing & Thresholding:** Slices and crops CT scan images, thresholding pixel values against calculated medians.
- **Radial Feature Identification:** Scans image neighborhoods using distance equations to locate region centers based on local pixel density.
- **Spatial Aggregation:** Uses an iterative clustering algorithm (`recluster()`) to group adjacent coordinates and compute mean centroids for detected features.

---

## Requirements

- Python 3.x
- `numpy`
- `Pillow` (PIL)

Install required dependencies via `pip`:

```bash
pip install numpy pillow
