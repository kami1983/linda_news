import React from 'react';
import { strongAndWeekColor } from '../utils/colorUtils'; // 导入函数

const ColorLegend = () => {
  return (
    <div>
      <div>颜色图例 0~99% 越红估值越高</div>
      {Array.from({ length: 20 }, (_, i) => i * 5).map((i) => (
        <div
          key={i}
          style={{
            display: 'inline-block',
            width: '10px',
            height: '10px',
            backgroundColor: strongAndWeekColor(i.toString()),
            marginRight: '2px'
          }}
          title={`${i}%`}
        />
      ))}
    </div>
  );
};

export default ColorLegend; 