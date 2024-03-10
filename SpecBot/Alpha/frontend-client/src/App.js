import React, { useState } from 'react';
import './assets/styles/stylesheet.css';
import ScanInputComponent from './components/ScanInputComponent';
import ReportLayout from './layouts/ReportsLayout';
import AwsHelper from './components/AwsHelper';
import { SpinnerDotted } from 'spinners-react';

function App() {
  const [data, setData] = useState({});
  const [showScanInput, setShowScanInput] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const sqsBucket = [
    { queueName: 'vulnerability-scanner-result', bucketName: 'vulnerability-scn' },
    { queueName: 'js-syntax-checker-result', bucketName: 'js-syntax-checker' },
    { queueName: 'html-validator-result', bucketName: 'html-validator' },
    { queueName: 'error-scanner-result', bucketName: 'error-scanner' }
  ];

  const processQueue = async ({ queueName, bucketName }) => {
    const bucketPath = await AwsHelper.pollSQS(queueName); // Poll from SQS and get the message body

    if (!bucketPath) {
      console.log(`Error: Missing data from SQS for queue ${queueName}`);
      return null;
    }

    const fileData = await AwsHelper.downloadFromS3(bucketName, bucketPath); // Download file from S3

    if (!fileData) {
      console.log(`Error: Missing data from S3 for bucket ${bucketName}`);
      return null;
    }

    return fileData;
  };

  const handleScanButtonClick = async () => {
    const url = document.getElementById('url').value;
    const formattedUrl = url.endsWith('/') ? url.slice(0, -1) : url;

    AwsHelper.sendToSQS('parent-crawler', formattedUrl); // Send the url to 'parent-crw' SQS queue

    setShowScanInput(false);
    setIsLoading(true);

    const promises = sqsBucket.map(processQueue);

    await Promise.all(
      promises.map(async (promise) => {
        const data = await promise;
        if (data !== null) {
          setData((previousData) => ({ ...data, ...previousData }));
          // setData((previousData) => ({ ...previousData, ...data }));
        }
      })
    );

    setIsLoading(false);
  };

  return (
    <div className="wrapper">
      <header>
        <div className="logo"></div>
      </header>
      <div className="content-wrapper">
        {showScanInput && <ScanInputComponent onScanButtonClick={handleScanButtonClick} />}
        {isLoading && (
          <div className="spinner-loading">
            <SpinnerDotted className="spinner" />
          </div>
        )}
        {!showScanInput && <ReportLayout data={data} />}
      </div>
      <footer>Powered by the Three Musketeers</footer>
    </div>
  );
}

export default App;