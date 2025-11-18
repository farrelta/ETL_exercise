import pytest
from unittest.mock import patch, MagicMock
from utils.extract import get_page_url, extract_page, extract_all

BASE_URL = "https://fashion-studio.dicoding.dev"


class TestGetPageUrl:
    def test_page_one_returns_base_url(self):
        assert get_page_url(1) == BASE_URL
    
    def test_page_two_returns_correct_url(self):
        assert get_page_url(2) == f"{BASE_URL}/page2"
    
    def test_page_fifty_returns_correct_url(self):
        assert get_page_url(50) == f"{BASE_URL}/page50"


class TestExtractPage:
    @patch('utils.extract.requests.get')
    def test_extract_page_success(self, mock_get):
        html_content = """
        <div class="collection-card">
            <div class="product-title">Test Product</div>
            <div class="price">$99.99</div>
            Rating: 4.5
            Colors: 3 Colors
            Size: M
            Gender: Male
        </div>
        """
        mock_response = MagicMock()
        mock_response.text = html_content
        mock_get.return_value = mock_response
        
        result = extract_page(1)
        assert len(result) == 1
        assert result[0]["title"] == "Test Product"
        assert result[0]["price"] == "$99.99"
    
    @patch('utils.extract.requests.get')
    def test_extract_page_missing_price(self, mock_get):
        html_content = """
        <div class="collection-card">
            <div class="product-title">Test Product</div>
            Rating: 4.0
        </div>
        """
        mock_response = MagicMock()
        mock_response.text = html_content
        mock_get.return_value = mock_response
        
        result = extract_page(1)
        assert result[0]["price"] == "Price Unavailable"
    
    @patch('utils.extract.requests.get')
    def test_extract_page_http_error(self, mock_get):
        mock_get.side_effect = Exception("Connection error")
        
        with pytest.raises(Exception):
            extract_page(1)


class TestExtractAll:
    @patch('utils.extract.extract_page')
    def test_extract_all_multiple_pages(self, mock_extract):
        mock_extract.return_value = [{"title": "Product"}]
        
        result = extract_all(1, 3)
        assert len(result) == 3
        assert mock_extract.call_count == 3
    
    @patch('utils.extract.extract_page')
    def test_extract_all_handles_errors(self, mock_extract):
        mock_extract.side_effect = [
            [{"title": "Product1"}],
            Exception("Error"),
            [{"title": "Product3"}]
        ]
        
        result = extract_all(1, 3)
        assert len(result) == 2