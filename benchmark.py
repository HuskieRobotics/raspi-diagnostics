# adapted from https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd

import subprocess
import time
import datetime
import csv
import argparse

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_cpu_temp():
    temp_output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    return temp_output.split('=')[1].split("'")[0]

def get_cpu_clock_speed():
    clock_output = subprocess.check_output(["vcgencmd", "measure_clock", "arm"]).decode()
    return str(int(clock_output.split('=')[1]) // 1000000)

def get_pmic_ext5v_voltage():
    voltage_output = subprocess.check_output(["vcgencmd", "pmic_read_adc", "EXT5V_V"]).decode()
    return voltage_output.split('=')[1].split("V")[0]

def get_throttled_status():
    throttled_output = subprocess.check_output(["vcgencmd", "get_throttled"]).decode()
    return throttled_output.split('=')[1].strip()

def log_benchmark_data(output_file, duration):
    with open(output_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(duration):
            timestamp = get_timestamp()
            cpu_temp = get_cpu_temp()
            cpu_clock_speed = get_cpu_clock_speed()
            voltage = get_pmic_ext5v_voltage()
            throttled_status = get_throttled_status()
            
            writer.writerow([timestamp, cpu_temp, cpu_clock_speed, voltage, throttled_status])
            
            if (i % 10 == 0):
	            print(f"{timestamp}, {cpu_temp}, {cpu_clock_speed}, {voltage}, {throttled_status}")
            if (int(throttled_status, 0) & 1):
            	print(f"{timestamp}, *** currently under-voltage ***")
            time.sleep(1)

def main(stress_duration):
    output_file = "benchmark.csv"
    # Write header
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp", "CPU Temperature (°C)", "CPU Clock Speed (MHz)", "EXT5V (V)", "CPU Throttled"])

    print("Idle data for 60 seconds")
    log_benchmark_data(output_file, 60)

    print(f"Starting stress test for {stress_duration} seconds")
    subprocess.Popen(["stress", "--cpu", "4", "-t", str(stress_duration)])
    log_benchmark_data(output_file, stress_duration)

    print("Cool down data for 60 seconds")
    log_benchmark_data(output_file, 60)

    print("Benchmark complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Raspberry Pi benchmark tool with a stress test.")
    parser.add_argument("stress_duration", type=int, help="Duration of the stress test in seconds")
    args = parser.parse_args()

    main(args.stress_duration)
