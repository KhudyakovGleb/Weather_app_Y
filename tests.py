import unittest
from fastapi.testclient import TestClient
from main import app
from uuid import uuid4


class TestWeatherApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_info(self):
        response = self.client.get("/info")
        self.assertEqual(response.status_code, 200)
        self.assertIn("version", response.json())
        self.assertIn("service", response.json())
        self.assertIn("author", response.json())

    def test_get_weather_data(self):
        response = self.client.get(
            "/info/weather?geo_place=Russia,%20Saint-Petersburg&date_start=2025-02-19&date_end=2025-02-20"
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertIn("data", response_json)
        self.assertIn("weather_stats", response_json["data"])
        weather_stats = response_json["data"]["weather_stats"]
        self.assertIn("average", weather_stats)
        self.assertIn("median", weather_stats)
        self.assertIn("min", weather_stats)
        self.assertIn("max", weather_stats)

    def test_get_all_weather_data(self):
        response = self.client.get(
            "/info/weather?geo_place=Russia,%20Saint-Petersburg&date_start=2025-02-19&date_end=2025-02-20"
        )
        response = self.client.get("/info/allresponses")
        self.assertEqual(response.status_code, 200)

        response_json = response.json()

        self.assertTrue(response_json)

        first_key = next(iter(response_json))

        self.assertIn("id", response_json[first_key])
        self.assertIn("geo_place", response_json[first_key])
        self.assertIn("date_start", response_json[first_key])
        self.assertIn("date_end", response_json[first_key])
        self.assertIn("temp_value", response_json[first_key])
        self.assertIn("median_value", response_json[first_key])
        self.assertIn("avg_value", response_json[first_key])
        self.assertIn("min_value", response_json[first_key])
        self.assertIn("max_value", response_json[first_key])

        self.assertEqual(
            response_json[first_key]["geo_place"], "Russia, Saint-Petersburg"
        )
        self.assertEqual(response_json[first_key]["date_start"], "2025-02-19")
        self.assertEqual(response_json[first_key]["date_end"], "2025-02-20")
        self.assertEqual(response_json[first_key]["temp_value"], [-6.4, -8.5])
        self.assertEqual(response_json[first_key]["median_value"], -7.45)
        self.assertEqual(response_json[first_key]["avg_value"], -7.45)
        self.assertEqual(response_json[first_key]["min_value"], -8.5)
        self.assertEqual(response_json[first_key]["max_value"], -6.4)

    def test_get_weather_data_by_id_not_found(self):
        non_existent_id = uuid4()
        response = self.client.get(f"/info/responce/{non_existent_id}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "ID not found"})

    def test_delete_weather_data_by_id(self):
        response = self.client.get(
            "/info/weather?geo_place=Russia,%20Saint-Petersburg&date_start=2025-02-19&date_end=2025-02-20"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/info/allresponses")
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertTrue(response_json)

        weather_id = next(iter(response_json))

        response = self.client.delete(f"/info/responcedel/{weather_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Deleted successfully"})

        response = self.client.get(f"/info/responce/{weather_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
