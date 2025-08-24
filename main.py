#!/usr/bin/env python3
"""
Main pipeline runner for the Silat RAG System.
Runs the complete PDF ingestion pipeline from extraction to vector storage.
"""

import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.pdf_parser import extract_text_with_metadata
from src.data_processor import process_and_store_data
from src.pipeline_utils import display_page_samples, generate_summary_stats, print_summary_stats
from src.config import PDF_PATH

def main():
    """Run the complete PDF ingestion pipeline."""
    print("="*80)
    print("SILAT RAG SYSTEM - PDF INGESTION PIPELINE")
    print("="*80)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"PDF file: {PDF_PATH}")
    
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"ERROR: PDF file not found at {PDF_PATH}")
        print("Please ensure the PDF is in the correct location.")
        return
    
    try:
        # Phase 1: PDF Extraction & Content Analysis
        print("\n" + "="*80)
        print("PHASE 1: PDF EXTRACTION & CONTENT ANALYSIS")
        print("="*80)
        
        extracted_data = extract_text_with_metadata(PDF_PATH)
        
        if not extracted_data:
            print("WARNING: No data was extracted from the PDF. Halting pipeline.")
            return
            
        print(f"\nPHASE 1 COMPLETE: Extracted and analyzed {len(extracted_data)} pages.")
        
        # Phase 2: Data Processing & Vector Storage
        print("\n" + "="*80)
        print("PHASE 2: DATA PROCESSING & VECTOR STORAGE")
        print("="*80)
        
        process_and_store_data(extracted_data)
        
        print(f"\nPHASE 2 COMPLETE: Data chunked, embedded, and stored in ChromaDB.")

        # Phase 3: Post-Ingestion Analysis
        print("\n" + "="*80)
        print("PHASE 3: POST-INGESTION ANALYSIS")
        print("="*80)
        
        # Generate and display summary statistics
        stats = generate_summary_stats(extracted_data)
        print_summary_stats(stats)
        
        # Display page samples (first 7, middle 7, last 7)
        display_page_samples(extracted_data, sample_size=3) # smaller sample for brevity
        
        # Success message
        print("\n" + "="*80)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*80)
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("The vector database is now ready for the RAG query pipeline.")
        
    except Exception as e:
        print(f"\nERROR: Pipeline failed with exception:")
        print(f"  {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    main()
