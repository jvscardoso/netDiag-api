-- Criação da tabela de usuários
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    deleted_at TIMESTAMP
);


-- Usuário admin inicial (senha: admin123)
INSERT INTO users (name, email, password_hash, role)
VALUES (
    'admin',
    'admin@netdiag.com',
    '$2b$12$V2IwvlUcMDEjg4bwPF0lZehxjTQ.83fisQjYFxyCmkTAbDwZgiU1q', 
    'admin'
)
ON CONFLICT (email) DO NOTHING;

-- Criação da tabela de diagnósticos
CREATE TABLE IF NOT EXISTS diagnostics (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    latency_ms FLOAT NOT NULL,
    packet_loss FLOAT NOT NULL,
    quality_of_service FLOAT NOT NULL,
    date TIMESTAMP NOT NULL
);


-- Inserção de dados fake
INSERT INTO diagnostics (device_id, city, state, latency_ms, packet_loss, quality_of_service, date)
VALUES
('device-001', 'São Paulo', 'SP', 120.5, 0.3, 4.5, NOW() - INTERVAL '1 day'),
('device-002', 'Rio de Janeiro', 'RJ', 85.1, 0.1, 4.8, NOW() - INTERVAL '2 day'),
('device-003', 'Curitiba', 'PR', 150.0, 0.7, 3.9, NOW());



-- Usuário admin inicial
INSERT INTO users (name, email, password_hash, role)
VALUES (
    'Admin User',
    'admin@netdiag.com',
    '$2b$12$V2IwvlUcMDEjg4bwPF0lZehxjTQ.83fisQjYFxyCmkTAbDwZgiU1q',
    'admin'
)
ON CONFLICT (email) DO NOTHING;
