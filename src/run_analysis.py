#!/usr/bin/env python
"""
CLI for Axonal Damage Analysis
Run from terminal: python src/run_analysis.py --input ../docs/sample_data
"""

# --- IMPORTS ---
import argparse      # Built-in library for parsing command-line arguments
import os            # For file path operations
import sys           # For modifying Python's module search path

# Add src/ folder to Python's path so you can import pipeline.py
# __file__ is the path to this script (run_analysis.py)
# os.path.dirname(__file__) gives the src/ folder
# sys.path.insert(0, ...) adds it at the beginning of the search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import process_folder # Import your batch processing function


# --- MAIN FUNCTION ---
def main():
    """
    This function sets up the CLI, parses arguments, and runs the analysis.
    """
    
    # Create the argument parser
    # description appears when user runs: python run_analysis.py --help
    parser = argparse.ArgumentParser(
        description='Axonal bead analysis from CZI microscopy images'
    )
    
    # --input: REQUIRED argument
    # User must provide this: python run_analysis.py --input docs/sample_data
    # -i is a shortcut: python run_analysis.py -i docs/sample_data
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Input folder containing .czi files'
    )
    
    # --output: OPTIONAL argument with default value
    # If not provided, uses 'docs/example_output'
    parser.add_argument(
        '--output', '-o',
        default='docs/example_output',
        help='Output folder for results and QC images (default: docs/example_output)'
    )
    
    # --scale: OPTIONAL, must be a number (float)
    # type=float ensures Python converts the string input to a number
    parser.add_argument(
        '--scale',
        type=float,
        default=0.3126,
        help='Pixel size in µm/pixel (default: 0.3126)'
    )
    
    # --bead-threshold: OPTIONAL, must be an integer
    # This replaces the old --bead-percentile to match your pipeline.py
    parser.add_argument(
        '--bead-threshold',
        type=int,
        default=220,
        help='Manual threshold for bead detection, 0-255 (default: 220)'
    )
    
    # --no-qc: OPTIONAL flag (no value needed)
    # action='store_true' means: if flag is present, value is True
    # If absent, value is False
    # Usage: python run_analysis.py --input x --no-qc
    parser.add_argument(
        '--no-qc',
        action='store_true',
        help='Skip QC overlay image generation'
    )
    
    # --- PARSE ARGUMENTS ---
    # This reads what the user typed and converts to Python objects
    args = parser.parse_args()
    
    # --- PRINT CONFIGURATION ---
    # Shows user what will happen (good for logging/debugging)
    print("=" * 50)
    print("Axonal Damage Analysis")
    print("=" * 50)
    print(f"Input folder:     {args.input}")
    print(f"Output folder:    {args.output}")
    print(f"Scale:            {args.scale} µm/pixel")
    print(f"Bead threshold:   {args.bead_threshold}")
    print(f"QC images:        {'No' if args.no_qc else 'Yes'}")
    print("=" * 50)
    
    # --- RUN ANALYSIS ---
    # Call your pipeline function with parsed arguments
    df = process_folder(
        input_dir=args.input,
        output_dir=args.output,
        scale_um_per_px=args.scale,
        bead_thresh=args.bead_threshold,      # Pass to pipeline.py
        save_qc=not args.no_qc                 # Invert: --no-qc=True → save_qc=False
    )
    
    # --- COMPLETION MESSAGE ---
    print("\n" + "=" * 50)
    print(f"Done! Processed {len(df)} images.")
    print("=" * 50)


# --- ENTRY POINT ---
# This ensures main() only runs when script is executed directly
# (not when imported as a module)
if __name__ == '__main__':
    main()