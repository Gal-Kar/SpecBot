import React from 'react';
import '../assets/styles/stylesheet.css';

const ReportedItemsList = ({ data }) => {
	const renderItems = () => {
		return data.map((item, index) => (
			<li className="reports-item" key={index}>{item}</li>
		));
	};

	return (
		<ul className="reports">
			{renderItems()}
		</ul>
	);
};

export default ReportedItemsList;