const AWS = require('aws-sdk');

AWS.config.update({
	credentials: {
		accessKeyId: 'AWS_ACCESS_KEY',
		secretAccessKey: 'SECRET_ACCESS_KEY',
	},
	region: 'eu-west-1',
});

const sqs = new AWS.SQS();

const get_region_and_account_id = () => {
	const region = 'eu-west-1'
	const accountId = 'ACCCOUNT_ID'
	return [region, accountId]
}

const pollSQS = async (queueName) => {
	console.log(`Starting polling from ${queueName} SQS`);

	const [region, accountId] = get_region_and_account_id();
	const queueUrl = `https://sqs.${region}.amazonaws.com/${accountId}/${queueName}`;

	const receiveParams = {
		QueueUrl: queueUrl,
		MaxNumberOfMessages: 1,
		WaitTimeSeconds: 20,
	};

	let count = 0;

	while (true) {
		console.log(`Starting ${count} polling from ${queueName}`);
		count += 1;

		try {
			const response = await sqs.receiveMessage(receiveParams).promise();

			if (response.Messages) {
				const message = response.Messages[0];
				const body = message.Body;

				// Process the received message
				const deleteParams = {
					QueueUrl: queueUrl,
					ReceiptHandle: message.ReceiptHandle,
				};

				await sqs.deleteMessage(deleteParams).promise(); // Delete the message after processing

				return body;
			}
		} catch (error) {
			// console.log('Error receiving or deleting message (for internal use only):', error);
		}
	}
};

const sendToSQS = (queueName, message) => {
	const [region, accountId] = get_region_and_account_id()
	const queueUrl = `https://sqs.${region}.amazonaws.com/${accountId}/${queueName}`

	const params = {
		MessageBody: message,
		QueueUrl: queueUrl
	};

	sqs.sendMessage(params, (err, _) => {
		if (err) {
			console.log('Error sending message to SQS:', err);
			return;
		}
	})
};

const downloadFromS3 = async (bucketName, bucketPath) => {
	const s3 = new AWS.S3();

	try {
		const response = await s3.getObject({
			Bucket: bucketName,
			Key: bucketPath,
		}).promise(); // Use .promise() to await the resolution of the promise

		const bodyData = response.Body.toString('utf-8');
		return JSON.parse(bodyData);
	} catch (error) {
		console.log('Error downloading from S3:', error);
		throw error;
	}
};

module.exports = {
	pollSQS,
	sendToSQS,
	downloadFromS3
}