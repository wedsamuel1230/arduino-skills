#!/usr/bin/env python3
"""
Arduino Serial Monitor - Enhanced debugging tool for Arduino serial output
"""

import serial
import serial.tools.list_ports
import argparse
import re
import json
import time
import sys
from datetime import datetime
import colorama
from colorama import Fore, Back, Style

colorama.init()

class ArduinoSerialMonitor:
    def __init__(self, port, baud=9600, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.serial_conn = None

    def connect(self):
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            print(f"Connected to {self.port} at {self.baud} baud")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            return False

    def disconnect(self):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print(f"Disconnected from {self.port}")

    def read_line(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            return None
        try:
            line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
            return line if line else None
        except serial.SerialException:
            return None

def detect_errors(line):
    """Detect common Arduino error patterns"""
    error_patterns = [
        r'error|Error|ERROR',
        r'exception|Exception|EXCEPTION',
        r'failed|Failed|FAILED',
        r'timeout|Timeout|TIMEOUT',
        r'overflow|Overflow|OVERFLOW',
        r'out of memory|Out of memory',
        r'stack overflow|Stack overflow',
        r'panic|Panic|PANIC'
    ]

    for pattern in error_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False

def format_json(line, pretty=False):
    """Try to parse and format JSON"""
    try:
        data = json.loads(line)
        if pretty:
            return json.dumps(data, indent=2)
        else:
            return json.dumps(data)
    except json.JSONDecodeError:
        return line

def colorize_line(line, detect_errors_flag=False):
    """Add color coding to output"""
    if detect_errors_flag and detect_errors(line):
        return Fore.RED + line + Style.RESET_ALL
    elif 'WARNING' in line.upper():
        return Fore.YELLOW + line + Style.RESET_ALL
    elif 'INFO' in line.upper():
        return Fore.BLUE + line + Style.RESET_ALL
    elif 'DEBUG' in line.upper():
        return Fore.GREEN + line + Style.RESET_ALL
    else:
        return line

def list_ports():
    """List available serial ports"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found")
        return

    print("Available serial ports:")
    for port in ports:
        print(f"  {port.device}: {port.description}")

def main():
    parser = argparse.ArgumentParser(description='Arduino Serial Monitor - Enhanced debugging tool')
    parser.add_argument('--port', '-p', required=True, help='Serial port (e.g., COM3, /dev/ttyACM0)')
    parser.add_argument('--baud', '-b', type=int, default=9600, help='Baud rate (default: 9600)')
    parser.add_argument('--output', '-o', help='Output file for logging')
    parser.add_argument('--filter', '-f', help='Regex pattern to filter lines')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text', help='Data format')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON')
    parser.add_argument('--timestamp', '-t', action='store_true', help='Add timestamps')
    parser.add_argument('--color', '-c', action='store_true', help='Enable color output')
    parser.add_argument('--detect-errors', '-e', action='store_true', help='Highlight error patterns')
    parser.add_argument('--timeout', type=int, default=1, help='Connection timeout in seconds')
    parser.add_argument('--list-ports', '-l', action='store_true', help='List available serial ports')

    args = parser.parse_args()

    if args.list_ports:
        list_ports()
        return

    # Initialize monitor
    monitor = ArduinoSerialMonitor(args.port, args.baud, args.timeout)

    # Connect
    if not monitor.connect():
        sys.exit(1)

    # Open output file if specified
    output_file = None
    if args.output:
        try:
            output_file = open(args.output, 'a', encoding='utf-8')
            print(f"Logging to {args.output}")
        except IOError as e:
            print(f"Error opening output file: {e}")
            monitor.disconnect()
            sys.exit(1)

    # Compile filter regex if specified
    filter_regex = None
    if args.filter:
        try:
            filter_regex = re.compile(args.filter, re.IGNORECASE)
        except re.error as e:
            print(f"Invalid regex pattern: {e}")
            monitor.disconnect()
            if output_file:
                output_file.close()
            sys.exit(1)

    print("Monitoring serial output... (Ctrl+C to stop)")

    try:
        while True:
            line = monitor.read_line()
            if line is None:
                continue

            # Apply filtering
            if filter_regex and not filter_regex.search(line):
                continue

            # Format data
            if args.format == 'json':
                line = format_json(line, args.pretty)
            # CSV format could be added here

            # Add timestamp
            if args.timestamp:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                line = f"[{timestamp}] {line}"

            # Colorize
            if args.color or args.detect_errors:
                line = colorize_line(line, args.detect_errors)

            # Print to console
            print(line)

            # Write to file
            if output_file:
                # Remove ANSI color codes for file output
                clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                output_file.write(clean_line + '\n')
                output_file.flush()

    except KeyboardInterrupt:
        print("\nStopping monitor...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        monitor.disconnect()
        if output_file:
            output_file.close()

if __name__ == '__main__':
    main()