Examples
========

This page contains practical examples of using Quamina in different scenarios.

Basic Examples
--------------

Simple Pattern Matching
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina

   q = Quamina()

   # Add patterns
   q.add_pattern("numbers", {"x": [1, 2, 3]})
   q.add_pattern("strings", {"name": ["Alice", "Bob"]})

   # Match events
   print(q.matches_for_event({"x": 2}))  # ['numbers']
   print(q.matches_for_event({"name": "Alice"}))  # ['strings']
   print(q.matches_for_event({"x": 99}))  # []

Multiple Patterns Matching
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina

   q = Quamina()

   # Add patterns that overlap
   q.add_pattern("all-orders", {"type": ["order"]})
   q.add_pattern("completed-orders", {
       "type": ["order"],
       "status": ["completed"]
   })
   q.add_pattern("high-value", {"amount": [1000, 2000, 5000]})

   # This matches two patterns
   matches = q.matches_for_event({
       "type": "order",
       "status": "completed",
       "amount": 1000
   })
   print(matches)  # ['all-orders', 'completed-orders', 'high-value']

Event-Driven Applications
--------------------------

Order Processing System
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina
   from typing import Any

   class OrderProcessor:
       def __init__(self):
           self.q = Quamina()
           self._setup_handlers()

       def _setup_handlers(self):
           # Handle new orders
           @self.q.handler("new-orders", {
               "event_type": ["order.created"]
           })
           def handle_new_order(event: dict[str, Any]) -> None:
               print(f"Processing new order: {event['order_id']}")
               # Send to fulfillment system
               self._send_to_fulfillment(event)

           # Handle high-value orders
           @self.q.handler("high-value-orders", {
               "event_type": ["order.created"],
               "total_amount": [1000, 2000, 5000]
           })
           def handle_high_value_order(event: dict[str, Any]) -> None:
               print(f"High value order detected: ${event['total_amount']}")
               # Send notification to sales team
               self._notify_sales_team(event)

           # Handle international orders
           @self.q.handler("international-orders", {
               "event_type": ["order.created"],
               "country": ["UK", "FR", "DE", "JP"]
           })
           def handle_international_order(event: dict[str, Any]) -> None:
               print(f"International order from {event['country']}")
               # Calculate customs and shipping
               self._calculate_international_shipping(event)

       def process_event(self, event: dict[str, Any]) -> None:
           """Process an order event through all registered handlers."""
           results = self.q.process_event(event)
           print(f"Event processed by {len(results)} handlers")

       def _send_to_fulfillment(self, event):
           pass  # Implementation here

       def _notify_sales_team(self, event):
           pass  # Implementation here

       def _calculate_international_shipping(self, event):
           pass  # Implementation here

   # Usage
   processor = OrderProcessor()
   processor.process_event({
       "event_type": "order.created",
       "order_id": "ORD-12345",
       "total_amount": 1500,
       "country": "UK"
   })

Alert System
~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   class AlertSystem:
       def __init__(self):
           self.q = Quamina()
           self._setup_alerts()

       def _setup_alerts(self):
           # Critical errors
           @self.q.handler("critical-errors", {
               "level": ["critical", "fatal"],
               "service": ["api", "database", "payment"]
           })
           def alert_critical(event):
               logger.critical(f"CRITICAL: {event['message']}")
               self._page_oncall(event)

           # High error rates
           @self.q.handler("high-error-rate", {
               "metric": ["error_rate"],
               "value": [50, 75, 100]  # Percentage
           })
           def alert_high_errors(event):
               logger.error(f"High error rate: {event['value']}%")
               self._notify_slack(event)

           # Resource exhaustion
           @self.q.handler("resource-exhaustion", {
               "resource": ["memory", "disk", "cpu"],
               "usage_percent": [90, 95, 98]
           })
           def alert_resources(event):
               logger.warning(f"High resource usage: {event}")
               self._scale_infrastructure(event)

       def process_metric(self, metric: dict) -> None:
           self.q.process_event(metric)

       def _page_oncall(self, event):
           print(f"Paging on-call engineer: {event}")

       def _notify_slack(self, event):
           print(f"Sending Slack notification: {event}")

       def _scale_infrastructure(self, event):
           print(f"Auto-scaling resources: {event['resource']}")

   # Usage
   alerts = AlertSystem()
   alerts.process_metric({
       "level": "critical",
       "service": "api",
       "message": "API service down"
   })

