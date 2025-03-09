import os
import pytest
from unittest.mock import patch, MagicMock
import omni.client

from i4h_asset_helper.assets import (
    get_i4h_asset_path,
    retrieve_asset,
    I4H_ASSET_ROOT,
    SHA256_HASH,
)

@pytest.fixture
def mock_omni_client():
    with patch('omni.client') as mock_client:
        # Set up default return values
        mock_client.Result.OK = 'OK'
        mock_client.stat.return_value = ('OK', None)
        mock_client.read_file.return_value = ('OK', None, b'mock_file_content')
        yield mock_client

def test_get_i4h_asset_path_valid_version(mock_omni_client):
    # Test with valid version
    result = get_i4h_asset_path(version="0.1")
    expected_path = f"{I4H_ASSET_ROOT['nucleus']}/Library/IsaacHealthcare/0.1/i4h-assets-v0.1-{SHA256_HASH['0.1']}.zip"
    assert result == expected_path

def test_get_i4h_asset_path_invalid_version():
    # Test with invalid version
    with pytest.raises(ValueError, match="Invalid version"):
        get_i4h_asset_path(version="invalid")

def test_get_i4h_asset_path_asset_not_found(mock_omni_client):
    # Mock stat to return non-OK result
    mock_omni_client.stat.return_value = ('ERROR', None)
    
    with pytest.raises(ValueError, match="Asset not found"):
        get_i4h_asset_path(version="0.1")

@pytest.fixture
def mock_temp_dir(tmp_path):
    return tmp_path

def test_retrieve_asset_success(mock_omni_client, mock_temp_dir):
    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_tempdir.return_value.__enter__.return_value = str(mock_temp_dir)
        
        result = retrieve_asset(version="0.1", download_dir=str(mock_temp_dir))
        
        # Verify the result is a path in the mock temp directory
        assert os.path.exists(result)
        assert str(mock_temp_dir) in result

def test_retrieve_asset_download_failure(mock_omni_client, mock_temp_dir):
    # Mock read_file to return error
    mock_omni_client.read_file.return_value = ('ERROR', None, None)
    
    with pytest.raises(ValueError, match="Failed to download asset"):
        retrieve_asset(version="0.1", download_dir=str(mock_temp_dir))

def test_retrieve_asset_existing_no_force(mock_omni_client, mock_temp_dir):
    # Create mock existing directory
    existing_path = os.path.join(mock_temp_dir, SHA256_HASH["0.1"])
    os.makedirs(existing_path)
    
    result = retrieve_asset(version="0.1", download_dir=str(mock_temp_dir), force_download=False)
    
    # Should return existing path without downloading
    assert result == existing_path
    mock_omni_client.read_file.assert_not_called()

def test_retrieve_asset_force_download(mock_omni_client, mock_temp_dir):
    # Create mock existing directory
    existing_path = os.path.join(mock_temp_dir, SHA256_HASH["0.1"])
    os.makedirs(existing_path)
    
    with patch('tempfile.TemporaryDirectory') as mock_tempdir:
        mock_tempdir.return_value.__enter__.return_value = str(mock_temp_dir)
        
        result = retrieve_asset(version="0.1", download_dir=str(mock_temp_dir), force_download=True)
        
        # Should download even though directory exists
        mock_omni_client.read_file.assert_called_once()
        assert result == existing_path 