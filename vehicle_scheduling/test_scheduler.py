"""
Unit tests for the Vehicle Maintenance Scheduler (knapsack solver).
Run with:  python test_scheduler.py
All tests must pass before submission.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vehicle_scheduling.scheduler import knapsack, schedule_depot


class TestKnapsack(unittest.TestCase):

    def test_empty_tasks(self):
        impact, chosen = knapsack([], 100)
        self.assertEqual(impact, 0)
        self.assertEqual(chosen, [])

    def test_zero_capacity(self):
        tasks = [{"TaskID": "t1", "Duration": 2, "Impact": 5}]
        impact, chosen = knapsack(tasks, 0)
        self.assertEqual(impact, 0)
        self.assertEqual(chosen, [])

    def test_single_task_fits(self):
        tasks = [{"TaskID": "t1", "Duration": 3, "Impact": 7}]
        impact, chosen = knapsack(tasks, 5)
        self.assertEqual(impact, 7)
        self.assertEqual(len(chosen), 1)
        self.assertEqual(chosen[0]["TaskID"], "t1")

    def test_single_task_does_not_fit(self):
        tasks = [{"TaskID": "t1", "Duration": 10, "Impact": 7}]
        impact, chosen = knapsack(tasks, 5)
        self.assertEqual(impact, 0)
        self.assertEqual(chosen, [])

    def test_classic_knapsack(self):
        # Classic example: capacity=5, optimal = tasks 0+1 (impact 3+4=7)
        tasks = [
            {"TaskID": "A", "Duration": 2, "Impact": 3},
            {"TaskID": "B", "Duration": 3, "Impact": 4},
            {"TaskID": "C", "Duration": 4, "Impact": 5},
        ]
        impact, chosen = knapsack(tasks, 5)
        self.assertEqual(impact, 7)
        chosen_ids = {t["TaskID"] for t in chosen}
        self.assertEqual(chosen_ids, {"A", "B"})

    def test_all_tasks_fit(self):
        tasks = [
            {"TaskID": "A", "Duration": 1, "Impact": 10},
            {"TaskID": "B", "Duration": 2, "Impact": 5},
            {"TaskID": "C", "Duration": 3, "Impact": 8},
        ]
        impact, chosen = knapsack(tasks, 100)
        self.assertEqual(impact, 23)
        self.assertEqual(len(chosen), 3)

    def test_greedy_not_optimal(self):
        # Greedy (best ratio) picks A (impact/dur = 5), but optimal picks B+C
        tasks = [
            {"TaskID": "A", "Duration": 3, "Impact": 15},   # ratio = 5
            {"TaskID": "B", "Duration": 2, "Impact": 10},   # ratio = 5
            {"TaskID": "C", "Duration": 2, "Impact": 11},   # ratio = 5.5
        ]
        impact, chosen = knapsack(tasks, 4)
        # B+C = 10+11 = 21, A = 15 → optimal is B+C
        self.assertEqual(impact, 21)
        chosen_ids = {t["TaskID"] for t in chosen}
        self.assertIn("B", chosen_ids)
        self.assertIn("C", chosen_ids)

    def test_selected_tasks_within_capacity(self):
        tasks = [
            {"TaskID": str(i), "Duration": i % 5 + 1, "Impact": i % 10 + 1}
            for i in range(20)
        ]
        capacity = 30
        impact, chosen = knapsack(tasks, capacity)
        total_dur = sum(t["Duration"] for t in chosen)
        self.assertLessEqual(total_dur, capacity)
        total_impact = sum(t["Impact"] for t in chosen)
        self.assertEqual(total_impact, impact)

    def test_no_duplicate_tasks_selected(self):
        tasks = [
            {"TaskID": "X", "Duration": 2, "Impact": 6},
            {"TaskID": "Y", "Duration": 2, "Impact": 6},
        ]
        _, chosen = knapsack(tasks, 2)
        # Only one task should be selected (capacity=2 allows only one)
        self.assertEqual(len(chosen), 1)

    def test_impact_is_maximised(self):
        # Brute-force all subsets and compare
        tasks = [
            {"TaskID": str(i), "Duration": (i % 4) + 1, "Impact": (i % 7) + 1}
            for i in range(10)
        ]
        capacity = 15
        dp_impact, _ = knapsack(tasks, capacity)

        # Brute force
        best = 0
        for mask in range(1 << len(tasks)):
            total_dur = total_imp = 0
            for j in range(len(tasks)):
                if mask & (1 << j):
                    total_dur += tasks[j]["Duration"]
                    total_imp += tasks[j]["Impact"]
            if total_dur <= capacity and total_imp > best:
                best = total_imp

        self.assertEqual(dp_impact, best)

    def test_large_input_performance(self):
        import time
        tasks = [
            {"TaskID": str(i), "Duration": (i % 8) + 1, "Impact": (i % 10) + 1}
            for i in range(500)
        ]
        capacity = 188
        start = time.time()
        impact, chosen = knapsack(tasks, capacity)
        elapsed = time.time() - start
        self.assertLess(elapsed, 10.0, "Knapsack too slow for 500 tasks")
        total_dur = sum(t["Duration"] for t in chosen)
        self.assertLessEqual(total_dur, capacity)


class TestScheduleDepot(unittest.TestCase):

    def test_depot_result_structure(self):
        depot = {"ID": 3, "MechanicHours": 10}
        tasks = [
            {"TaskID": "t1", "Duration": 3, "Impact": 7},
            {"TaskID": "t2", "Duration": 4, "Impact": 5},
            {"TaskID": "t3", "Duration": 5, "Impact": 9},
        ]
        result = schedule_depot(depot, tasks)
        self.assertIn("DepotID", result)
        self.assertIn("MechanicHoursAvailable", result)
        self.assertIn("MechanicHoursUsed", result)
        self.assertIn("TotalImpact", result)
        self.assertIn("TasksSelected", result)
        self.assertIn("Tasks", result)
        self.assertEqual(result["DepotID"], 3)
        self.assertLessEqual(result["MechanicHoursUsed"], 10)

    def test_hours_used_matches_tasks(self):
        depot = {"ID": 1, "MechanicHours": 60}
        tasks = [
            {"TaskID": str(i), "Duration": i % 6 + 1, "Impact": i % 8 + 1}
            for i in range(15)
        ]
        result = schedule_depot(depot, tasks)
        computed_hours = sum(t["Duration"] for t in result["Tasks"])
        self.assertEqual(result["MechanicHoursUsed"], computed_hours)

    def test_impact_matches_tasks(self):
        depot = {"ID": 2, "MechanicHours": 50}
        tasks = [
            {"TaskID": str(i), "Duration": 5, "Impact": i + 1}
            for i in range(10)
        ]
        result = schedule_depot(depot, tasks)
        computed_impact = sum(t["Impact"] for t in result["Tasks"])
        self.assertEqual(result["TotalImpact"], computed_impact)

    def test_mock_depots_five_depots(self):
        from vehicle_scheduling.scheduler import MOCK_DEPOTS, MOCK_VEHICLES
        results = [schedule_depot(d, MOCK_VEHICLES) for d in MOCK_DEPOTS]
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertLessEqual(r["MechanicHoursUsed"], r["MechanicHoursAvailable"])
            self.assertGreater(r["TotalImpact"], 0)


if __name__ == "__main__":
    print("Running Vehicle Scheduling Tests...\n")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
