import React, { useState } from 'react';
import { strongAndWeekColor } from '../utils/colorUtils'; // 导入颜色计算函数

const ColorIndicator = ({ value, tipstr }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <span
      style={{
        display: 'inline-block',
        width: '10px',
        height: '10px',
        borderRadius: '50%',
        backgroundColor: strongAndWeekColor(value),
        marginLeft: '5px',
        position: 'relative'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {isHovered && tipstr && (
        <span
          style={{
            position: 'absolute',
            top: '-20px',
            left: '50%',
            transform: 'translateX(-50%)',
            backgroundColor: 'white',
            border: '1px solid black',
            padding: '2px 5px',
            borderRadius: '3px',
            whiteSpace: 'nowrap',
            zIndex: 1
          }}
        >
          {tipstr}
        </span>
      )}
    </span>
  );
};

export default ColorIndicator; 