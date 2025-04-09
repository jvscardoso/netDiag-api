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

-- Usuário admin inicial (senha: admin123)
INSERT INTO users (name, email, password_hash, role)
VALUES (
    'Joe Doe Analyst',
    'analyst@netdiag.com',
    '$2b$12$V2IwvlUcMDEjg4bwPF0lZehxjTQ.83fisQjYFxyCmkTAbDwZgiU1q', 
    'analyst'
)
ON CONFLICT (email) DO NOTHING;

-- Usuário admin inicial (senha: admin123)
INSERT INTO users (name, email, password_hash, role)
VALUES (
    'Joe Doe User',
    'user@netdiag.com',
    '$2b$12$V2IwvlUcMDEjg4bwPF0lZehxjTQ.83fisQjYFxyCmkTAbDwZgiU1q', 
    'user'
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
INSERT INTO diagnostics (device_id, city, state, latency_ms, packet_loss, quality_of_service, date) VALUES
('device-sp-001', 'São Paulo', 'SP', 110.2, 0.2, 4.6, NOW() - INTERVAL '1 day'),
('device-sp-002', 'Campinas', 'SP', 130.0, 0.5, 4.2, NOW() - INTERVAL '2 day'),
('device-rj-001', 'Rio de Janeiro', 'RJ', 90.1, 0.3, 4.7, NOW() - INTERVAL '1 day'),
('device-rj-002', 'Niterói', 'RJ', 95.0, 0.2, 4.5, NOW() - INTERVAL '2 day'),
('device-mg-001', 'Belo Horizonte', 'MG', 105.3, 0.4, 4.3, NOW() - INTERVAL '1 day'),
('device-mg-002', 'Uberlândia', 'MG', 115.6, 0.5, 4.1, NOW() - INTERVAL '3 day'),
('device-es-001', 'Vitória', 'ES', 98.7, 0.3, 4.4, NOW() - INTERVAL '1 day'),
('device-es-002', 'Vila Velha', 'ES', 100.4, 0.2, 4.6, NOW() - INTERVAL '2 day'),
('device-pr-001', 'Curitiba', 'PR', 120.0, 0.2, 4.2, NOW() - INTERVAL '1 day'),
('device-pr-002', 'Londrina', 'PR', 130.3, 0.4, 4.0, NOW() - INTERVAL '2 day'),
('device-rs-001', 'Porto Alegre', 'RS', 140.5, 0.5, 4.1, NOW() - INTERVAL '1 day'),
('device-rs-002', 'Caxias do Sul', 'RS', 135.6, 0.3, 4.3, NOW() - INTERVAL '2 day'),
('device-sc-001', 'Florianópolis', 'SC', 110.7, 0.2, 4.5, NOW() - INTERVAL '1 day'),
('device-sc-002', 'Joinville', 'SC', 115.8, 0.3, 4.2, NOW() - INTERVAL '2 day'),
('device-go-001', 'Goiânia', 'GO', 125.1, 0.3, 4.0, NOW() - INTERVAL '1 day'),
('device-go-002', 'Anápolis', 'GO', 128.5, 0.4, 3.9, NOW() - INTERVAL '2 day'),
('device-mt-001', 'Cuiabá', 'MT', 135.4, 0.6, 3.8, NOW() - INTERVAL '1 day'),
('device-mt-002', 'Várzea Grande', 'MT', 132.3, 0.5, 3.7, NOW() - INTERVAL '2 day'),
('device-ms-001', 'Campo Grande', 'MS', 127.0, 0.3, 4.1, NOW() - INTERVAL '1 day'),
('device-ms-002', 'Dourados', 'MS', 129.6, 0.4, 4.0, NOW() - INTERVAL '2 day'),
('device-df-001', 'Brasília', 'DF', 100.0, 0.2, 4.5, NOW() - INTERVAL '1 day'),
('device-df-002', 'Taguatinga', 'DF', 105.2, 0.3, 4.4, NOW() - INTERVAL '2 day'),
('device-ba-001', 'Salvador', 'BA', 145.0, 0.5, 3.9, NOW() - INTERVAL '1 day'),
('device-ba-002', 'Feira de Santana', 'BA', 142.3, 0.4, 4.0, NOW() - INTERVAL '2 day'),
('device-pe-001', 'Recife', 'PE', 130.8, 0.3, 4.2, NOW() - INTERVAL '1 day'),
('device-pe-002', 'Jaboatão', 'PE', 132.0, 0.4, 4.1, NOW() - INTERVAL '2 day'),
('device-ce-001', 'Fortaleza', 'CE', 138.5, 0.3, 4.0, NOW() - INTERVAL '1 day'),
('device-ce-002', 'Caucaia', 'CE', 136.7, 0.4, 4.1, NOW() - INTERVAL '2 day'),
('device-rn-001', 'Natal', 'RN', 125.6, 0.2, 4.3, NOW() - INTERVAL '1 day'),
('device-rn-002', 'Mossoró', 'RN', 127.4, 0.3, 4.2, NOW() - INTERVAL '2 day'),
('device-ma-001', 'São Luís', 'MA', 139.8, 0.4, 3.8, NOW() - INTERVAL '1 day'),
('device-ma-002', 'Imperatriz', 'MA', 137.2, 0.5, 3.9, NOW() - INTERVAL '2 day'),
('device-pi-001', 'Teresina', 'PI', 129.1, 0.3, 4.0, NOW() - INTERVAL '1 day'),
('device-pi-002', 'Parnaíba', 'PI', 130.9, 0.4, 3.9, NOW() - INTERVAL '2 day'),
('device-pb-001', 'João Pessoa', 'PB', 128.4, 0.3, 4.2, NOW() - INTERVAL '1 day'),
('device-pb-002', 'Campina Grande', 'PB', 126.7, 0.2, 4.1, NOW() - INTERVAL '2 day'),
('device-al-001', 'Maceió', 'AL', 122.5, 0.3, 4.1, NOW() - INTERVAL '1 day'),
('device-al-002', 'Arapiraca', 'AL', 124.8, 0.4, 4.0, NOW() - INTERVAL '2 day'),
('device-se-001', 'Aracaju', 'SE', 119.9, 0.2, 4.3, NOW() - INTERVAL '1 day'),
('device-se-002', 'Nossa Senhora do Socorro', 'SE', 121.3, 0.3, 4.2, NOW() - INTERVAL '2 day');

INSERT INTO diagnostics (device_id, city, state, latency_ms, packet_loss, quality_of_service, date) VALUES
('device-pa-001', 'Belém', 'PA', 140.6, 0.5, 3.9, NOW() - INTERVAL '1 day'),
('device-pa-002', 'Ananindeua', 'PA', 142.7, 0.6, 3.8, NOW() - INTERVAL '2 day'),
('device-am-001', 'Manaus', 'AM', 150.0, 0.7, 3.7, NOW() - INTERVAL '1 day'),
('device-am-002', 'Itacoatiara', 'AM', 148.4, 0.6, 3.6, NOW() - INTERVAL '2 day'),
('device-ro-001', 'Porto Velho', 'RO', 137.0, 0.4, 4.0, NOW() - INTERVAL '1 day'),
('device-ro-002', 'Ji-Paraná', 'RO', 135.2, 0.3, 4.1, NOW() - INTERVAL '2 day'),
('device-ac-001', 'Rio Branco', 'AC', 138.3, 0.5, 3.9, NOW() - INTERVAL '1 day'),
('device-ac-002', 'Cruzeiro do Sul', 'AC', 136.9, 0.4, 4.0, NOW() - INTERVAL '2 day'),
('device-rr-001', 'Boa Vista', 'RR', 139.5, 0.4, 3.8, NOW() - INTERVAL '1 day'),
('device-rr-002', 'Rorainópolis', 'RR', 137.8, 0.3, 3.9, NOW() - INTERVAL '2 day'),
('device-ap-001', 'Macapá', 'AP', 141.0, 0.5, 3.7, NOW() - INTERVAL '1 day'),
('device-ap-002', 'Santana', 'AP', 142.2, 0.6, 3.6, NOW() - INTERVAL '2 day'),
('device-to-001', 'Palmas', 'TO', 132.1, 0.4, 4.1, NOW() - INTERVAL '1 day'),
('device-to-002', 'Araguaína', 'TO', 134.0, 0.5, 4.0, NOW() - INTERVAL '2 day');


-- Usuário admin inicial
INSERT INTO users (name, email, password_hash, role)
VALUES (
    'Admin User',
    'admin@netdiag.com',
    '$2b$12$V2IwvlUcMDEjg4bwPF0lZehxjTQ.83fisQjYFxyCmkTAbDwZgiU1q',
    'admin'
)
ON CONFLICT (email) DO NOTHING;
