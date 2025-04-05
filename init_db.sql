-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user', -- valores: user, admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuário admin inicial (senha: admin123)
INSERT INTO users (username, password_hash, role)
VALUES (
    'admin',
    -- hash de 'admin123' com bcrypt (gerado por Python depois, vamos ajustar isso futuramente)
    '$2b$12$w4iTGHK2hOhq7jcGbQWxvOK.oe9gzSK7P1KQwVZFAvEfNWvmBFn1a',
    'admin'
)
ON CONFLICT (username) DO NOTHING;

-- Criação da tabela de diagnósticos
CREATE TABLE IF NOT EXISTS diagnostics (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(50),
    latency_ms FLOAT,
    packet_loss FLOAT,
    quality_of_service FLOAT,
    date TIMESTAMP
);

-- Inserção de dados fake
INSERT INTO diagnostics (device_id, city, state, latency_ms, packet_loss, quality_of_service, date)
VALUES
('device-001', 'São Paulo', 'SP', 120.5, 0.3, 4.5, NOW() - INTERVAL '1 day'),
('device-002', 'Rio de Janeiro', 'RJ', 85.1, 0.1, 4.8, NOW() - INTERVAL '2 day'),
('device-003', 'Curitiba', 'PR', 150.0, 0.7, 3.9, NOW());
