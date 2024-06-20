import unittest
import json
from unittest.mock import patch, MagicMock
from client3 import getDataPoint, getRatio

class TestGetDataPoint(unittest.TestCase):
    
    def test_getDataPoint(self):
        quotes = [
            {'stock': 'ABC', 'top_bid': {'price': 120.48}, 'top_ask': {'price': 121.2}},
            {'stock': 'DEF', 'top_bid': {'price': 117.87}, 'top_ask': {'price': 121.68}}
        ]
        
        expected_data_points = [
            ('ABC', 120.48, 121.2, 120.84),
            ('DEF', 117.87, 121.68, 119.775)
        ]
        
        for i, quote in enumerate(quotes):
            with self.subTest(quote=quote):
                # Act
                data_point = getDataPoint(quote)
                
                # Assert
                self.assertEqual(data_point, expected_data_points[i])

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'stock': 'ABC', 'top_bid': {'price': 120.48}, 'top_ask': {'price': 119.2}},
            {'stock': 'DEF', 'top_bid': {'price': 117.87}, 'top_ask': {'price': 121.68}}
        ]
        
        expected_data_points = [
            ('ABC', 120.48, 119.2, 119.84),
            ('DEF', 117.87, 121.68, 119.775)
        ]
        
        for i, quote in enumerate(quotes):
            with self.subTest(quote=quote):
                # Act
                data_point = getDataPoint(quote)
                
                # Assert
                self.assertEqual(data_point, expected_data_points[i])

    def test_getRatio(self):
        # Arrange
        price_a = 100.0
        price_b = 50.0
        expected_ratio = 2.0
        
        # Act
        ratio = getRatio(price_a, price_b)
        
        # Assert
        self.assertEqual(ratio, expected_ratio)

    def test_getRatio_division_by_zero(self):
        # Arrange
        price_a = 100.0
        price_b = 0.0
        
        # Act
        ratio = getRatio(price_a, price_b)
        
        # Assert
        self.assertIsNone(ratio)

    def test_integration(self):
        # Arrange
        mock_quotes = [
            {'stock': 'ABC', 'top_bid': {'price': '100.00'}, 'top_ask': {'price': '101.00'}},
            {'stock': 'DEF', 'top_bid': {'price': '98.00'}, 'top_ask': {'price': '99.00'}}
        ]
        
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value.read.return_value = json.dumps(mock_quotes).encode('utf-8')
            
            # Act
            data_points = [getDataPoint(quote) for quote in mock_quotes]
            prices = {stock: price for stock, bid_price, ask_price, price in data_points}
            ratio = getRatio(prices["ABC"], prices["DEF"])
        
        # Assert
        self.assertEqual(len(data_points), 2)
        self.assertEqual(prices["ABC"], 100.5)
        self.assertEqual(prices["DEF"], 98.5)
        self.assertEqual(ratio, 100.5 / 98.5)

if __name__ == '__main__':
    unittest.main()
