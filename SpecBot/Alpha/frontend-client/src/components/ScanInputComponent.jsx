import React, { useEffect, useState } from 'react';
import '../assets/styles/stylesheet.css';
import validator from 'validator';

const ScanInputComponent = ({ onScanButtonClick }) => {
  const [url, setUrl] = useState('');

  const removeWWW = (str) => str.replace(/(www\.)/, '');

  const handleInputChange = (event) => {
    const inputValue = removeWWW(event.target.value.trim());
    const pattern = /^https?:\/\//i;
    const securePattern = /^https:\/\/?/i;

    if (!pattern.test(inputValue)) {
      const value = inputValue.replace(/^https?:\/*/, '');
      if (securePattern.test(inputValue)) {
        event.target.value = 'https://' + value;
      } else {
        event.target.value = 'http://' + value;
      }
    }

    setUrl(event.target.value);
  };

  const handleScanButtonClick = () => {
    if (isValidUrl(url)) {
      onScanButtonClick(url);
    } else {
      // TODO: add alert
      // const inputURL = document.getElementById('url');
      console.log('Invalid URL');
    }
  };

  const isValidUrl = (url) => {
    return validator.isURL(url);
  };

  useEffect(() => {
    const inputURL = document.getElementById('url');

    const handlePaste = (event) => {
      event.preventDefault();
      const clipboardData = event.clipboardData || window.clipboardData;
      const pastedData = clipboardData.getData('text/plain');

      inputURL.value = removeWWW(pastedData);
      setUrl(inputURL.value);
    };

    inputURL.addEventListener('paste', handlePaste);

    return () => {
      inputURL.removeEventListener('paste', handlePaste);
    };
  }, []);

  return (
    <div className="scanner" >
      <input
        type="text"
        name="url"
        id="url"
        className="scanner-term"
        placeholder="http://"
        value={url}
        onChange={handleInputChange}
      />
      <button type="submit" className="scan-button" onClick={handleScanButtonClick}>
        Scan
      </button>
    </div>
  );
};

export default ScanInputComponent;