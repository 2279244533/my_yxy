const express = require('express');
const crypto = require('crypto'); // 引入 Node.js 的 crypto 模块
const app = express();
const port = 8001;

// 配置文件中的签名服务器配置
const signServers = [
  {
    url: 'http://localhost:8080/sign',  // 主签名服务器地址
    key: 'your-api-key',                // API Key 或者密钥
    authorization: 'Bearer your-token'  // 授权信息，例如Bearer Token
  },
  {
    url: '-',                          // 备用签名服务器地址
    key: 'backup-api-key',             // 备用 API Key 或者密钥
    authorization: 'Bearer backup-token'// 备用授权信息，例如Bearer Token
  }
];

// 定义签名生成逻辑，随机生成一个签名
function generateSignature() {
  // 生成一个随机的签名值，这里使用 Node.js 的 crypto 模块生成一个随机的 32 字节长度的十六进制字符串
  return crypto.randomBytes(16).toString('hex'); // 这里生成的是 32 字节的十六进制字符串
}

// 处理 /sign 路由请求
app.get('/sign', (req, res) => {
  // 调用签名生成逻辑，得到随机生成的签名
  const signature = generateSignature();

  // 返回签名
  res.send({ sign: signature });
});

// 启动服务器
app.listen(port, () => {
  console.log(`Signature server listening at http://localhost:${port}`);
});
