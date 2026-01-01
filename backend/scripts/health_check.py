#!/usr/bin/env python3
"""
Health check script for monitoring system status
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.orchestrator import HybridRAGOrchestrator

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def print_header():
    """Print header banner"""
    print("=" * 60)
    print(" " * 15 + "🏥 SYSTEM HEALTH CHECK 🏥")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_component_health(name, check_func):
    """Check health of a component"""
    try:
        result = check_func()
        status = "✅ HEALTHY" if result else "❌ UNHEALTHY"
        return status, None
    except Exception as e:
        return "❌ ERROR", str(e)

def run_health_check():
    """Run complete health check"""
    print_header()
    
    try:
        # Initialize orchestrator
        orchestrator = HybridRAGOrchestrator()
        
        # Get system status
        status = orchestrator.get_system_status()
        
        print("\n🔍 COMPONENT STATUS:")
        print("-" * 40)
        
        # Check each provider
        providers = status.get('providers', {})
        for name, info in providers.items():
            available = info.get('available', False)
            status_icon = "✅" if available else "❌"
            print(f"{status_icon} {name.upper()}: {'Available' if available else 'Unavailable'}")
            if not available and name in ['llm', 'embedding', 'vector_store']:
                print(f"  ⚠️  Warning: {name} is a critical component")
        
        # Check hybrid components
        print("\n🎯 HYBRID COMPONENTS:")
        print("-" * 40)
        
        components = status.get('hybrid_components', {})
        
        # Rate Limiter
        if 'rate_limiter' in components:
            rl_stats = components['rate_limiter']
            print(f"📊 Rate Limiter: Active")
            print(f"   - Total requests: {rl_stats.get('total_requests', 0)}")
            print(f"   - Active clients: {len(rl_stats.get('clients', {}))}")
        
        # FAQ Classifier
        if 'faq_classifier' in components:
            faq_stats = components['faq_classifier']
            print(f"❓ FAQ Classifier: Active")
            print(f"   - Total classifications: {faq_stats.get('total_classifications', 0)}")
            print(f"   - Hit rate: {faq_stats.get('faq_hit_rate', 0):.1%}")
        
        # Emergency Mode
        if 'emergency_mode' in components:
            em_status = components['emergency_mode']
            em_icon = "🚨" if em_status.get('is_active') else "✅"
            print(f"{em_icon} Emergency Mode: {'ACTIVE' if em_status.get('is_active') else 'Inactive'}")
            if em_status.get('is_active'):
                print(f"   - Reason: {em_status.get('reason')}")
                print(f"   - Duration: {em_status.get('duration_seconds')}s")
        
        # Safety Checker
        if 'safety_checker' in components:
            safety_stats = components['safety_checker']
            print(f"🛡️ Safety Checker: Active")
            print(f"   - Total checks: {safety_stats.get('total_checks', 0)}")
            print(f"   - Pass rate: {safety_stats.get('pass_rate', 100):.1%}")
        
        # i18n Service
        if 'i18n_service' in components:
            i18n_stats = components['i18n_service']
            print(f"🌍 i18n Service: Active")
            print(f"   - Languages: {', '.join(i18n_stats.get('supported_languages', []))}")
            print(f"   - Translations: {i18n_stats.get('total_translations', 0)}")
        
        # Vector Store Stats
        if 'vector_store_stats' in status:
            vs_stats = status['vector_store_stats']
            print(f"\n📚 VECTOR STORE:")
            print("-" * 40)
            print(f"   - Documents: {vs_stats.get('total_documents', 0)}")
            print(f"   - Embeddings: {vs_stats.get('total_embeddings', 0)}")
            print(f"   - Collection: {vs_stats.get('collection_name', 'default')}")
        
        # Performance Check
        print("\n⚡ PERFORMANCE TEST:")
        print("-" * 40)
        
        # Test response time
        start_time = time.time()
        test_response = orchestrator.process_hybrid_request(
            message="test",
            client_identifier="health_check",
            target_language="es"
        )
        response_time = (time.time() - start_time) * 1000
        
        if test_response.get('success'):
            print(f"✅ Response Time: {response_time:.0f}ms")
            if response_time < 500:
                print("   - Performance: Excellent")
            elif response_time < 1000:
                print("   - Performance: Good")
            elif response_time < 2000:
                print("   - Performance: Acceptable")
            else:
                print("   - Performance: Needs optimization")
        else:
            print(f"❌ Test request failed: {test_response.get('error')}")
        
        # Overall Status
        print("\n📋 OVERALL STATUS:")
        print("-" * 40)
        
        critical_ok = all([
            providers.get('llm', {}).get('available', False),
            providers.get('vector_store', {}).get('available', False),
            status.get('initialized', False)
        ])
        
        if critical_ok:
            print("✅ SYSTEM STATUS: OPERATIONAL")
            print("   All critical components are functioning")
        else:
            print("⚠️  SYSTEM STATUS: DEGRADED")
            print("   Some critical components are unavailable")
            if not status.get('initialized'):
                print("   - Documents not initialized")
            if not providers.get('llm', {}).get('available'):
                print("   - LLM provider unavailable")
            if not providers.get('vector_store', {}).get('available'):
                print("   - Vector store unavailable")
        
        print("\n" + "=" * 60)
        
        # Return exit code
        return 0 if critical_ok else 1
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("=" * 60)
        return 2

def continuous_monitoring(interval=30):
    """Run continuous health monitoring"""
    print("Starting continuous health monitoring...")
    print(f"Checking every {interval} seconds. Press Ctrl+C to stop.\n")
    
    try:
        while True:
            exit_code = run_health_check()
            
            if exit_code != 0:
                print("\n⚠️ ALERT: System health check failed!")
            
            time.sleep(interval)
            print("\n" * 2)  # Clear space for next check
            
    except KeyboardInterrupt:
        print("\n\nStopping health monitoring...")
        return 0

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Health check for hybrid chatbot system')
    parser.add_argument('--continuous', '-c', action='store_true',
                       help='Run continuous monitoring')
    parser.add_argument('--interval', '-i', type=int, default=30,
                       help='Monitoring interval in seconds (default: 30)')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')
    
    args = parser.parse_args()
    
    if args.continuous:
        return continuous_monitoring(args.interval)
    else:
        return run_health_check()

if __name__ == '__main__':
    sys.exit(main())
