-- 创建行程统计表
CREATE TABLE IF NOT EXISTS trip_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL UNIQUE,
    total_expense FLOAT DEFAULT 0.0 COMMENT '总支出',
    average_expense FLOAT DEFAULT 0.0 COMMENT '人均支出',
    member_count INT DEFAULT 0 COMMENT '成员数量',
    category_totals JSON COMMENT '分类汇总',
    category_ratios JSON COMMENT '分类占比',
    transaction_count INT DEFAULT 0 COMMENT '交易总数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_trip_stats_trip_id (trip_id),
    INDEX idx_trip_stats_updated_at (updated_at),
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='行程统计表';

-- 创建成员统计表
CREATE TABLE IF NOT EXISTS member_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    member_id INT NOT NULL,
    member_name VARCHAR(100) COMMENT '成员名称冗余字段',
    total_amount FLOAT DEFAULT 0.0 COMMENT '总支出',
    by_category JSON COMMENT '按分类统计',
    by_wallet JSON COMMENT '按钱包统计',
    should_pay FLOAT DEFAULT 0.0 COMMENT '应付金额（平均值）',
    actual_paid FLOAT DEFAULT 0.0 COMMENT '实际支付金额',
    balance FLOAT DEFAULT 0.0 COMMENT '差额（实际-应付）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_member_stats_trip_id (trip_id),
    INDEX idx_member_stats_member_id (member_id),
    UNIQUE INDEX idx_member_stats_trip_member (trip_id, member_id),
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='成员统计表';

-- 创建钱包统计表
CREATE TABLE IF NOT EXISTS wallet_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trip_id INT NOT NULL,
    wallet_id INT NOT NULL UNIQUE,
    wallet_name VARCHAR(100) COMMENT '钱包名称冗余字段',
    balance_by_member JSON COMMENT '成员余额',
    total_balance FLOAT DEFAULT 0.0 COMMENT '总余额',
    transaction_count INT DEFAULT 0 COMMENT '交易数量',
    total_deposited FLOAT DEFAULT 0.0 COMMENT '总存入',
    total_spent FLOAT DEFAULT 0.0 COMMENT '总支出',
    remaining FLOAT DEFAULT 0.0 COMMENT '剩余金额',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_wallet_stats_trip_id (trip_id),
    INDEX idx_wallet_stats_wallet_id (wallet_id),
    INDEX idx_wallet_stats_updated_at (updated_at),
    FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
    FOREIGN KEY (wallet_id) REFERENCES wallets(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='钱包统计表';
