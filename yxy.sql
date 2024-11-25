-- 创建 yxy 数据库
CREATE DATABASE IF NOT EXISTS yxy;

-- 选择 yxy 数据库
USE yxy;

-- 创建 proxy 表
CREATE TABLE IF NOT EXISTS proxy (
    qq VARCHAR(20) PRIMARY KEY,   -- qq 字段，设置为主键，保证每个 QQ 唯一
    count INT DEFAULT 0           -- count 字段，默认为 0
);

-- 为表添加一个索引 (可选的优化)
CREATE INDEX idx_count ON proxy(count);
