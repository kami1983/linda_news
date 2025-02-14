import React from 'react';
import './Home.css'; // 导入样式文件

function Home() {
  return (
    <div className="home-container">
      <h1 className="home-title">欢迎来到AI投资消息分析平台</h1>
      <p className="home-description">
        我们的平台通过分析最新的投资新闻，帮助您做出明智的投资决策。利用先进的AI技术，我们为您提供精准的投资方向建议。
      </p>
      <div className="home-features">
        <div className="feature">
          <h2>实时新闻分析</h2>
          <p>获取最新的投资新闻，实时分析市场动态。</p>
        </div>
        <div className="feature">
          <h2>智能投资建议</h2>
          <p>基于AI的投资建议，帮助您做出更好的决策。</p>
        </div>
        <div className="feature">
          <h2>个性化服务</h2>
          <p>根据您的投资偏好，提供定制化的分析报告。</p>
        </div>
      </div>
    </div>
  );
}

export default Home; 