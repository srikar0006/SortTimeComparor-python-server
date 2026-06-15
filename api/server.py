from http.server import BaseHTTPRequestHandler
import json
import time


def bubble_sort(numbers):
    arr = numbers[:]
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def merge_sort(numbers):
    if len(numbers) <= 1:
        return numbers

    mid = len(numbers) // 2
    left = merge_sort(numbers[:mid])
    right = merge_sort(numbers[mid:])

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def measure_time(sort_function, numbers):
    start = time.time()
    sorted_numbers = sort_function(numbers)
    end = time.time()

    return sorted_numbers, (end - start) * 1000


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json(200, {"ok": True})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))

            numbers = payload.get("numbers", [])

            if not numbers or not isinstance(numbers, list):
                self._send_json(
                    400,
                    {"error": "Please send a non-empty list of numbers."}
                )
                return

            bubble_sorted, bubble_ms = measure_time(bubble_sort, numbers)
            merge_sorted, merge_ms = measure_time(merge_sort, numbers)

            self._send_json(
                200,
                {
                    "inputSize": len(numbers),
                    "sortedNumbers": merge_sorted,
                    "bubbleSort": {
                        "name": "Bubble Sort",
                        "timeComplexity": "O(n^2)",
                        "elapsedMs": round(bubble_ms, 5),
                    },
                    "mergeSort": {
                        "name": "Merge Sort",
                        "timeComplexity": "O(n log n)",
                        "elapsedMs": round(merge_ms, 5),
                    },
                },
            )

        except Exception as error:
            self._send_json(500, {"error": str(error)})
