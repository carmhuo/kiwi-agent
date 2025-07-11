-- 启用外键支持
PRAGMA foreign_keys = ON;

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    encrypted_password VARCHAR(128) NOT NULL,
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 角色表
CREATE TABLE IF NOT EXISTS role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code INTEGER UNIQUE NOT NULL,
    description TEXT
);

-- 用户角色关联表
CREATE TABLE IF NOT EXISTS user_role (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- 项目表
CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

-- 数据源表
CREATE TABLE IF NOT EXISTS data_source (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    connection_config TEXT NOT NULL,  -- JSON格式
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);

-- 数据集表
CREATE TABLE IF NOT EXISTS dataset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    configuration TEXT NOT NULL,  -- JSON格式
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);

-- 数据集数据源关联表
CREATE TABLE IF NOT EXISTS dataset_data_source (
    dataset_id INTEGER NOT NULL,
    data_source_id INTEGER NOT NULL,
    alias VARCHAR(100) NOT NULL,
    PRIMARY KEY (dataset_id, alias),
    FOREIGN KEY (dataset_id) REFERENCES dataset(id),
    FOREIGN KEY (data_source_id) REFERENCES data_source(id)
);

-- Agent表
CREATE TABLE IF NOT EXISTS agent (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    config TEXT NOT NULL,  -- JSON格式
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);

-- Agent版本表
CREATE TABLE IF NOT EXISTS agent_version (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    version VARCHAR(20) NOT NULL,
    config TEXT NOT NULL,  -- JSON格式
    checksum CHAR(64) NOT NULL,  -- SHA256校验和
    created_by INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT 0,
    FOREIGN KEY (agent_id) REFERENCES agent(id),
    FOREIGN KEY (created_by) REFERENCES user(id)
);

-- Agent指标表
CREATE TABLE IF NOT EXISTS agent_metric (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_version_id INTEGER NOT NULL,
    sql_gen_latency REAL NOT NULL,
    query_success_rate REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_version_id) REFERENCES agent_version(id)
);

-- 对话表
CREATE TABLE IF NOT EXISTS conversation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 消息表
CREATE TABLE IF NOT EXISTS message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    role VARCHAR(10) NOT NULL,  -- user/assistant
    sql_query TEXT,
    report_data TEXT,  -- JSON格式
    feedback_type INTEGER,  -- 1=结果正确,0=完全错误,2=部分正确,3=建议改进
    feedback_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversation(id),
    CHECK (feedback_type != 3 OR feedback_text IS NOT NULL)  -- 改进建议需有文本
);

-- 项目成员表
CREATE TABLE IF NOT EXISTS project_member (
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

-- 审计日志表
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operator_id INTEGER NOT NULL,
    action VARCHAR(20) NOT NULL,  -- CREATE/UPDATE/DELETE
    target_type VARCHAR(30) NOT NULL,  -- DATASOURCE/AGENT等
    old_value TEXT,  -- JSON格式
    new_value TEXT,  -- JSON格式
    ip_address TEXT,  -- SQLite不支持INET类型
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (operator_id) REFERENCES user(id)
);

-- 数据脱敏规则表
CREATE TABLE IF NOT EXISTS data_masking_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    field_pattern VARCHAR(100) NOT NULL,
    mask_type TEXT NOT NULL CHECK (mask_type IN ('partial', 'hash', 'full')),
    template VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引优化查询性能
CREATE INDEX IF NOT EXISTS idx_message_conversation ON message(conversation_id);
CREATE INDEX IF NOT EXISTS idx_message_feedback ON message(feedback_type);
CREATE INDEX IF NOT EXISTS idx_project_owner ON project(owner_id);
CREATE INDEX IF NOT EXISTS idx_dataset_project ON dataset(project_id);
CREATE INDEX IF NOT EXISTS idx_conversation_user ON conversation(user_id);
CREATE INDEX IF NOT EXISTS idx_agent_version ON agent_version(agent_id, version);
CREATE INDEX IF NOT EXISTS fk_data_source_project ON data_source(project_id);
CREATE INDEX IF NOT EXISTS fk_conversation_project ON conversation(project_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_operator ON audit_log(operator_id);