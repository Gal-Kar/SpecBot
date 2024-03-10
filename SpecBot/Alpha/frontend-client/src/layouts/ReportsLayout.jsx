import React, { useState } from 'react';
import PropTypes from 'prop-types';
import '../assets/styles/stylesheet.css';

const ReportLayout = ({ data }) => {
  const [selectedPriority, setSelectedPriority] = useState(null);
  const [expandedItems, setExpandedItems] = useState({});

  const toggleExpandedItem = (key) => {
    setExpandedItems((prevState) => ({
      ...prevState,
      [key]: !prevState[key],
    }));
  };

  const renderOverviewItems = () => {
    if (data == null || Object.keys(data).length === 0 || Object.values(data).every(items => items.length === 0)) {
      return [];
    }

    const priorityCounts = {};

    Object.values(data).forEach((items) => {
      items.forEach((item) => {
        const priority = item.priority.toLowerCase();
        priorityCounts[priority] = (priorityCounts[priority] || 0) + 1;
      });
    });

    const priorities = ['high', 'medium', 'low'];

    return priorities.map((priority, index) => (
      <li
        key={index}
        className={`overview-item centered ${priority}-priority-highlight`}
        onClick={() => setSelectedPriority(priority)}
      >
        {priorityCounts[priority] || 0}
      </li>
    ));
  };

  const capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
  };

  const renderReportItems = () => {
    if (!data || Object.keys(data).length === 0 || Object.values(data).every(items => items.length === 0)) {
      return null;
    }

    const filteredData = selectedPriority
      ? Object.entries(data).map(([url, items]) => ({
        url,
        items: items.filter((item) => item.priority.toLowerCase() === selectedPriority),
      }))
      : Object.entries(data).map(([url, items]) => ({
        url,
        items,
    }));

    return filteredData.map(({ url, items }) => (
      <div key={url}>
        {items.map((item, index) => {
          const isExpanded = expandedItems[`${url}-${index}`];

          return (
            <li key={`${url}-${index}`} className="reports-item">
              <div className={`report-entry ${isExpanded ? 'expanded' : ''}`}>
                <div className="flex">
                  <span className="arrow" onClick={() => toggleExpandedItem(`${url}-${index}`)}>
                    <i className={`fas fa-angle-${isExpanded ? 'up' : 'down'} fa-xs" style="color: #000000;`}></i>
                  </span>
                  <span className="message bold">{item.type}</span>
                  <span className={`bold priority ${item.priority.toLowerCase()}-priority-color`}>{capitalize(item.priority)}</span>
                </div>
                {isExpanded && (
                  <div className="flex">
                    <div className="detials-container">
                      <span className="url">
                        <span className="bold">Full Path:</span> {url}
                        { item.firstColumn !== -1 &&
                          item.lastColumn !== -1 &&
                          item.lastLine !== -1 ? ' ' + item.lastLine + ':' + item.firstColumn + ':' + item.lastColumn : ''
                        }
                      </span>
                      <span className="type">{item.message}</span>
                      <span className="suggestions">
                        {item.block_code.length === 0 ? (
                          <React.Fragment>
                            <span className="bold">Suggestions:</span>
                            {item.suggestions.map((suggestion, idx) => (
                              <React.Fragment key={idx}>
                                <br />
                                {suggestion.includes("No solution") ? (
                                  <span>{suggestion}</span>
                                ) : (
                                  <a href={suggestion}>{suggestion}</a>
                                )}
                              </React.Fragment>
                            ))}
                          </React.Fragment>
                        ) : (
                          <React.Fragment>
                            {item.block_code.map((block, idx) => {
                              const modifiedBlock = block.split("~~~~")[0].split('[*]');
                              const suggestion = block.split("~~~~")[1];

                              return (
                                <span key={idx}>
                                  <span className="bold">Issue:</span> {modifiedBlock[0]}
                                  <span className="bold">[*]</span> {modifiedBlock[1]}
                                  <br />
                                  <span className="bold">Suggestion:</span> {suggestion.replace('~~~', '')}
                                  <br />
                                </span>
                              );
                            })}
                          </React.Fragment>
                        )}
                      </span>
                    </div>
                  </div>
                )}
              </div>
            </li>
          );
        })}
      </div>
    ));
  };
  console.log(Object.keys(data).length);
  return (
    <div className="reports-container">
      <ul className="overview">
        {renderOverviewItems()}
      </ul>
      {Object.keys(data).length === 0 && <p className="processing-message">Processing...</p>}
      <ul className="reports">
        {renderReportItems()}
      </ul>
    </div>
  );
};

ReportLayout.propTypes = {
  data: PropTypes.objectOf(
    PropTypes.arrayOf(
      PropTypes.shape({
        priority: PropTypes.string.isRequired,
        type: PropTypes.string.isRequired,
        lastLine: PropTypes.number.isRequired,
        lastColumn: PropTypes.number.isRequired,
        firstColumn: PropTypes.number.isRequired,
        message: PropTypes.string.isRequired,
        block_code: PropTypes.array.isRequired,
        suggestions: PropTypes.array.isRequired
      })
    )
  ).isRequired,
};

export default ReportLayout;