Data Pipeline
-------------

Stream Processing
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina
   from typing import Any, Iterator

   class StreamProcessor:
       def __init__(self):
           self.q = Quamina()
           self.processed_count = 0
           self.matched_count = 0

       def add_filter(self, filter_id: str, pattern: dict[str, list[Any]]) -> None:
           """Add a filter pattern to the stream processor."""
           self.q.add_pattern(filter_id, pattern)

       def process_stream(self, events: Iterator[dict[str, Any]]) -> Iterator[tuple[dict, list[str]]]:
           """Process a stream of events, yielding events with their matches."""
           for event in events:
               self.processed_count += 1
               matches = self.q.matches_for_event(event)
               if matches:
                   self.matched_count += 1
                   yield event, matches

       def get_stats(self) -> dict[str, int]:
           """Get processing statistics."""
           return {
               "processed": self.processed_count,
               "matched": self.matched_count,
               "match_rate": (
                   self.matched_count / self.processed_count
                   if self.processed_count > 0
                   else 0
               )
           }

   # Usage
   processor = StreamProcessor()

   # Define filters
   processor.add_filter("errors", {"level": ["error", "critical"]})
   processor.add_filter("slow-requests", {"duration_ms": [1000, 2000, 5000]})

   # Process stream
   events = [
       {"level": "info", "message": "Request completed"},
       {"level": "error", "message": "Database timeout"},
       {"level": "info", "duration_ms": 150, "endpoint": "/api/users"},
       {"level": "warning", "duration_ms": 2000, "endpoint": "/api/search"},
   ]

   for event, matches in processor.process_stream(iter(events)):
       print(f"Event {event} matched filters: {matches}")

   print(f"Statistics: {processor.get_stats()}")

ETL Pipeline
~~~~~~~~~~~~

.. code-block:: python

   from quamina import Quamina
   from typing import Any

   class ETLPipeline:
       def __init__(self):
           self.q = Quamina()
           self._setup_transformations()
           self.output_buckets = {
               "analytics": [],
               "archive": [],
               "alerts": []
           }

       def _setup_transformations(self):
           @self.q.handler("analytics-events", {
               "event_type": ["page_view", "click", "purchase"]
           })
           def route_to_analytics(event):
               self.output_buckets["analytics"].append(event)

           @self.q.handler("archive-all", {
               "event_type": ["page_view", "click", "purchase", "error"]
           })
           def route_to_archive(event):
               self.output_buckets["archive"].append(event)

           @self.q.handler("alert-events", {
               "event_type": ["error"],
               "severity": ["high", "critical"]
           })
           def route_to_alerts(event):
               self.output_buckets["alerts"].append(event)

       def process_batch(self, events: list[dict[str, Any]]) -> dict[str, list]:
           """Process a batch of events and route to appropriate buckets."""
           for event in events:
               self.q.process_event(event)

           return self.output_buckets

   # Usage
   pipeline = ETLPipeline()
   events = [
       {"event_type": "page_view", "page": "/home"},
       {"event_type": "click", "button": "signup"},
       {"event_type": "error", "severity": "high", "message": "API timeout"},
       {"event_type": "purchase", "amount": 99.99},
   ]

   results = pipeline.process_batch(events)
   print(f"Analytics: {len(results['analytics'])} events")
   print(f"Archive: {len(results['archive'])} events")
   print(f"Alerts: {len(results['alerts'])} events")

Integration Examples
--------------------

With Flask
~~~~~~~~~~

.. code-block:: python

   from flask import Flask, request, jsonify
   from quamina import Quamina

   app = Flask(__name__)
   q = Quamina()

   # Setup patterns
   q.add_pattern("webhook-github", {
       "source": ["github"],
       "event": ["push", "pull_request"]
   })

   q.add_pattern("webhook-slack", {
       "source": ["slack"],
       "event": ["message"]
   })

   @app.route('/webhook', methods=['POST'])
   def handle_webhook():
       event = request.json

       # Match against patterns
       matches = q.matches_for_event(event)

       if not matches:
           return jsonify({"error": "No matching handlers"}), 404

       # Process based on matches
       results = []
       for pattern_id in matches:
           if pattern_id == "webhook-github":
               result = handle_github_event(event)
           elif pattern_id == "webhook-slack":
               result = handle_slack_event(event)
           results.append(result)

       return jsonify({"processed": len(results)})

   def handle_github_event(event):
       print(f"GitHub event: {event['event']}")
       return {"status": "processed"}

   def handle_slack_event(event):
       print(f"Slack event: {event['event']}")
       return {"status": "processed"}

   if __name__ == '__main__':
       app.run(debug=True)

