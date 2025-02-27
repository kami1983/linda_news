
export const strongAndWeekColor = (percentageStr) => {
    // 从字符串中提取数值部分
    let percentage = parseFloat(percentageStr);
    if(percentage>99)percentage=99;
    // 验证提取的数值是否为有效百分比
    if (isNaN(percentage) || percentage < 0 || percentage > 99) {
        throw new Error(`Invalid percentage: ${percentageStr}. Must be between 0% and 99%.`);
    }

    // 计算红色和绿色分量
    const red = Math.round((percentage / 99) * 255);
    const green = Math.round(((99 - percentage) / 99) * 255);

    // 返回 RGB 颜色值
    return `rgb(${red}, ${green}, 0)`;
  };