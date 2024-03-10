import React from 'react';
import '../assets/styles/stylesheet.css';

const ReportSummaryBoxes = ({ data }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'critical':
        return 'critical-priority';
      case 'medium':
        return 'medium-priority';
      default:
      case 'low':
        return 'low-priority';
    }
  };

	const renderItems = () => {
    return data.map((item, index) => (
      <li key={index} className={`${getPriorityColor(item.priority)} overview-item centered`}>
        {item.number}
      </li>
    ));
  };

	return <ul className="overview">{renderItems()}</ul>;
};

export default ReportSummaryBoxes;