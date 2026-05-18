# Phase 22 Calibration Readiness Summary

## Operational Focus
Phase 22 introduces telemetry-driven calibration and practical Hull-B route-score tuning.

## Added Capabilities
- observed vs predicted route burden analysis
- unloading time calibration
- dead-leg risk calibration
- orbital-loop persistence calibration
- rep/hour calibration
- route degradation analysis

## Hull-B Baselines
The package now supports observational Hull-B performance baselines for:
- mission completion timing
- unloading timing
- SCU throughput
- stop density
- dead-leg recovery
- practical rep/hour

## Explicit Rules
- telemetry remains observational
- OCR uncertainty remains probabilistic
- runtime values remain runtime-derived
- sourced facts remain immutable unless superseded by better sourced data
