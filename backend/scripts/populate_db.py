#!/usr/bin/env python3
"""
Script to initialize and populate the vector database with documents
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.orchestrator import HybridRAGOrchestrator
from app.providers.document_processor import DocumentProcessor
from app.config.settings import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def populate_database():
    """Populate ChromaDB with portfolio documents"""
    try:
        logger.info("🚀 Starting database population...")
        
        # Initialize orchestrator
        orchestrator = HybridRAGOrchestrator()
        
        # Check if already populated
        status = orchestrator.get_system_status()
        if status.get('initialized'):
            logger.info("✅ Database already populated")
            
            response = input("Do you want to reload documents? (y/n): ")
            if response.lower() != 'y':
                logger.info("Exiting without changes")
                return
            
            logger.info("Reloading documents...")
            result = orchestrator.reload_documents()
            if result.get('success'):
                logger.info(f"✅ {result.get('message')}")
            else:
                logger.error(f"❌ Error: {result.get('error')}")
        else:
            logger.info("📚 Loading documents for first time...")
            
            # Document processor will handle loading
            doc_processor = DocumentProcessor()
            documents = doc_processor.load_documents()
            
            logger.info(f"📄 Found {len(documents)} documents")
            
            for doc in documents:
                metadata = doc.get('metadata', {})
                logger.info(f"  - {metadata.get('filename', 'Unknown')}: {len(doc['content'])} chars")
            
            logger.info("✅ Database population complete!")
            
        # Show statistics
        logger.info("\n📊 Database Statistics:")
        stats = orchestrator.get_system_status()
        
        if stats.get('vector_store_stats'):
            logger.info(f"  - Total documents: {stats['vector_store_stats'].get('total_documents', 0)}")
            logger.info(f"  - Total embeddings: {stats['vector_store_stats'].get('total_embeddings', 0)}")
        
        if stats.get('documents_info'):
            logger.info(f"  - Document languages: {stats['documents_info'].get('languages', [])}")
            logger.info(f"  - Document types: {stats['documents_info'].get('types', [])}")
            
    except Exception as e:
        logger.error(f"❌ Error populating database: {e}")
        sys.exit(1)

def verify_documents():
    """Verify that documents are correctly loaded"""
    try:
        logger.info("🔍 Verifying documents...")
        
        orchestrator = HybridRAGOrchestrator()
        
        # Test queries
        test_queries = [
            "¿Cuál es tu experiencia?",
            "What projects have you worked on?",
            "Háblame sobre tus habilidades"
        ]
        
        for query in test_queries:
            logger.info(f"\nTesting query: '{query}'")
            
            # Search for relevant context
            context = orchestrator._search_relevant_context(query)
            
            if context:
                logger.info(f"  ✅ Found {len(context)} relevant documents")
                for i, doc in enumerate(context[:2], 1):
                    preview = doc['content'][:100] + "..." if len(doc['content']) > 100 else doc['content']
                    logger.info(f"    {i}. {preview}")
            else:
                logger.warning("  ⚠️ No relevant documents found")
                
    except Exception as e:
        logger.error(f"❌ Error verifying documents: {e}")
        sys.exit(1)

def clear_database():
    """Clear the vector database"""
    try:
        response = input("⚠️ This will delete all data in the vector database. Continue? (y/n): ")
        if response.lower() != 'y':
            logger.info("Operation cancelled")
            return
        
        logger.info("🗑️ Clearing database...")
        
        orchestrator = HybridRAGOrchestrator()
        
        if orchestrator.vector_store:
            orchestrator.vector_store.clear()
            logger.info("✅ Vector store cleared")
        
        if orchestrator.cache_provider:
            orchestrator.cache_provider.clear()
            logger.info("✅ Cache cleared")
        
        logger.info("✅ Database cleared successfully")
        
    except Exception as e:
        logger.error(f"❌ Error clearing database: {e}")
        sys.exit(1)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management for hybrid chatbot')
    parser.add_argument('command', choices=['populate', 'verify', 'clear', 'reload'],
                       help='Command to execute')
    parser.add_argument('--force', action='store_true',
                       help='Force operation without confirmation')
    
    args = parser.parse_args()
    
    if args.command == 'populate':
        populate_database()
    elif args.command == 'verify':
        verify_documents()
    elif args.command == 'clear':
        clear_database()
    elif args.command == 'reload':
        logger.info("Reloading documents...")
        orchestrator = HybridRAGOrchestrator()
        result = orchestrator.reload_documents()
        if result.get('success'):
            logger.info(f"✅ {result.get('message')}")
        else:
            logger.error(f"❌ {result.get('error')}")

if __name__ == '__main__':
    main()
