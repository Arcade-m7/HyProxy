"""
Config LOG Example 2: Controlling Stream Output

StreamOutput handlers can be enabled/disabled at runtime.

Methods:
- stream.enable() - Attach handler to logger (start logging)
- stream.desible() - Remove handler from logger (stop logging)
- stream.reinit(stream=None) - Reinitialize with different stream

Use Cases:
- Production: Enable logging for auditing
- Debug mode: Detailed logging
- Performance optimization: Disable logging on high-traffic listeners
- Log rotation: Reinitialize with new stream file

Logger Format:
Each log entry contains:
- Timestamp (automatic)
- Log level (DEBUG, INFO, WARNING, ERROR)
- Message (formatted log content)
"""

from hyproxy import Server, Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


def main():
    """Create listeners with different logging configurations."""
    
    # Production listener: Default logging enabled
    prod_config = Config()
    # Logging enabled by default
    
    prod_listener = Asynclestener(
        name='ProductionProxy',
        ip='127.0.0.1',
        port=1968,
        protocols=[HTTP1O1(prod_config), SOCKS4(prod_config), SOCKS5(prod_config)]
    )
    
    # Development listener: Also has logging
    dev_config = Config()
    # Could manually control stream with config.log.stream.desible()
    # to temporarily disable logging for testing
    
    dev_listener = Asynclestener(
        name='DevelopmentProxy',
        ip='127.0.0.1',
        port=1969,
        protocols=[HTTP1O1(dev_config), SOCKS4(dev_config), SOCKS5(dev_config)]
    )
    
    # High-performance listener: Could disable logging
    perf_config = Config()
    # Stream output is managed internally by the logger
    # Disable logging for high-traffic scenarios by disabling handler
    try:
        perf_config.log.stream.desible()
    except:
        # If stream is not yet attached, this may fail (OK)
        pass
    
    perf_listener = Asynclestener(
        name='HighPerformanceProxy',
        ip='127.0.0.1',
        port=1970,
        protocols=[HTTP1O1(perf_config), SOCKS4(perf_config), SOCKS5(perf_config)]
    )
    
    server = Server(prod_listener, dev_listener, perf_listener)
    
    print("[*] Starting server with selective logging...")
    print()
    print("[*] Port 1968 (Production): Logging ENABLED")
    print("    All connections logged for auditing")
    print()
    print("[*] Port 1969 (Development): Logging ENABLED")
    print("    Detailed debugging information available")
    print()
    print("[*] Port 1970 (HighPerformance): Logging DISABLED")
    print("    Optimized for throughput, minimal logging overhead")
    print()
    server.run()


if __name__ == '__main__':
    main()