With AsyncIO
~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from quamina import Quamina
   from typing import Any

   class AsyncEventProcessor:
       def __init__(self):
           self.q = Quamina()

       def add_pattern(self, pattern_id: str, pattern: dict[str, list[Any]]):
           """Add a pattern (synchronous)."""
           self.q.add_pattern(pattern_id, pattern)

       async def process_event_async(self, event: dict[str, Any]) -> list[str]:
           """Process an event asynchronously."""
           # Pattern matching is fast and synchronous
           matches = self.q.matches_for_event(event)

           # But you can do async processing based on matches
           tasks = []
           for match in matches:
               tasks.append(self._handle_match_async(match, event))

           results = await asyncio.gather(*tasks)
           return results

       async def _handle_match_async(self, match: str, event: dict[str, Any]) -> str:
           """Handle a match asynchronously."""
           # Simulate async I/O (e.g., API call, database write)
           await asyncio.sleep(0.1)
           return f"Processed {match} for event {event}"

   # Usage
   async def main():
       processor = AsyncEventProcessor()
       processor.add_pattern("orders", {"type": ["order"]})
       processor.add_pattern("high-value", {"amount": [1000, 2000]})

       event = {"type": "order", "amount": 1000}
       results = await processor.process_event_async(event)
       print(results)

   asyncio.run(main())

Testing Examples
----------------

Unit Testing with Quamina
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from quamina import Quamina, QuaminaError

   def test_basic_matching():
       q = Quamina()
       q.add_pattern("test", {"x": [1, 2, 3]})

       # Test match
       assert q.matches_for_event({"x": 2}) == ["test"]

       # Test no match
       assert q.matches_for_event({"x": 99}) == []

   def test_multiple_patterns():
       q = Quamina()
       q.add_pattern("p1", {"type": ["A"]})
       q.add_pattern("p2", {"type": ["A"], "value": [1]})

       # Both patterns match
       matches = q.matches_for_event({"type": "A", "value": 1})
       assert set(matches) == {"p1", "p2"}

       # Only p1 matches
       matches = q.matches_for_event({"type": "A", "value": 2})
       assert matches == ["p1"]

   def test_pattern_deletion():
       q = Quamina()
       q.add_pattern("temp", {"x": [1]})

       # Pattern exists
       assert q.matches_for_event({"x": 1}) == ["temp"]

       # Delete pattern
       q.delete_patterns("temp")

       # Pattern gone
       assert q.matches_for_event({"x": 1}) == []

   def test_handler_functionality():
       q = Quamina()
       results = []

       @q.handler("test", {"x": [1]})
       def my_handler(event):
           results.append(event["x"])
           return "processed"

       # Process event
       return_values = q.process_event({"x": 1})

       assert results == [1]
       assert return_values == ["processed"]

   def test_context_manager():
       with Quamina() as q:
           q.add_pattern("test", {"x": [1]})
           matches = q.matches_for_event({"x": 1})
           assert matches == ["test"]
       # Automatically cleaned up

Performance Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from quamina import Quamina
   import time

   @pytest.mark.benchmark
   def test_matching_performance(benchmark):
       q = Quamina()
       q.add_pattern("test", {"x": [1, 2, 3]})
       event = {"x": 2}

       result = benchmark(q.matches_for_event, event)
       assert result == ["test"]

   def test_scalability():
       q = Quamina()

       # Add many patterns
       num_patterns = 1000
       for i in range(num_patterns):
           q.add_pattern(f"pattern-{i}", {"id": [i]})

       # Measure matching time
       start = time.time()
       for i in range(100):
           q.matches_for_event({"id": i})
       elapsed = time.time() - start

       avg_time = elapsed / 100
       print(f"Average match time with {num_patterns} patterns: {avg_time*1000:.2f}ms")
       assert avg_time < 0.01  # Should be under 10ms
